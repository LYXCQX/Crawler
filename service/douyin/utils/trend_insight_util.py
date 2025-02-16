import asyncio
import os
import time

import loguru
from playwright.async_api import async_playwright
import json
from datetime import datetime
from typing import List, Dict
import logging
from crawlers.hybrid.hybrid_crawler import HybridCrawler
from Crawler.service.douyin.views.buyin_login import get_account_file
from social_auto_upload.conf import LOCAL_CHROME_PATH
from social_auto_upload.utils.base_social_media import set_init_script
from youdub.util.sql_utils import getdb
hybridCrawler = HybridCrawler()

class TrendInsightCrawler:
    def __init__(self):
        self.base_url = "https://trendinsight.oceanengine.com/arithmetic-index/videosearch"
        self.api_url = "https://trendinsight.oceanengine.com/api/v2/index/itemQuery"
        self.processed_urls_file = "E:\IDEA\workspace\YouDub-webui\data\douyin\dwn_txt\playlet.txt"
        self.processed_urls = self._load_processed_urls()

    def _load_processed_urls(self) -> set:
        """加载已处理过的URL"""
        try:
            if os.path.exists(self.processed_urls_file):
                with open(self.processed_urls_file, 'r', encoding='utf-8') as f:
                    return set(line.strip() for line in f)
            return set()
        except Exception as e:
            logging.error(f"加载已处理URL文件失败: {str(e)}")
            return set()

    def _save_processed_url(self, url: str):
        """保存已处理的URL"""
        try:
            with open(self.processed_urls_file, 'a', encoding='utf-8') as f:
                f.write(f"{url}\n")
            self.processed_urls.add(url)
        except Exception as e:
            logging.error(f"保存已处理URL失败: {str(e)}")

    async def crawl_video_list(self, query: str = "短剧") -> List[Dict]:
        """
        爬取巨量算数榜单视频列表
        
        Args:
            query: 搜索关键词
            
        Returns:
            List[Dict]: 视频信息列表
        """
        async with async_playwright() as playwright:
            # 启动浏览器时添加更多配置
            browser = await playwright.chromium.launch(
                headless=False,
                executable_path=LOCAL_CHROME_PATH,  # 请替换为实际的Chrome路径
                args=['--start-maximized']
            )
            storage_path = get_account_file('222528105620820')
            # 使用保存的登录状态
            context = await browser.new_context(
                storage_state=storage_path,
                no_viewport=True
            )
            # 设置初始化脚本
            context = await set_init_script(context)
            page = await context.new_page()

            # 初始化视频数据列表
            video_data = []

            async def handle_response(response):
                nonlocal video_data  # 使用nonlocal访问外部变量
                if self.api_url in response.url:
                    try:
                        request = response.request
                        post_data = request.post_data
                        if isinstance(post_data, str):
                            post_data = json.loads(post_data)
                        if post_data.get('labelType', '0') == 1 and post_data.get('dateType', '0') == 7:
                            data = await response.json()
                            if data and "data" in data and "data" in data["data"]:
                                items = data["data"]["data"]
                                for item in items:
                                    video_info = {
                                        "video_url": item["url"],
                                        "title": item["title"],
                                        "author": item["nickname"],
                                        "likes": int(item["likes"]),
                                        "duration": item["duration"],
                                        "create_time": item["createTime"],
                                        "fans_count": item["fans"],
                                        "thumbnail": item["thumbnail"]
                                    }
                                    video_data.append(video_info)
                    except Exception as e:
                        logging.error(f"解析响应数据失败: {str(e)}")

            # 监听网络请求
            page.on("response", handle_response)

            # 访问页面
            await page.goto(f"{self.base_url}?query={query}")
            
            # 点击"类型不限"的父元素
            await page.click('input[value="类型不限"] >> xpath=..')
            await page.wait_for_timeout(1000)  # 等待1秒确保点击生效
            
            # 点击"低粉爆款"
            await page.click('div:text("低粉爆款")')

            # 点击"类型不限"的父元素
            await page.click('input[value="发布时间不限"] >> xpath=..')
            await page.wait_for_timeout(1000)  # 等待1秒确保点击生效

            # 点击"低粉爆款"
            await page.click('div:text("近7天")')
            # 等待数据加载，最多等待30秒
            max_wait_time = 30
            start_time = time.time()
            while len(video_data) == 0:
                await page.wait_for_timeout(1000)  # 每秒检查一次
                if time.time() - start_time > max_wait_time:
                    raise TimeoutError("获取视频数据超时")

            await context.storage_state(path=storage_path)
            await browser.close()
            return video_data if video_data else []

    def save_to_transport_job(self, video_data: List[Dict]):
        """
        将视频数据保存到transport_job表，仅保存包含anchor_info的视频
        
        Args:
            video_data: 视频信息列表
        """
        db = getdb()

        try:
            for video in video_data:
                # 检查URL是否已经处理过
                if video['video_url'] in self.processed_urls:
                    logging.info(f"URL已经处理过，跳过: {video['video_url']}")
                    continue

                try:
                    dy_res = asyncio.run(hybridCrawler.hybrid_parsing_single_video(
                        url=video['video_url'], 
                        minimal=False
                    ))
                    
                    # 检查是否包含anchor_info
                    if not dy_res or 'anchor_info' not in dy_res:
                        logging.info(f"视频不包含anchor_info，跳过保存: {video['video_url']}")
                        self._save_processed_url(video['video_url'])  # 仍然记录已处理
                        continue

                    sql = """
                    INSERT INTO transport_job 
                    (dwn_url, state, platform, remark, create_time) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    state = VALUES(state),
                    update_time = NOW()
                    """

                    db.execute(sql, (
                        video['video_url'],
                        0,
                        'douyin',
                        '短剧',
                        datetime.now()
                    ))

                    # 保存已处理的URL
                    self._save_processed_url(video['video_url'])

                except Exception as e:
                    logging.error(f"保存视频数据失败: {str(e)}, URL: {video['video_url']}")
                    continue
        except Exception as e:
            logging.error(f"数据库操作失败: {str(e)}")
            db.rollback()
            raise e


