from Crawler.data.driver import CommonAccount
from Crawler.service.kuaishou.kfx.logic.sql.goods_info_db import GoodsInfoStore

accounts = CommonAccount("../data/kuaishou/sql_lab/kuaishou_kfx.db")
goods_db = GoodsInfoStore("../data/kuaishou/sql_lab/kuaishou_kfx.db")
