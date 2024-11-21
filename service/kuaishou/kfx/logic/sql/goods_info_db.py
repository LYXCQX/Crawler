from contextlib import asynccontextmanager, closing
import time
import sqlite3
import aiosqlite

from MediaCrawler.tools.utils import logger


class SqliteStore:
    def __init__(self, db_path):
        self.db_path = db_path

    @asynccontextmanager
    async def _get_connection(self):
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            yield conn

    def _get_sync_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

class GoodsInfoStore(SqliteStore):
    def __init__(self, store_path):
        super().__init__(store_path)
        self.primary_key = 'id'
        self.table_name = 'goods_info'
        self._create_table()

    def _create_table(self):
        with closing(self._get_sync_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'''
                CREATE TABLE IF NOT EXISTS goods_info (
                    {self.primary_key} INTEGER PRIMARY KEY AUTOINCREMENT,
                    lUserId VARCHAR(2048) NOT NULL,
                    status INTEGER DEFAULT 0,
                    activityProfitAmount VARCHAR(50),
                    logisticsId INTEGER,
                    distributeItemId VARCHAR(50),
                    itemDisplayStatus INTEGER,
                    activityBeginTime INTEGER,
                    itemTagDto TEXT,
                    ska INTEGER,
                    bestCommissionType INTEGER,
                    commissionType INTEGER,
                    saleVolumeThirtyDays INTEGER,
                    freeShipment INTEGER,
                    sampleStatus INTEGER,
                    activityId INTEGER,
                    distributeType INTEGER,
                    showPopupStatusDesc TEXT,
                    relItemId INTEGER,
                    couponAmount TEXT,
                    sellerId INTEGER,
                    rankNum INTEGER,
                    bestCommissionId INTEGER,
                    commissionId INTEGER,
                    salesVolume INTEGER,
                    activityStatus INTEGER,
                    shareDisabled INTEGER,
                    goodRateCnt7d INTEGER,
                    webLogParam TEXT,
                    ext TEXT,
                    freeSample INTEGER,
                    hasDistributePlan INTEGER,
                    itemTag TEXT,
                    itemDisplayReason TEXT,
                    titleTagDto TEXT,
                    crossBoarder INTEGER,
                    promoterCount INTEGER,
                    rankInfo TEXT,
                    relVideo TEXT,
                    chosenItemTag TEXT,
                    activityEndTime INTEGER,
                    sourceType INTEGER,
                    soldCountThirtyDays INTEGER,
                    brandId INTEGER,
                    itemLinkUrl TEXT,
                    sAGoods INTEGER,
                    fsTeam INTEGER,
                    reservePrice TEXT,
                    commissionRate TEXT,
                    sellPoint TEXT,
                    itemTitle TEXT,
                    profitAmount TEXT,
                    recoReason TEXT,
                    investmentActivityStatus INTEGER,
                    itemTagAttr TEXT,
                    itemChannel INTEGER,
                    sellerName TEXT,
                    exposureWeightType INTEGER,
                    tagText TEXT,
                    zkFinalPrice TEXT,
                    coverMd5 TEXT,
                    relLive  TEXT,
                    serverExpTag TEXT,
                    secondActivityId INTEGER,
                    titleHeadIcon TEXT,
                    stepCommissionInfo TEXT,
                    waistCoverShowInfo TEXT,
                    itemImgUrl TEXT,
                    channelId INTEGER,
                    shelfItemStatus INTEGER,
                    couponRemainCount INTEGER,
                    hasRecoReason INTEGER,
                    activityCommissionRate TEXT,
                    isAdd INTEGER,
                    soldCountYesterday INTEGER,
                    investmentActivityId INTEGER,
                    showPopupStatusType INTEGER,
                    isStepCommission INTEGER,
                    itemData TEXT,
                    isHealthCategory INTEGER,
                    linkType INTEGER,
                    activityType INTEGER,
                    categoryId INTEGER,
                    categoryName TEXT,
                    salesVolumeDesc TEXT,
                    keywords TEXT,
                    ct DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
                    ut DATETIME
                )
                '''
                cursor.execute(sql)
                
                # 创建更新触发器
                trigger_sql = f'''
                CREATE TRIGGER IF NOT EXISTS update_goods_timestamp 
                AFTER UPDATE ON {self.table_name}
                FOR EACH ROW
                BEGIN
                    UPDATE {self.table_name} SET ut = CURRENT_TIMESTAMP
                    WHERE {self.primary_key} = NEW.{self.primary_key} AND 
                    (
                        NEW.status != OLD.status OR 
                        NEW.salesVolume != OLD.salesVolume OR 
                        NEW.saleVolumeThirtyDays != OLD.saleVolumeThirtyDays OR
                        NEW.itemTitle != OLD.itemTitle OR
                        NEW.zkFinalPrice != OLD.zkFinalPrice OR
                        NEW.itemDisplayStatus != OLD.itemDisplayStatus OR
                        NEW.keywords != OLD.keywords
                    );
                END;
                '''
                cursor.execute(trigger_sql)
                conn.commit()
            except Exception as e:
                logger.error(f'创建商品信息表失败, error: {e}')

    async def save(self, goods_data: dict) -> bool:
        async with self._get_connection() as conn:
            try:
                if 'id' in goods_data:
                    del goods_data['id']
                
                columns = ', '.join(goods_data.keys())
                placeholders = ', '.join(['?' for _ in goods_data])
                sql = f'INSERT OR REPLACE INTO {self.table_name} ({columns}) VALUES ({placeholders})'
                await conn.execute(sql, tuple(goods_data.values()))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'保存商品信息失败, error: {e}')
                await conn.rollback()
                return False

    async def batch_save(self, goods_list: list) -> bool:
        async with self._get_connection() as conn:
            try:
                for goods in goods_list:
                    if 'id' in goods:
                        del goods['id']
                    
                    columns = ', '.join(goods.keys())
                    placeholders = ', '.join(['?' for _ in goods])
                    sql = f'INSERT OR REPLACE INTO {self.table_name} ({columns}) VALUES ({placeholders})'
                    await conn.execute(sql, tuple(goods.values()))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'批量保存商品信息失败, error: {e}')
                await conn.rollback()
                return False

    async def get_by_id(self, id: int) -> dict:
        async with self._get_connection() as conn:
            try:
                sql = f'SELECT * FROM {self.table_name} WHERE id = ?'
                cursor = await conn.execute(sql, (id,))
                result = await cursor.fetchone()
                return dict(result) if result else {}
            except Exception as e:
                logger.error(f'查询商品信息失败, error: {e}')
                return {}

    async def query_by_lUserId(self, lUserId: int, date: str = None) -> list:
        async with self._get_connection() as conn:
            try:
                if date:
                    sql = f'''
                        SELECT *  FROM {self.table_name} 
                        WHERE lUserId = ? 
                        AND date(ct) >= date(?)
                    '''
                    cursor = await conn.execute(sql, (lUserId, date))
                else:
                    sql = f'SELECT * FROM {self.table_name} WHERE lUserId = ?'
                    cursor = await conn.execute(sql, (lUserId,))
                
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'按用户ID查询商品信息失败, error: {e}')
                return []

    async def query_by_price_range(self, min_price: float, max_price: float) -> list:
        async with self._get_connection() as conn:
            try:
                sql = f'SELECT * FROM {self.table_name} WHERE CAST(zk_final_price AS FLOAT) BETWEEN ? AND ?'
                cursor = await conn.execute(sql, (min_price, max_price))
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'按价格范围查询商品信息失败, error: {e}')
                return []

    async def delete_by_id(self, id: int) -> bool:
        async with self._get_connection() as conn:
            try:
                sql = f'DELETE FROM {self.table_name} WHERE id = ?'
                await conn.execute(sql, (id,))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'删除商品信息失败, error: {e}')
                await conn.rollback()
                return False

    async def update_sales_info(self, id: int, sales_volume: int, 
                              sale_volume_thirty_days: int) -> bool:
        async with self._get_connection() as conn:
            try:
                # ut会通过触发器自动更新
                sql = f'''UPDATE {self.table_name} 
                         SET sales_volume = ?, sale_volume_thirty_days = ?
                         WHERE id = ?'''
                await conn.execute(sql, (sales_volume, sale_volume_thirty_days, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'更新商品销售信息失败, error: {e}')
                await conn.rollback()
                return False

    async def update_status(self, id: int, status: int) -> bool:
        async with self._get_connection() as conn:
            try:
                # ut会通过触发器自动更新
                sql = f'''UPDATE {self.table_name} 
                         SET status = ?
                         WHERE id = ?'''
                await conn.execute(sql, (status, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'更新商品状态失败, error: {e}')
                await conn.rollback()
                return False

    async def query_by_status(self, status: int, limit: int = 100, offset: int = 0) -> list:
        async with self._get_connection() as conn:
            try:
                sql = f'SELECT * FROM {self.table_name} WHERE status = ? LIMIT ? OFFSET ?'
                cursor = await conn.execute(sql, (status, limit, offset))
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'按状态查询商品信息失败, error: {e}')
                return []

    async def query_by_keywords(self, keywords: str) -> list:
        async with self._get_connection() as conn:
            try:
                sql = f'''SELECT * FROM {self.table_name} 
                         WHERE keywords LIKE ? OR item_title LIKE ?'''
                search_pattern = f'%{keywords}%'
                cursor = await conn.execute(sql, (search_pattern, search_pattern))
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'按关键字查询商品信息失败, error: {e}')
                return []

    async def get_keywords_statistics(self, date: str = None, lUserId: str = None) -> dict:
        """
        统计商品标题和关键词中的词频
        Args:
            date: 指定日期，格式为'YYYY-MM-DD'，默认为None表示所有日期
            lUserId: 用户ID，默认为None表示所有用户
        Returns:
            dict: 关键词统计结果，格式为 {keyword: count}
        """
        async with self._get_connection() as conn:
            try:
                # 构建查询条件
                conditions = []
                params = []
                
                if date:
                    conditions.append("date(ct) = date(?)")
                    params.append(date)
                
                if lUserId:
                    conditions.append("lUserId = ?")
                    params.append(lUserId)
                
                where_clause = f"WHERE word != '' {' AND ' + ' AND '.join(conditions) if conditions else ''}"
                
                sql = f'''
                WITH split_keywords AS (
                    SELECT word
                    FROM {self.table_name},
                         json_each(
                             '["' || replace(
                                 replace(
                                     coalesce(keywords, '') || ' ' || coalesce(item_title, ''),
                                     ' ', '","'
                                 ),
                                 '，', '","'
                             ) || '"]'
                         ) AS words(word)
                    {where_clause}
                )
                SELECT word as keyword, COUNT(*) as count 
                FROM split_keywords 
                GROUP BY word 
                ORDER BY count DESC
                '''
                
                cursor = await conn.execute(sql, params)
                results = await cursor.fetchall()
                return {row['keyword']: row['count'] for row in results}
            except Exception as e:
                logger.error(f'统计关键词失败, error: {e}')
                return {}