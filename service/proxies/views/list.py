from Crawler.utils.error_code import ErrorCode
from Crawler.utils.reply import reply
from ..models import proxies
async def list():
    '''
    返回代理地址
    '''
    return reply(ErrorCode.OK, "OK", await proxies.load())