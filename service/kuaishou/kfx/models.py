from Crawler.data.driver import CommonAccount
from Crawler.service.douyin.models import BASE_DIR
from Crawler.service.kuaishou.kfx.logic.sql.goods_info_db import GoodsInfoStore

accounts = CommonAccount(BASE_DIR/"data/kuaishou/sql_lab/kuaishou_kfx.db")
goods_db = GoodsInfoStore(BASE_DIR/"data/kuaishou/sql_lab/kuaishou_kfx.db")
