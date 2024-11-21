from enum import Enum
from Crawler.lib.logger import logger
from Crawler.lib import requests

HOST = 'https://cps.kwaixiaodian.com'
# https://cps.kwaixiaodian.com/gateway/distribute/match/selection/home/query/theme/item/list
COMMON_HEADERS = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6",
    "content-type": "application/json",
    "kpf": "PC_WEB",
    "kpn": "",
    "Origin": "https://cps.kwaixiaodian.com",
    "Referer": "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home",
    "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Trace-Id": "1.0.0.1731492933529.16",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

}

GRAPHQL_DIR = '../Crawler/service/kuaishou/kfx/logic/graphql/'


class GraphqlQuery(Enum):
    SEARCH = 'search'
    GOODS_INFO = 'goods_info'
    COMMENTS = 'comments'
    REPLYS = 'replys'
    PROFILE = 'profile'
    PROFILE_PHOTO = 'profile_photo'


GRAPHQL_FILES = {
    GraphqlQuery.SEARCH: 'search_query.graphql',
    GraphqlQuery.GOODS_INFO: 'goods_info.graphql',
    GraphqlQuery.COMMENTS: 'comment_list.graphql',
    GraphqlQuery.REPLYS: 'replys.graphql',
    GraphqlQuery.PROFILE: 'profile.graphql',
    GraphqlQuery.PROFILE_PHOTO: 'profile_photo.graphql'
}

graphql = {}
for type, file in GRAPHQL_FILES.items():
    with open(str(GRAPHQL_DIR + file), 'r') as f:
        graphql_queries = f.read()
        graphql[type] = graphql_queries


def load_graphql_queries(type: GraphqlQuery) -> str:
    return graphql.get(type)


async def common_request(data: dict, headers: dict, url: str) -> tuple[dict, bool]:
    """
    请求 kuaishou
    :param url:
    :param data: 请求参数
    :param headers: 请求头
    :return: 返回数据和是否成功
    """
    headers.update(COMMON_HEADERS)
    logger.info(
        f'url: {url}, request {url}, body={data}, headers={headers}')
    response = await requests.post(url, headers, json=data)
    logger.info(
        f'url: {url}, body: {data}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, body: {data}, request error, code: {response.status_code}, body: {response.text}')
        return {}, False

    return response.json(), True
