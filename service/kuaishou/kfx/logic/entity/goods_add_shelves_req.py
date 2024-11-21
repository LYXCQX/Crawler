from dataclasses import dataclass
from typing import Dict, Any
import uuid  # 添加uuid模块导入

from pydantic import BaseModel

from Crawler.service.kuaishou.kfx.logic.Enum.goods_emnu import QueryType


# {"distributeItemId":787530242698,"relItemId":23226210435698,"activityId":0,"saveType":"add","isReplace":0,"bizCode":"pcShelfItemSelection",
# "statisticsInfo":{"pageUrl":"https://cps.kwaixiaodian.com/pc/promoter/selection-center/home"
# ,"refer":"https://cps.kwaixiaodian.com/pc/promoter/selection-center/home","appName":"PC","terminal":"PC","commissionId":1548176832698
# ,"commissionType":6,"ext":{"matchId":"f29df65a-e172-411a-b27c-5e0a670f27ec"}}}
@dataclass
class StatisticsInfo:
    """统计信息实体类"""
    ext: Dict[str, Any]  # 扩展信息，包含业务代码、场景等额外信息
    pageUrl: str = "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home"  # 页面URL
    refer: str = "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home"  # 来源页面URL
    appName: str = 'PC'  # 应用名称，如 'PC'
    terminal: str = 'PC'  # 终端类型，如 'PC'
    commissionId: int = 0  # 佣金ID
    commissionType: int = 6  # 佣金类型

    def __init__(self,
                 pageUrl: str,
                 commissionId: int = 0,
                 commissionType: int = 6,
                 ext: Dict[str, Any] = None):
        if ext and ext.get('matchId') is None:
            ext['matchId'] = str(uuid.uuid4())  # 生成新的UUID
        self.pageUrl = pageUrl
        self.commissionId = commissionId
        self.commissionType = commissionType
        self.ext = ext

    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典格式"""
        return {
            'ext': self.ext,
            'pageUrl': self.pageUrl,
            'refer': self.refer,
            'appName': self.appName,
            'terminal': self.terminal,
            'commissionId': self.commissionId,
            'commissionType': self.commissionType
        }


@dataclass
class GoodsAddShelvesReq:
    """快手小店商品上架请求实体类"""
    distributeItemId: int  # 分销商品ID
    relItemId: int  # 关联商品ID
    activityId: int  # 活动ID
    secondActivityId: int  # 二级活动ID
    statisticsInfo: StatisticsInfo  # 统计息对象
    saveType: str = 'add'  # 保存类型，如 'add' 表示新增
    isReplace: int = 0  # 是否替换，0表示不替换
    bizCode: str = 'pcShelfItemSelection'  # 业务代码，如 'pcShelfItemSelection'

    def __init__(self,
                 distributeItemId: int,
                 relItemId: int,
                 activityId: int = 0,
                 secondActivityId: int = 0,
                 saveType: str = 'add',
                 isReplace: int = 0,
                 bizCode: str = 'pcShelfItemSelection',
                 statisticsInfo: StatisticsInfo = None):
        self.distributeItemId = distributeItemId
        self.relItemId = relItemId
        self.activityId = activityId
        self.secondActivityId = secondActivityId
        self.saveType = saveType
        self.isReplace = isReplace
        self.bizCode = bizCode
        self.statisticsInfo = statisticsInfo

    @classmethod
    def from_other(cls, other: Any, query_type: QueryType) -> 'GoodsAddShelvesReq':
        """从其他对象创建实例，忽略不存在的属性"""
        data = {}
        for field in cls.__annotations__:
            if hasattr(other, field):
                data[field] = getattr(other, field)
            elif field == 'statisticsInfo':
                statisticsInfo = StatisticsInfo(
                    pageUrl=query_type.referer,
                    commissionId=getattr(other, 'bestCommissionId'),
                    commissionType=getattr(other, 'bestCommissionType'),
                    ext=getattr(other, 'ext')
                )
                data[field] = statisticsInfo
        # 使用 pydantic 的构造方法创建实例
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典格式"""
        return {
            'distributeItemId': self.distributeItemId,
            'relItemId': self.relItemId,
            'activityId': self.activityId,
            'secondActivityId': self.secondActivityId,
            'saveType': self.saveType,
            'isReplace': self.isReplace,
            'bizCode': self.bizCode,
            'statisticsInfo': self.statisticsInfo.to_dict() if self.statisticsInfo else None
        }
