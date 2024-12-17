import logging
import os
import sys
import json

from dotenv import load_dotenv
from playwright.async_api import async_playwright
import asyncio
from pathlib import Path

from Crawler.service.douyin.logic.Enum.goods_emnu import get_cate_by_id
from Crawler.service.douyin.logic.entity.goods_info_req import env_filter_mapping
from Crawler.service.kuaishou.kfx.logic.entity.goods_req import GoodsInfoHomeReq
from social_auto_upload.conf import LOCAL_CHROME_PATH
# 获取当前文件所在目录的父目录（项目根目录）
from Crawler.service.douyin.views.buyin_login import get_account_file

load_dotenv()


async def set_init_script(context):
    stealth_js_path = Path("../social_auto_upload/utils/stealth.min.js")
    await context.add_init_script(path=stealth_js_path)
    return context


async def get_goods(user_id, playwright, req: GoodsInfoHomeReq, page, browser):
    response_data = None  # 添加变量存储响应数据
    response_received = asyncio.Event()  # 添加事件标志

    # 定义请求拦截处理函数
    async def handle_response(response):
        nonlocal response_data  # 使用nonlocal访问外部变量
        if "pc/selection/common/material_list" in response.url:
            try:
                # 获取请求信息
                request = response.request
                post_data = request.post_data  # 直接获取post_data属性
                if isinstance(post_data, str):
                    post_data = json.loads(post_data)
                if ((req.pcursor == 0 or post_data.get('cursor', '0') > req.pcursor)
                        and (not req.key_word or req.key_word == post_data.get('search_text', ''))):
                    req.pcursor = post_data.get('cursor', '0')  # 更新请求对象中的cursor
                    logging.info(f"获取商品信息{post_data.get('cursor')}")
                    data = await response.json()
                    response_data = data
                    response_received.set()  # 设置事件标志
            except Exception as e:
                logging.exception("响应解析失败", e)
    try:
        if not page:
            # 启动浏览器时添加更多配置
            browser = await playwright.chromium.launch(
                headless=False,
                executable_path=LOCAL_CHROME_PATH,  # 请替换为实际的Chrome路径
                args=['--start-maximized']
            )

            # 使用保存的登录状态
            context = await browser.new_context(
                storage_state=get_account_file(user_id),
                no_viewport=True
            )

            # 设置初始化脚本
            context = await set_init_script(context)
            page = await context.new_page()

            # 访问目标页面
            await page.goto("https://buyin.jinritemai.com/dashboard/merch-picking-library")
            if req.key_word:
                print(f'赋值word{req.key_word}')
                await page.fill('.auxo-input', req.key_word)
                print(f'赋值word{req.key_word} end')
            for env_key, env_entity in env_filter_mapping.items():
                if os.getenv(env_key):
                    mendel_cid_lists = eval(os.getenv(env_key))
                    for i, mendel_cid_list in enumerate(mendel_cid_lists):
                        if env_key == 'MendelCid':
                            goods_category = env_entity.get_parent_tree(mendel_cid_list)
                        else:
                            goods_category = get_cate_by_id(env_entity, mendel_cid_list)
                        # 递归处理分类树
                        await process_category(goods_category, page, env_key)
            await context.storage_state(path=get_account_file(user_id))
        page.on("response", handle_response)
        print('点击搜索')
        await page.click('button:has-text("搜索")')
        print('点击搜索--end')

        # 等待响应数据
        try:
            await asyncio.wait_for(response_received.wait(), timeout=30)  # 设置10秒超时
        except asyncio.TimeoutError:
            logging.error("获取响应数据超时")
            return False, None, page, browser

        return True, response_data, page, browser
    finally:
        page.remove_listener("response", handle_response)



async def add_chat(page, title):
    try:
        # 首先获取定位器
        xpc_class = page.get_by_text(title).locator("..").locator("..").get_by_text('加选品车')
        # 尝试点击
        await xpc_class.click()
        
        # 等待文本变化，检查是否成功添加
        try:
            # 检查是否变为"已加选品车"
            success_text = page.get_by_text(title).locator("..").locator("..").get_by_text('已加选品车')
            await success_text.wait_for(timeout=5000)  # 等待5秒
            return True
        except Exception:
            # 检查是否出现"添加失败"
            try:
                fail_text = page.get_by_text("添加失败")
                await fail_text.wait_for(timeout=1000)  # 等待1秒
                return False
            except Exception:
                # 如果既没有成功也没有失败的提示，返回False
                return False
    except Exception as e:
        print(f"定位器查找或点击过程中出现错误: {str(e)}")
        raise e


async def process_category(category, page, env_key, level=0):
    menu_selector = category['category_selector']
    if env_key == 'MendelCid' or env_key == 'FeaturedItems':
        one_node_class = f".merch-filter-table div:text('{category['classify_name']}')"
        son_node_class = f"{menu_selector} li:text('%s')"
    else:
        one_node_class = f".merch-filter-table span:text('{category['classify_name']}')"
        son_node_class = f"{menu_selector} div:text('%s')"

    if level == 0:
        # 点击一级分类
        await page.click(one_node_class)
        if 'children' in category and category['children']:
            child = category['children'][0]
            await process_category(child, page, env_key, level + 1)
    else:
        # 等待级联菜单出现
        await page.wait_for_selector(menu_selector)
        if env_key == 'Price' or env_key == 'CosRatio':
            # 处理价格和佣金比例的输入
            cate_sub_value = category['classify_value'].replace('R:', '').split(',')
            min_value = cate_sub_value[0]
            max_value = cate_sub_value[1]
            if min_value:
                await page.fill(f'{menu_selector} input[placeholder^="最低"]', str(min_value))
            if max_value:
                await page.fill(f'{menu_selector} input[placeholder^="最高"]', str(max_value))
            # 点击确定按钮
            await page.click(f'{menu_selector} button:has-text("确定")')
        else:
            if 'children' in category and category['children']:
                # 有子节点 使用hover代替click来选中但不点击
                await page.hover(son_node_class % category['classify_name'])
                child = category['children'][0]
                await process_category(child, page, env_key, level + 1)
            else:
                # 没有子节点时，点击"不限"选项
                await page.click(son_node_class % category['classify_name'], force=True)


if __name__ == "__main__":
    with async_playwright() as playwright:
        query_success, response_data = asyncio.run(get_goods('account_id', playwright))
