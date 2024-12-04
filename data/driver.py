import traceback
from contextlib import asynccontextmanager, closing
from Crawler.lib.logger import logger
import time
import sqlite3
import aiosqlite

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

class CommonAccount(SqliteStore):
    def __init__(self, store_path):
        super().__init__(store_path)
        self.primary_key = 'id'
        self.table_name = 'account'
        self._create_table()

    def _create_table(self):
        with closing(self._get_sync_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.primary_key} INTEGER PRIMARY KEY AUTOINCREMENT,
                    cookie VARCHAR(2048) NOT NULL,
                    expired INTEGER DEFAULT 0,
                    creator_id VARCHAR(50) DEFAULT NULL,
                    shop_user_id VARCHAR(50) DEFAULT NULL,
                    pub_count INTEGER DEFAULT 100,
                    keywords text DEFAULT '玩具,女孩玩具,男孩玩具,玩具枪,学习玩具,儿童车,布娃娃,益智,水枪,乐高,毛绒玩具,公仔,玩具车,魔方,医生玩具,积木,发条玩具,积木桌',
                    ct INTEGER NOT NULL,
                    ut INTEGER NOT NULL
                )
                '''
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error(f'failed to create table, error: {e}')

    async def save(self,  cookie: str, expired: int, creator_id: str = None, shop_user_id: str = None, pub_count: str = None, keywords: str = None) -> bool:
        ct = ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                if creator_id or shop_user_id:
                    update_fields = ['cookie = ?', 'expired = ?', 'ut = ?']
                    params = [cookie, expired, ut]

                    if creator_id is not None:
                        update_fields.append('creator_id = ?')
                        params.append(creator_id)
                    if shop_user_id is not None:
                        update_fields.append('shop_user_id = ?')
                        params.append(shop_user_id)
                    if pub_count is not None:
                        update_fields.append('pub_count = ?')
                        params.append(pub_count)
                    if keywords is not None:
                        update_fields.append('keywords = ?')
                        params.append(keywords)

                    update_sql = f'UPDATE {self.table_name} SET {", ".join(update_fields)} WHERE 1=1'
                    if creator_id is not None:
                        update_sql += ' and creator_id = ?'
                        params.append(creator_id)
                    if shop_user_id is not None:
                        update_sql += ' and shop_user_id = ?'
                        params.append(shop_user_id)
                    await conn.execute(update_sql, params)
                
                if conn.total_changes == 0:
                    insert_fields = ['cookie', 'expired', 'ct', 'ut']
                    insert_values = ['?'] * 5
                    insert_params = [cookie, expired, ct, ut]
                    
                    if creator_id is not None:
                        insert_fields.append('creator_id')
                        insert_values.append('?')
                        insert_params.append(creator_id)
                    if shop_user_id is not None:
                        insert_fields.append('shop_user_id')
                        insert_values.append('?')
                        insert_params.append(shop_user_id)
                    if pub_count is not None:
                        insert_fields.append('pub_count')
                        insert_values.append('?')
                        insert_params.append(pub_count)
                    if keywords is not None:
                        insert_fields.append('keywords')
                        insert_values.append('?')
                        insert_params.append(keywords)
                    
                    insert_sql = f'INSERT INTO {self.table_name} ({", ".join(insert_fields)}) VALUES ({", ".join(insert_values)})'
                    await conn.execute(insert_sql, insert_params)
                
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save cookies, error: {e}')
                await conn.rollback()
                traceback.print_exc()
                return False

    async def load(self, offset: int = 0, limit: int = 0) -> list:
        async with self._get_connection() as conn:
            try:
                if limit == 0:
                    sql = f'SELECT * FROM {self.table_name}'
                    cursor = await conn.execute(sql)
                else:
                    sql = f'SELECT * FROM {self.table_name} LIMIT ? OFFSET ?'
                    cursor = await conn.execute(sql, (limit, offset))
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'failed to load cookies, error: {e}')
                await conn.rollback()
                return []

    async def expire(self, id: str) -> bool:
        ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET expired = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (1, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save cookies, error: {e}')
                await conn.rollback()
                return False

class Proxies(SqliteStore):
    def __init__(self, store_path):
        super().__init__(store_path)
        self.primary_key = 'id'
        self.table_name = 'proxies'
        self._create_table()

    def _create_table(self):
        with closing(self._get_sync_connection()) as conn, closing(conn.cursor()) as cursor:
            try:
                sql = f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.primary_key} INTEGER PRIMARY KEY AUTOINCREMENT,
                    url VARCHAR(512) NOT NULL,
                    enable INTEGER NOT NULL,
                    ct INTEGER NOT NULL,
                    ut INTEGER NOT NULL
                )
                '''
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error(f'failed to create table, error: {e}')

    async def save(self, url: str = '', enable: int = 1, id: int = 0) -> bool:
        ct = ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET url = ?, enable = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (url, enable, ut, id))
                if conn.total_changes == 0:
                    sql = f'INSERT INTO {self.table_name} (url, enable, ct, ut) VALUES (?, ?, ?, ?)'
                    await conn.execute(sql, (url, enable, ct, ut))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save proxy, error: {e}')
                await conn.rollback()
                return False
            
    async def remove(self, id: int) -> bool:
        async with self._get_connection() as conn:
            try:
                sql = f'DELETE FROM {self.table_name} WHERE id = ?'
                await conn.execute(sql, (id,))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to remove proxy, error: {e}')
                await conn.rollback()
                return False 

    async def load(self, enable: int = -1, offset: int = 0, limit: int = 0) -> list:
        async with self._get_connection() as conn:
            try:
                base_sql = f'SELECT * FROM {self.table_name}'
                params = []

                if enable != -1:
                    base_sql += ' WHERE enable = ?'
                    params.append(enable)

                if limit > 0:
                    base_sql += ' LIMIT ? OFFSET ?'
                    params.extend([limit, offset])

                cursor = await conn.execute(base_sql, params)
                results = await cursor.fetchall()
                return [dict(row) for row in results]
            except Exception as e:
                logger.error(f'failed to load proxies, error: {e}')
                await conn.rollback()
                return []


    async def enable(self, id: int) -> bool:
        ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET enable = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (1, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save proxies, error: {e}')
                await conn.rollback()
                return False

    async def disable(self, id: int) -> bool:
        ut = int(time.time())
        async with self._get_connection() as conn:
            try:
                sql = f'UPDATE {self.table_name} SET enable = ?, ut = ? WHERE id = ?'
                await conn.execute(sql, (0, ut, id))
                await conn.commit()
                return True
            except Exception as e:
                logger.error(f'failed to save proxies, error: {e}')
                await conn.rollback()
                return False