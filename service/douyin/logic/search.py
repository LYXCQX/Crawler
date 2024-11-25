from .common import common_request

async def request_search(cookie: str, offset: int = 0, limit: int = 10,req_param=None) -> tuple[dict, bool]:
    """
    请求抖音获取搜索信息
    """
    params = { "search_channel": 'aweme_general', "search_source": 'normal_search',
              "query_correct_type": '1', "is_filter_search": '0', 'offset': offset, 'count': limit}
    headers = {"cookie": cookie}
    params.update(req_param)
    resp, succ = await common_request('/aweme/v1/web/general/search/single/', params, headers)
    if not succ:
        return resp, succ
    ret = resp.get('data', {})
    return ret, succ
