from Crawler.utils.error_code import ErrorCode
from Crawler.utils.reply import reply
from ..models import accounts
from Crawler.lib.logger import logger
from ..logic import request_search
import random
import os

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

async def search(keyword: str, offset: int = 0, limit: int = 10)->reply:
    """
    获取视频搜索
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    
    search_params = get_filter_params(keyword)
    
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_search(
            account.get('cookie', ''), 
            offset, 
            limit,
            search_params
        )
        if res == {} or not succ:
            logger.error(f'search failed, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
            continue
        logger.info(f'search success, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功', res)
    
    logger.warning(f'search failed, keyword: {keyword}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')