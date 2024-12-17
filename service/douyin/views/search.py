from Crawler.utils.error_code import ErrorCode
from Crawler.utils.reply import reply
from ..models import accounts
from Crawler.lib.logger import logger
from ..logic import request_search
import random
import os
import asyncio
import time

def get_filter_params(keyword):
    """获取搜索过滤参数"""
    sort_type = os.getenv('DOUYIN_SEARCH_SORT_TYPE', '0')
    publish_time = os.getenv('DOUYIN_SEARCH_PUBLISH_TIME', '0')
    duration = os.getenv('DOUYIN_SEARCH_DURATION', '0')
    content_type = os.getenv('DOUYIN_SEARCH_CONTENT_TYPE', '0')
    
    filter_selected = {
        "sort_type": sort_type,
        "publish_time": publish_time
    }
    
    # 添加视频时长筛选
    if duration == '1':
        filter_selected["filter_duration"] = "0-1"
    elif duration == '2':
        filter_selected["filter_duration"] = "1-5"
    elif duration == '3':
        filter_selected["filter_duration"] = "0-5"
    
    # 添加内容形式筛选
    if content_type in ['1', '2']:
        filter_selected["content_type"] = content_type
    
    params = {
        'filter_selected': filter_selected,
        'search_source': 'tab_search',
        'is_filter_search': '1',
        'need_filter_settings': '1'
    }
    
    # 如果关键词不为空，添加到查询参数中
    if keyword:
        params['keyword'] = keyword
        
    return params

# 添加一个变量来记录上次调用时间
_last_search_time = 0

async def search(keyword: str, offset: int = 0, limit: int = 10)->reply:
    """
    获取视频搜索，每次调用需间隔10秒
    """
    global _last_search_time
    
    # 检查时间间隔
    current_time = time.time()
    time_diff = current_time - _last_search_time
    if time_diff < 10:
        # 如果间隔小于10秒，则等待剩余时间
        await asyncio.sleep(10 - time_diff)
    
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    
    search_params = get_filter_params(keyword)
    account = _accounts[0]
    if account.get('expired', 0) == 1:
        return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')
    
    account_id = account.get('id', '')
    res, succ = await request_search(
        account.get('cookie', ''), 
        offset, 
        limit,
        search_params
    )
    
    # 更新最后调用时间
    _last_search_time = time.time()
    
    if res == {} or not succ:
        logger.error(f'search failed, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.SEARCH_FAILED, '搜索失败')    
    logger.info(f'search success, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
    return reply(ErrorCode.OK, '成功', res)