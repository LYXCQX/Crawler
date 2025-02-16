from pathlib import Path

from Crawler.data.driver import CommonAccount

# 获取项目根目录
def get_project_root() -> Path:
    current = Path(__file__).resolve()
    while current.name != 'YouDub-webui':
        current = current.parent
    return current

BASE_DIR = get_project_root()
accounts = CommonAccount(BASE_DIR/"data/douyin/sql_lab/douyin.db")