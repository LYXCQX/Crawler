from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import json

from Crawler.service.douyin.logic.Enum.goods_emnu import GoodsCategory, AllianceSales30d, BrowseCnt30d, \
    PromotionAuthorUcnt30d, Price, CosRatio, ExpScore, PositiveRate, Insurance, FeaturedItems


@dataclass
class Extra:
    new_session_strategy: str = "1"
    search_id: str = ""
    session_id: str = ""

    def __init__(self, new_session_strategy: str = "1", search_id: str = "", session_id: str = ""):
        self.new_session_strategy = new_session_strategy
        self.search_id = search_id
        self.session_id = session_id

    def to_dict(self) -> dict:
        return {
            "new_session_strategy": self.new_session_strategy,
            "search_id": self.search_id,
            "session_id": self.session_id
        }


@dataclass
class FilterValue:
    value: List[str]


@dataclass
class Filters:
    MendelCid: Optional[FilterValue] = None
    alliance_sales_30d: Optional[FilterValue] = None
    browse_cnt_30d: Optional[FilterValue] = None
    promotion_author_ucnt_30d: Optional[FilterValue] = None
    Price: Optional[FilterValue] = None
    CosRatio: Optional[FilterValue] = None
    ExpScore: Optional[FilterValue] = None
    PositiveRate: Optional[FilterValue] = None
    Insurance: Optional[FilterValue] = None
    FeaturedItems: Optional[FilterValue] = None

    def to_dict(self) -> Dict:
        """将Filters转换为字典，去除值为None的字段"""
        result = {}
        for field, value in asdict(self).items():
            if value is not None:
                result[field] = value
        return result


env_filter_mapping = {
    "MendelCid": GoodsCategory,
    "alliance_sales_30d": AllianceSales30d,
    "browse_cnt_30d": BrowseCnt30d,
    "promotion_author_ucnt_30d": PromotionAuthorUcnt30d,
    "Price": Price,
    "CosRatio": CosRatio,
    "ExpScore": ExpScore,
    "PositiveRate": PositiveRate,
    "Insurance": Insurance,
    "FeaturedItems": FeaturedItems
}


@dataclass
class GoodsInfoRequest:
    scene: str = "PCSquareFeed"
    size: int = 30
    search_text: str = ""
    cursor: int = 0
    extra: Extra = field(default_factory=Extra)
    filters: Filters = field(default_factory=Filters)

    def to_dict(self) -> Dict:
        """将请求实体转换为字典，过滤掉filters中的空值"""
        result = {
            "scene": self.scene,
            "size": self.size,
            "search_text": self.search_text,
            "cursor": self.cursor,
            "extra": asdict(self.extra)
        }

        filters_dict = self.filters.to_dict()
        if filters_dict:
            result["filters"] = filters_dict
        else:
            result["filters"] = {}
        return result

    @classmethod
    def from_env_config(cls, config: Dict):
        filters = Filters()

        for key, value in config.items():
            if hasattr(filters, key) and value:  # 只设置非空值
                setattr(filters, key, FilterValue(value))

        return cls(filters=filters)

    @classmethod
    def create_from_env(cls) -> 'GoodsInfoRequest':
        """从环境变量创建商品请求实体"""
        load_dotenv()

        config = {}
        for env_key, filter_key in env_filter_mapping.items():
            env_value = os.getenv(env_key)
            if env_value:
                try:
                    value = json.loads(env_value)
                    if value:  # 只添加非空值
                        config[env_key] = value
                except json.JSONDecodeError:
                    print(f"警告: 环境变量 {env_key} 的值格式不正确，应为JSON数组格式")
                    continue

        return cls.from_env_config(config)
