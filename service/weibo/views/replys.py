from Crawler.utils.error_code import ErrorCode
from Crawler.utils.reply import reply
from ..models import accounts
from Crawler.lib.logger import logger
from ..logic import request_replys
import random

async def replys(id: str, comment_id: str, offset: int = 0, limit: int = 20):
    """
    获取微博评论回复
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_replys(id, comment_id, account.get('cookie', ''), offset, limit)
        if res == {} or not succ:
            logger.error(f'get replys failed, account: {account_id}, id: {id}, comment_id: {comment_id}, offset: {offset}, limit: {limit}, res: {res}')
            continue
        logger.info(f'get replys success, account: {account_id}, id: {id}, comment_id: {comment_id}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get replys failed, id: {id}, comment_id: {comment_id}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')