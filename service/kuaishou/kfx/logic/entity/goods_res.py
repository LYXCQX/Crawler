from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict


class ItemTagDto(BaseModel):
    tagCode: Optional[str] = None  # 标签代码
    tagDesc: Optional[str] = None  # 标签描述
    tagValue: Optional[str] = None  # 标签值
    fireFlag: Optional[bool] = None  # 是否热门标志


class TitleTagDto(BaseModel):
    tagCode: Optional[str] = None  # 标签代码
    tagDesc: Optional[str] = None  # 标签描述
    tagImgUrl: Optional[str] = None  # 标签图片URL


class RecoReason(BaseModel):
    name: Optional[str] = None  # 推荐理由名称
    desc: Optional[str] = None  # 推荐理由描述


class Ext(BaseModel):
    bizCode: Optional[str] = None  # 业务代码
    scene: Optional[str] = None  # 场景
    itemSellerName: Optional[str] = None  # 商家名称
    dailyCommission: Optional[str] = None  # 日常佣金
    activityOrderNum: Optional[str] = None  # 活动订单数量
    isHotSale: Optional[str] = None  # 是否热销
    promoterHeadIconList: Optional[str] = None  # 推广者头像列表
    investmentActivityId: Optional[str] = None  # 投资活动ID
    investmentActivityStatus: Optional[str] = None  # 投资活动状态


class RankInfo(BaseModel):
    rankText: Optional[str] = None  # 排名文本
    rankNum: Optional[str] = None  # 排名数字
    rankLink: Optional[str] = None  # 排名链接
    tagId: Optional[int] = None  # 标签ID
    tagName: Optional[str] = None  # 标签名称
    categoryId: Optional[int] = None  # 类目ID
    categoryName: Optional[str] = None  # 类目名称


class RelLive(BaseModel):
    liveImg: Optional[str] = None  # 直播图片
    liveLink: Optional[str] = None  # 直播链接
    promoterId: Optional[int] = None  # 推广者ID
    promoterLogo: Optional[str] = None  # 推广者logo
    promoterName: Optional[str] = None  # 推广者名称


class RelVideo(BaseModel):
    nickname: Optional[str] = None  # 昵称
    imgUrl: Optional[str] = None  # 图片URL
    videoUrl: Optional[str] = None  # 视频URL
    viewCount: Optional[int] = None  # 观看次数
    headImg: Optional[str] = None  # 头像图片
    fansNum: Optional[int] = None  # 粉丝数量
    kwaiUrl: Optional[str] = None  # 快手链接
    displayTime: Optional[str] = None  # 显示时间
    caption: Optional[str] = None  # 视频标题


class StepCommissionInfo(BaseModel):
    stepNum: Optional[int] = None  # 阶梯数量
    beforeStepProfitAmount: Optional[str] = None  # 阶梯前利润金额
    beforeStepCommissionRate: Optional[str] = None  # 阶梯前佣金率
    afterStepProfitAmount: Optional[str] = None  # 阶梯后利润金额
    afterStepCommissionRate: Optional[str] = None  # 阶梯后佣金率
    startTime: Optional[int] = None  # 开始时间
    endTime: Optional[int] = None  # 结束时间


class WaistCoverShowInfo(BaseModel):
    waistName: Optional[str] = None  # 腰封名称
    waistImgUrl: Optional[str] = None  # 腰封图片URL
    discountPrice: Optional[str] = None  # 折扣价格
    discountDefaultText: Optional[str] = None  # 折扣默认文本
    discountBgColor: Optional[str] = None  # 折扣背景颜色
    themeUrl: Optional[str] = None  # 主题URL
    themeSceneId: Optional[int] = None  # 主题场景ID
    tagId: Optional[int] = None  # 标签ID


class SalesVolumeDesc(BaseModel):
    value: Optional[str] = None  # 销量值
    unit: Optional[str] = None  # 单位