async def juliang_setup(account_file, handle=False):
    if not os.path.exists(account_file) or not await cookie_auth(account_file):
        if not handle:
            # Todo alert message
            return False
        logging.info('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        await douyin_cookie_gen(account_file)
    return True


async def cookie_auth(account_file):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=account_file)
        context = await set_init_script(context)
        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto("https://business.oceanengine.com/account/page/service/account/security/level")
        try:
            await page.wait_for_url("https://business.oceanengine.com/account/page/service/account/security/level",
                                    timeout=5000)
        except:
            print("[+] 等待5秒 cookie 失效")
            await context.close()
            await browser.close()
            return False
        # 2024.06.17 抖音创作者中心改版
        if await page.get_by_text('手机号登录').count():
            print("[+] 等待5秒 cookie 失效")
            return False
        else:
            print("[+] cookie 有效")
            return True


async def douyin_cookie_gen(account_file):
    async with async_playwright() as playwright:
        options = {
            'headless': False
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options)
        # Setup context however you like.
        context = await browser.new_context()  # Pass any options
        context = await set_init_script(context)
        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.goto("https://open.douyin.com/platform/oauth/connect?response_type=code&client_key=aw7tduvjdk1a0x3r&scope=mobile%2Cuser_info%2Cvideo.create%2Cvideo.data&redirect_uri=https%3A%2F%2Fbusiness.oceanengine.com%2Flogin%3FappKey%3D51%26from%3Dhttps%253A%252F%252Fbusiness.oceanengine.com%252Faccount%252Fpage%252Fservice%252Faccount%252Fsecurity%252Flevel&state=douyin_sso")
        login_url = page.url
        # await page.pause()
        start_time = time.time()
        while True:
            if login_url == page.url:
                await asyncio.sleep(0.5)
            else:
                break
            elapsed_time = time.time() - start_time
            # 检查是否超过了超时时间
            if elapsed_time > 120:
                raise TimeoutError("操作超时，跳出循环")
        # await page.goto("https://business.oceanengine.com/account/page/service/account/security/level")
        user_id = await get_user_id(page)
        # 点击调试器的继续，保存cookie
        await context.storage_state(path=get_account_file(user_id))
        await context.close()
        await browser.close()
        return user_id


async def get_user_id(page):
    start_time = time.time()  # 获取开始时间
    while True:
        user_id = await page.locator('[class="user-id"]:has-text("ID: ")').text_content()
        user_id = user_id.replace("ID: ", "").strip()
        if user_id == '0':
            current_time = time.time()  # 获取当前时间
            elapsed_time = current_time - start_time  # 计算已经过去的时间
            if elapsed_time > 10:  # 如果已经过去的时间超过5秒
                break  # 退出循环
        else:
            break  # 退出循环
    return user_id
