from Crawler.utils.error_code import ErrorCode
from Crawler.utils.reply import reply
from ..models import accounts

async def account_list():
    '''
    获取快手账号
    '''
    return reply(ErrorCode.OK, "OK", await accounts.load())