class GoodsData(BaseModel):
    activityProfitAmount: Optional[str] = None  # 活动利润金额
    logisticsId: Optional[int] = None  # 物流ID
    itemDisplayStatus: Optional[int] = None  # 商品展示状态
    activityBeginTime: Optional[int] = None  # 活动开始时间
    itemTagDto: Optional[List[ItemTagDto]] = None  # 商品标签列表
    distributeItemId: Optional[int] = None  # 分销商品ID
    ska: Optional[int] = None  # SKU
    bestCommissionType: Optional[int] = None  # 最佳佣金类型
    commissionType: Optional[int] = None  # 佣金类型
    saleVolumeThirtyDays: Optional[int] = None  # 30天销量
    freeShipment: Optional[int] = None  # 是否包邮
    sampleStatus: Optional[int] = None  # 样品状态
    activityId: Optional[int] = None  # 活动ID
    distributeType: Optional[int] = None  # 分销类型
    showPopupStatusDesc: Optional[str] = None  # 弹窗状态描述
    relItemId: Optional[int] = None  # 关联商品ID
    couponAmount: Optional[str] = None  # 优惠券金额
    sellerId: Optional[int] = None  # 卖家ID
    rankNum: Optional[int] = None  # 排名
    bestCommissionId: Optional[int] = None  # 最佳佣金ID
    commissionId: Optional[int] = None  # 佣金ID
    salesVolume: Optional[int] = None  # 销量
    activityStatus: Optional[int] = None  # 活动状态
    shareDisabled: Optional[int] = None  # 是否禁用分享
    goodRateCnt7d: Optional[int] = None  # 7天好评数
    webLogParam: Optional[str] = None  # 网页日志参数
    ext: Dict[str, Any] = None  # 扩展信息
    freeSample: Optional[bool] = None  # 是否免费样品
    hasDistributePlan: Optional[bool] = None  # 是否有分销计划
    itemTag: Optional[List[Any]] = None  # 商品标签
    itemDisplayReason: Optional[str] = None  # 商品展示原因
    titleTagDto: Optional[List[TitleTagDto]] = None  # 标题标签列表
    crossBoarder: Optional[bool] = None  # 是否跨境
    promoterCount: Optional[int] = None  # 推广人数
    rankInfo: Optional[RankInfo] = None  # 排名信息
    chosenItemTag: Optional[str] = None  # 选择的商品标签
    activityEndTime: Optional[int] = None  # 活动结束时间
    sourceType: Optional[int] = None  # 来源类型
    soldCountThirtyDays: Optional[int] = None  # 30天销量
    brandId: Optional[int] = None  # 品牌ID
    itemLinkUrl: Optional[str] = None  # 商品链接URL
    sAGoods: Optional[bool] = None  # 是否为SA商品
    fsTeam: Optional[int] = None  # FS团队
    reservePrice: Optional[str] = None  # 保留价格
    commissionRate: Optional[str] = None  # 佣金率
    sellPoint: Optional[List[Any]]  # 卖点
    itemTitle: Optional[str]  # 商品标题
    profitAmount: Optional[str]  # 利润金额
    recoReason: Optional[List[RecoReason]]  # 推荐理由列表
    investmentActivityStatus: Optional[int]  # 投资活动状态
    itemTagAttr: Optional[Dict[str, Any]]  # 商品标签属性
    itemChannel: Optional[int]  # 商品渠道
    sellerName: Optional[str]  # 卖家名称
    exposureWeightType: Optional[int]  # 曝光权重类型
    tagText: Optional[str]  # 标签文本
    zkFinalPrice: Optional[str]  # 折扣最终价格
    coverMd5: Optional[str]  # 封面MD5
    serverExpTag: Optional[str]  # 服务器实验标签
    secondActivityId: Optional[int]  # 第二活动ID
    titleHeadIcon: Optional[List[str]] = None  # 标题头部图标
    itemImgUrl: Optional[str] = None  # 商品图片URL
    channelId: Optional[int] = None  # 渠道ID
    shelfItemStatus: Optional[int] = None  # 上架商品状态
    couponRemainCount: Optional[int] = None  # 优惠券剩余数量
    hasRecoReason: Optional[bool] = None  # 是否有推荐理由
    activityCommissionRate: Optional[str] = None  # 活动佣金率
    isAdd: Optional[int] = None  # 是否新增
    soldCountYesterday: Optional[int] = None  # 昨日销量
    investmentActivityId: Optional[int] = None  # 投资活动ID
    showPopupStatusType: Optional[int] = None  # 弹窗状态类型
    isStepCommission: Optional[bool] = None  # 是否阶梯佣金
    itemData: Optional[List[Any]] = None  # 商品数据
    isHealthCategory: Optional[bool] = None  # 是否健康类目
    linkType: Optional[int] = None  # 链接类型
    activityType: Optional[int] = None  # 活动类型
    categoryId: Optional[int] = None  # 类目ID
    categoryName: Optional[str] = None  # 类目名称
    relLive: Optional[RelLive] = None  # 关联直播信息
    relVideo: Optional[RelVideo] = None  # 关联视频信息
    stepCommissionInfo: Optional[StepCommissionInfo] = None  # 阶梯佣金信息
    waistCoverShowInfo: Optional[WaistCoverShowInfo] = None  # 腰封展示信息
    salesVolumeDesc: Optional[SalesVolumeDesc] = None  # 销量描述


class GoodsResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')  # 忽略模型中未定义的字段
    result: Optional[int] = None  # 结果
    data: Optional[List[GoodsData]] = None  # 商品数据列表
    requestId: Optional[str] = None  # 请求ID
    pcursor: Optional[str] = None  # 游标
    errorMsg: Optional[str] = None  # 错误信息
