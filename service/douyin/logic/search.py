from .common import common_request
from enum import Enum
import time

class XiguaChannel(Enum):
    """西瓜视频频道枚举
    包含频道ID和对应的中文说明
    """
    YINGSHI = ("94349546740", "影视")
    YOUXI = ("94349546935", "游戏")
    YINYUE = ("94349546885", "音乐")
    MEISHI = ("94349546920", "美食")
    NONGREN = ("94349546815", "农人")
    VLOG = ("94349546845", "VLOG")
    GAOXIAO = ("94349547030", "搞笑")
    CHONGWU = ("94349547025", "宠物")
    JUNSHI = ("94349546985", "军事")
    DONGCHEDI = ("94349547155", "懂车帝")
    TIYU = ("94349546840", "体育")
    YULE = ("94349547020", "娱乐")
    WENHUA = ("94349547175", "文化")
    SHOUGONG = ("94349547170", "手工")
    KEJI = ("94349547180", "科技")

    def __init__(self, channel_id: str, description: str):
        self.channel_id = channel_id
        self.description = description

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


async def request_xigua_search(cookie: str, channel: XiguaChannel = XiguaChannel.WENHUA, count: int = 9, query_count: int = 2, req_param=None) -> tuple[dict, bool]:
    """
    西瓜视频搜索
    Args:
        cookie: cookie字符串
        channel: 频道枚举，默认为文化频道
        count: 返回结果数量
        query_count: 查询次数，1为首次查询，2为加载更多
        req_param: 额外的请求参数
    Returns:
        tuple[dict, bool]: (响应数据, 是否成功)
    """
    # 如果queryCount为1则maxTime为0，否则使用当前时间戳
    max_time = 0 if query_count == 1 else int(time.time())
    
    params = {
        "channelId": channel.channel_id,
        "count": count,
        "maxTime": max_time,
        "request_from": "702",
        "queryCount": str(query_count),
        "offset": "0",
        "referrer": f"https://www.ixigua.com/channel/{channel.name.lower()}",
        "aid": "1768"
    }

    headers = {
        "cookie": cookie,
        "referer": "https://www.ixigua.com/"
    }
    
    if req_param:
        params.update(req_param)
        
    resp, succ = await common_request(
        'https://www.ixigua.com/api/feedv2/feedById', 
        params, 
        headers
    )
    if not succ:
        return resp, succ
    return resp, succ

async def main():
    """
    西瓜视频搜索示例
    """
    cookie = 'UIFID_V=2; UIFID_TEMP=630dc87f7218843564944b22829d362b9fabe9a9e3376a5c74988083749b66df450d5e38df4d8c77958e4dcfe023796bfb76be29e352e11fea6c796b80a65c6c35b620d4adc7a8605df29dcb0d3e8949; gfkadpd=1768,30523; _tea_utm_cache_1768={%22utm_source%22:%22xiguastudio%22}; _tea_utm_cache_2285={%22utm_source%22:%22xiguastudio%22}; fpk1=U2FsdGVkX1+wm7CKj7FndVElTuJUChEawKCWEKsLpJzW+aKA9aT088fZIAJfHY1m5CQID55gyecnyexhWSiOfQ==; fpk2=4f09e01c83d69100c363c33aecfef9f8; UIFID=630dc87f7218843564944b22829d362b9fabe9a9e3376a5c74988083749b66df85c403a70a2e3c144c34bc024db1fecac9556cb54c0cd8335e2bdfe9f232ebcf76a4e476f2f4aabc01a09f3d66afa90359afb54aad3ff166aa8d5e30f56129c0349eb55035d6aa9d018ff038769eb93b; __ac_signature=_02B4Z6wo00f01fEQXJQAAIDA-zaHPtiKBH3xMFgAABvh64; first_enter_player=%7B%22any_video%22%3A%222.14.7%22%7D; MONITOR_WEB_ID=8066a967-5e27-4988-b8d9-bb35fbe7bf61; s_v_web_id=verify_m6ln3w2a_dmRIgpOR_sUfi_4OdP_BtGq_noRQf2DTU9v5; support_webp=true; support_avif=true; csrf_session_id=901774a4c9db1f5fcd4321f072b75f75; passport_csrf_token=3034e4c792e16d878bda4f489c709abb; passport_csrf_token_default=3034e4c792e16d878bda4f489c709abb; odin_tt=6dab43e1f8a82cfc8b96c267316cbf6bbb3b3bccdfd5c3e5394ad1bdf9602ed8c40cb21911b788936774430a8f41cd5c76eeade7f2c55bfb791dabbb368feaf3; sid_guard=6acbee8eb916bc8f1a3bbf1cea0c3f3d%7C1738407823%7C5166358%7CWed%2C+02-Apr-2025+06%3A09%3A41+GMT; uid_tt=a52275a0c0240783cba4c8bd97d0b6c3; uid_tt_ss=a52275a0c0240783cba4c8bd97d0b6c3; sid_tt=6acbee8eb916bc8f1a3bbf1cea0c3f3d; sessionid=6acbee8eb916bc8f1a3bbf1cea0c3f3d; sessionid_ss=6acbee8eb916bc8f1a3bbf1cea0c3f3d; is_staff_user=false; sid_ucp_v1=1.0.0-KGQyYjYyNWY3MmJmYzJiOWQ3YzJjOTVmY2IwN2ZlMzNhYWM1MDBjNDQKGQijkuD4psyzBBCP__e8Bhj2FyAMOAZA9AcaAmxmIiA2YWNiZWU4ZWI5MTZiYzhmMWEzYmJmMWNlYTBjM2YzZA; ssid_ucp_v1=1.0.0-KGQyYjYyNWY3MmJmYzJiOWQ3YzJjOTVmY2IwN2ZlMzNhYWM1MDBjNDQKGQijkuD4psyzBBCP__e8Bhj2FyAMOAZA9AcaAmxmIiA2YWNiZWU4ZWI5MTZiYzhmMWEzYmJmMWNlYTBjM2YzZA; ttwid=1%7CYAPXG19xE3WmK1uV_LN0R2tbL7lEO23ToO_y6HpfIN4%7C1738408381%7Cb007abe04ba48ce54e9782594f6417094d3a8f5787bbea5ec5dc76cc2f1e233d; ixigua-a-s=3'  # 替换为实际的cookie
    
    # 示例1：获取文化频道的首页内容
    print("获取文化频道首页内容:")
    result, success = await request_xigua_search(
        cookie=cookie,
        channel=XiguaChannel.WENHUA,
        query_count=1  # 首次查询
    )
    if success:
        print(f"文化频道内容获取成功: {result}")
        return result, success
    else:
        print(f"文化频道内容获取失败: {result}")
        return result, success
