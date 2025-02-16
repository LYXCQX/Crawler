from playwright.async_api import async_playwright
import asyncio
from pathlib import Path
import os

from Crawler.service.douyin.models import BASE_DIR


def get_account_file(user_id: str) -> str:
    """获取账号存储文件路径"""
    account_dir = BASE_DIR/"data/douyin/cookies/buyin"
    return str( f"{account_dir}/{user_id}.json")


async def set_init_script(context):
    """设置初始化脚本"""
    stealth_js_path = Path(BASE_DIR/"social_auto_upload/utils/stealth.min.js")
    await context.add_init_script(path=stealth_js_path)
    return context


async def login_with_qrcode():
    """使用二维码登录抖音"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )

        context = await browser.new_context(
            no_viewport=True
        )
        
        # 设置stealth.js
        context = await set_init_script(context)
        page = await context.new_page()

        # 访问新的登录页面
        await page.goto("https://buyin.jinritemai.com/mpa/account/login")
        
        try:
            # 等待并获取第一个iframe
            iframe_element = await page.wait_for_selector('iframe', timeout=10000)
            if not iframe_element:
                raise Exception("未找到iframe")
            
            iframe = await iframe_element.content_frame()
            if not iframe:
                raise Exception("无法切换到iframe")
            
            # 在iframe中等待二维码元素
            await iframe.wait_for_selector('.qr-image', timeout=10000)
            initial_url = page.url
            print("请使用抖音APP扫描二维码登录")
            
            # 等待URL变化来判断登录成功
            while True:
                current_url = page.url
                if current_url != initial_url:
                    break
                await asyncio.sleep(1)
            
            # 等待页面加载完成并确认URL
            while True:
                current_url = page.url
                if "buyin.jinritemai.com/dashboard?" in current_url:
                    print("登录成功！")
                    await page.goto('https://buyin.jinritemai.com/dashboard/merch-picking-library?pre_universal_page_params_id=&universal_page_params_id=b8b0e7d7-4186-4569-addd-a60b35271ac7')
                    break
                await asyncio.sleep(1)
            await page.hover('.btn-item-role-exchange__arrow')
            # 等待百应ID元素出现并获取内容
            buyin_id_element = page.locator('text=百应ID').locator("..").locator('.header-role-menu__item-number').first
            buyin_id = await buyin_id_element.text_content()
            print(f"百应ID: {buyin_id}")
            
            # 保存登录状态
            storage_path = get_account_file(buyin_id)
            await context.storage_state(path=storage_path)
            print(f"登录状态已保存到: {storage_path}")
            
            # 等待一会儿确保状态保存完成
            await page.wait_for_timeout(2000)
            return buyin_id
        except Exception as e:
            print(f"登录过程出错: {str(e)}")
        
        finally:
            await browser.close()


if __name__ == "__main__":
    # 这里替换为实际的用户ID
    asyncio.run(login_with_qrcode())
