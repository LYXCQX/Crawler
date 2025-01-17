from .common import common_request

async def request_search(cookie: str, offset: int = 0, limit: int = 10,req_param=None) -> tuple[dict, bool]:
    """
    请求抖音获取搜索信息
    """
    params = { "search_channel": 'aweme_general', "search_source": 'normal_search',
              "query_correct_type": '1', "enable_history": '1',"list_type": 'single',"pc_libra_divert": 'Windows',"is_filter_search": '0', 'offset': offset, 'count': limit}

    headers = {"cookie": cookie}
    params.update(req_param)
    resp, succ = await common_request('/aweme/v1/web/general/search/single/', params, headers)
    if not succ:
        return resp, succ
    return resp, succ

async def leaderboard(cookie: str,req_param=None) -> tuple[dict, bool]:
    """
    请求抖音选品热门榜单
    rank_type榜单类型  pay_prod_qty_cnt 爆款榜   pay_author_cnt热推榜  incr_pay_prod_qty_cnt趋势榜  last常销榜
    cos_ratio佣金比率 10 20 30 50
    date_type时间 realtime实时  1d昨日  7d一周  30d一月
    genre_type载体  all不限载体  video短视频  live直播   window橱窗
    """
    params = { "rank_type": 'pay_author_cnt', "industry_id": 'all',
               "prod_mesh": 'all', "date_type": '1d',"genre_type": 'video',"cos_ratio": '10',"alli_cate_id": 'all', 'is_flagship': 0}

    headers = {"cookie": cookie}
    params.update(req_param)
    resp, succ = await common_request('https://buyin.jinritemai.com/pc/leaderboard/center/pmt', params, headers)
    if not succ:
        return resp, succ
    return resp, succ

# ?rank_type=pay_prod_qty_cnt&industry_id=all&prod_mesh=all&date_type=30d&
# genre_type=video&cos_ratio=10&alli_cate_id=all&is_flagship=0&verifyFp=verify_m4znze7z_ZCDQUmlR_34qG_4yib_89Vn_qqgJXIFLgV8H&fp=verify_m4znze7z_ZCDQUmlR_34qG_4yib_89Vn_qqgJXIFLgV8H&msToken=6Btb_YofIl0YqbqmIANVx5lPA7SOxzXwH7PmmUTkDSGgZ5DxFh2SATTwGYuzt1epnBrnivX3X2a5zGcUVBBNu8ujQARqDEovHXV8Us5j5_B4h5CZZNRrqLevsFMhBaLzLaY2g4047VOt--yLQ_4aX8bODHtKP0KLSodPJwq_ZEky&a_bogus=Ef0VkwyEdd%2FnepeS8KYiS6dl686lrsWyzsi2bSlP9ou6bHFPUdpOkOCnboFyUabu2mBHkLpHHnFlijdcPnshZorpLmpDuuvRD4QInU0o8qZ4GPiZI3SMebGEFi4TWSGPKQ2tEri1I0lLZ2QfZHOhlqK97AtE-Km8zqaSpPWl7x2B6-vY9doSePZm

async def request_search_goods(headers: dict,req_param=None) -> tuple[dict, bool]:
    """
    请求抖音获取搜索信息
    """
    headers.update(headers)
    resp, succ = await common_request('https://buyin.jinritemai.com/pc/selection/common/material_list', req_param, headers)
    if not succ:
        return resp, succ
    ret = resp.get('data', {})
    return ret, succ
