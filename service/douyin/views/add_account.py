from Crawler.utils.error_code import ErrorCode
from Crawler.utils.reply import reply
from social_auto_upload.utils.base_social_media import SOCIAL_MEDIA_DOUYIN
from ..models import accounts
from Crawler.lib.logger import logger
from pydantic import BaseModel

class Param(BaseModel):
    shop_user_id: str | None = None
    cookie: str | None = None
    creator_id: str | None = None
    id: int | None = None
    pub_count: int | None = None
    keywords: str | None = None

async def add_account(param: Param):
    '''
    添加抖音账号
    '''
    if param.shop_user_id == '' and param.creator_id == '':
        logger.error(f'id or cookie is empty, id: {param.id}, cookie: {param.cookie}')
        return reply(ErrorCode.PARAMETER_ERROR, "id and cookie is required")
    await accounts.save(cookie=param.cookie, expired=0, creator_id=param.creator_id, shop_user_id=param.shop_user_id)
    logger.info(f'douyin add account, id: {param.id}, cookie: {param.cookie}')
    return reply()