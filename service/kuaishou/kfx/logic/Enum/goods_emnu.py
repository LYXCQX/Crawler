# 主页 https://cps.kwaixiaodian.com/gateway/distribute/match/selection/home/query/item/list
# 快分销爆款榜 https://cps.kwaixiaodian.com/gateway/distribute/match/selection/home/query/pc/rank/item/list
# 主题商品列表 https://cps.kwaixiaodian.com/gateway/distribute/match/selection/home/query/theme/item/list
# 小店统计数据 https://syt.kwaixiaodian.com/zones/data_flow/shortvideo
# 短视频榜单 https://syt.kwaixiaodian.com/zones/short-video/list
# 货架商品 https://syt.kwaixiaodian.com/zones/shop/goods-management
# 商品榜单 https://syt.kwaixiaodian.com/zones/rankingList/productRanking
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":1,"categoryId":0}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":2,"categoryId":0}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":3,"categoryId":0}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":3,"categoryId":105774}
from enum import Enum


# 商品类目
class Channel(Enum):
    HOME = (99, "首页")
    MOTHER_BABY_TOYS = (13, "母婴玩具")
    DIGITAL_APPLIANCES = (4, "数码家电")
    HOUSEHOLD_GOODS = (9, "家居百货")
    SPORTS_OUTDOORS = (10, "运动户外")
    FOOD_BEVERAGES = (3, "食品饮料")
    WOMEN_CLOTHING_SHOES = (1, "女装女鞋")
    BEAUTY_SKINCARE = (118, "美妆护肤")
    PERSONAL_CARE_CLEANING = (6, "个护清洁")
    MEDICAL_HEALTH = (114, "医疗保健")
    TEA_WINE_FRESH = (116, "茶酒生鲜")
    MEN_CLOTHING_SHOES = (8, "男装男鞋")
    JEWELRY_ACCESSORIES = (120, "珠宝配饰")

    def __init__(self, channel_id, channel_name):
        self.channel_id = channel_id
        self.channel_name = channel_name

    @classmethod
    def get_by_id(cls, channel_id):
        for channel in cls:
            if channel.value[0] == channel_id:
                return channel
        return None

    @classmethod
    def get_by_name(cls, channel_name):
        for channel in cls:
            if channel.value[1] == channel_name:
                return channel
        return None


# 排序方式
class SortType(Enum):
    COMPREHENSIVE_SORT = (0, 0, "综合排序")
    SALES = (1, 6, "销量")
    COMMISSION_RATE = (1, 4, "佣金率")
    LISTING_PEOPLE = (1, 7, "上架达人数")

    def __init__(self, order_val, order_type, order_name):
        self.order_val = order_val
        self.order_type = order_type
        self.order_name = order_name

    @classmethod
    def get_by_order_type(cls, order_type):
        for order in cls:
            if order.order_type == order_type:
                return order
        return None

    @classmethod
    def get_by_order_name(cls, order_name):
        for order in cls:
            if order.order_name == order_name:
                return order
        return None


# 商品属性
class Tag(Enum):
    KFX_ACTIVITY_TAG_KFXKSYX = ("kfx_activity_tag_kfxksyx", "快手优选")
    DISTRIBUTE_BRAND_ITEM = ("distribute_brand_item", "品牌")
    DISTRIBUTE_SAMPLE_RULE = ("distribute_sample_rule", "买样后返")
    DISTRIBUTE_TRUST_BUY = ("distribute_trust_buy", "信任购")
    DISTRIBUTE_FREE_SHIP = ("distribute_free_ship", "包邮")
    DISTRIBUTE_RETURN_BACK_FREIGHT = ("distribute_return_back_freight", "退货补运费")
    DISTRIBUTE_FAKE_ONE_PAY_N = ("distribute_fake_one_pay_n", "假一赔十")
    DISTRIBUTE_SEND_ENSURE = ("distribute_send_ensure", "发货保障")
    DISTRIBUTE_GOOD_COMMENT_MUCH = ("distribute_good_comment_much", "好评多")

    def __init__(self, tag_code, tag_desc):
        self.tag_code = tag_code
        self.tag_desc = tag_desc

    @classmethod
    def get_by_tag_code(cls, tag_code):
        for tag in cls:
            if tag.tag_code == tag_code:
                return tag
        return None

    @classmethod
    def get_by_tag_desc(cls, tag_desc):
        for tag in cls:
            if tag.tag_desc == tag_desc:
                return tag
        return None


# 查询类型
class QueryType(Enum):
    KEYWORD_COLLECTION = (1, "关键词采集", "根据关键字采集商品", "https://cps.kwaixiaodian.com",
                          "/gateway/distribute/match/selection/home/query/item/list",
                          "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home")
    SHELF_COLLECTION = (
    2, "货架采集", "采集自己的货架商品", "https://syt.kwaixiaodian.com", "/rest/business/gateway/shop/ite",
    "https://syt.kwaixiaodian.com/rest/business/gateway/shop/ite")
    CUSTOM_PRODUCT_ID = (3, "自定义商品ID", "根据商品ID采集商品", "https://cps.kwaixiaodian.com",
                         "/gateway/distribute/match/selection/home/query/item/list",
                         "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home")
    CATEGORY_COLLECTION = (4, "商品类目采集", "根据商品类目采集商品", "https://cps.kwaixiaodian.com",
                           "/gateway/distribute/match/selection/home/query/item/list",
                           "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home")
    HOT_SELLING_LIST = (5, "热销榜单", "快分销爆款榜 分销热卖排行 跟卖就爆单", "https://cps.kwaixiaodian.com",
                        "/gateway/distribute/match/selection/home/query/pc/rank/item/list",
                        "https://cps.kwaixiaodian.com/pc/promoter/selection-center/hot-rank")
    SEASONAL_HOT_SALE = (6, "分销严选", "当季热卖 好价格好机制", "https://cps.kwaixiaodian.com",
                         "/gateway/distribute/match/selection/home/query/theme/item/list",
                         "https://cps.kwaixiaodian.com/pc/promoter/selection-center/theme-landing?themeId=473&themeTitle=%E5%88%86%E9%94%80%E4%B8%A5%E9%80%89")
    LOW_PRICE_FIRST_CHOICE = (7, "开单好物", "低至9.9 引流开单首选", "https://cps.kwaixiaodian.com",
                              "/gateway/distribute/match/selection/home/query/theme/item/list",
                              "https://cps.kwaixiaodian.com/pc/promoter/selection-center/theme-landing?themeId=104&themeTitle=%E5%BF%AB%E5%88%86%E9%94%80%E5%BC%80%E5%8D%95%E5%88%A9%E5%99%A8")
    HIGH_COMMISSION_GOODS = (8, "高佣优品", "佣金25%起 带货高收益", "https://cps.kwaixiaodian.com",
                             "/gateway/distribute/match/selection/home/query/theme/item/list",
                             "https://cps.kwaixiaodian.com/pc/promoter/selection-center/theme-landing?themeId=103&themeTitle=%E9%AB%98%E4%BD%A3%E4%BC%98%E9%80%89")
    SHORT_VIDEO_HOT_SALE = (9, "短视频热卖", "看同行找灵感 选货更简单", "https://cps.kwaixiaodian.com",
                            "/gateway/distribute/match/selection/home/query/theme/item/list",
                            "https://cps.kwaixiaodian.com/pc/promoter/selection-center/theme-landing?themeId=535&themeTitle=%E7%9F%AD%E8%A7%86%E9%A2%91")
    ALL_PRODUCTS = (10, "全部商品", "全部商品", "https://cps.kwaixiaodian.com",
                    "/gateway/distribute/match/selection/home/query/item/list",
                    "https://cps.kwaixiaodian.com/pc/promoter/selection-center/home")

    def __init__(self, type, title, sub_title, host, uri, referer):
        self.type = type
        self.title = title
        self.sub_title = sub_title
        self.host = host
        self.uri = uri
        self.referer = referer

    @classmethod
    def get_by_type(cls, type):
        for theme in cls:
            if theme.type == type:
                return theme
        return None

    @classmethod
    def get_by_sub_title(cls, sub_title):
        for theme in cls:
            if theme.sub_title == sub_title:
                return theme
        return None

    @classmethod
    def get_by_title(cls, title):
        for theme in cls:
            if theme.title == title:
                return theme
        return None

    @classmethod
    def get_by_jump_url(cls, jump_url):
        for theme in cls:
            if theme.jump_url == jump_url:
                return theme
        return None


# ------------------------------------------爆款榜单start------------------------------------------
# 爆款榜单商品类目
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":1,"categoryId":0}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":2,"categoryId":0}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":3,"categoryId":0}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":3,"categoryId":105774}
class HotSellingCategory(Enum):
    TOTAL_LIST = ("总榜", 0, 50740)
    FOOD_BEVERAGES = ("食品酒水", 105774, 10941)
    HOUSEHOLD_DAILY = ("家居日百", 105775, 12427)
    BEAUTY_PERSONAL_CARE = ("美妆个护", 105777, 6483)
    WOMEN_CLOTHING_SHOES = ("女装女鞋", 105853, 4339)
    MEN_CLOTHING_SHOES = ("男装男鞋", 105854, 1768)
    MOTHER_BABY_PETS = ("母婴花宠", 105778, 5137)
    SPORTS_OUTDOORS = ("运动户外", 105855, 2544)
    DIGITAL_APPLIANCES = ("数码家电", 105779, 1663)
    JEWELRY_ACCESSORIES = ("珠宝配饰", 105856, 1726)

    def __init__(self, category_name, category_id, item_count):
        self.category_name = category_name
        self.category_id = category_id
        self.item_count = item_count

    @classmethod
    def get_by_category_name(cls, category_name):
        for category in cls:
            if category.category_name == category_name:
                return category
        return None

    @classmethod
    def get_by_category_id(cls, category_id):
        for category in cls:
            if category.category_id == category_id:
                return category
        return None

    @classmethod
    def get_by_item_count(cls, item_count):
        for category in cls:
            if category.item_count == item_count:
                return category
        return None


# 爆款榜单类型
class RankingType(Enum):
    DAILY = (1, "日榜")
    WEEKLY = (2, "周榜")
    MONTHLY = (3, "月榜")

    def __init__(self, ranking_id, ranking_name):
        self.ranking_id = ranking_id
        self.ranking_name = ranking_name

    @classmethod
    def get_by_ranking_id(cls, ranking_id):
        for ranking in cls:
            if ranking.ranking_id == ranking_id:
                return ranking
        return None

    @classmethod
    def get_by_ranking_name(cls, ranking_name):
        for ranking in cls:
            if ranking.ranking_name == ranking_name:
                return ranking
        return None


# ------------------------------------------爆款榜单end------------------------------------------


# ------------------------------------------主题start------------------------------------------
class SubTheme(Enum):
    FOOD_FRESH = (473, 473001, "食品生鲜")
    HOUSEHOLD_APPLIANCES = (473, 473002, "百货家电")
    BEAUTY_PERSONAL_CARE = (473, 473003, "美妆个护")
    CLOTHING_ACCESSORIES = (473, 473004, "服装配饰")
    MOTHER_BABY_TOYS = (473, 473005, "母婴玩具")
    NINE_NINE_CAP = (104, 104001, "9.9封顶")
    NINETEEN_NINE_CAP = (104, 104002, "19.9封顶")
    HIGH_COMMISSION_SELECTION = (103, 103001, "高佣优选")
    HOT_SELLING = (535, 535001, "热卖爆款")
    FOOD_BEVERAGE = (535, 535002, "食品饮料")
    HOUSEHOLD_DAILY = (535, 535003, "家居日百")
    BEAUTY_PERSONAL_CARE_VIDEO = (535, 535004, "美妆个护")
    CLOTHING_SHOES = (535, 535005, "服饰鞋靴")

    def __init__(self, theme_id, sub_theme_id, sub_theme_title):
        self.theme_id = theme_id
        self.sub_theme_id = sub_theme_id
        self.sub_theme_title = sub_theme_title

    @classmethod
    def get_by_theme_id(cls, theme_id):
        for sub_theme in cls:
            if sub_theme.theme_id == theme_id:
                return sub_theme
        return None

    @classmethod
    def get_by_sub_theme_id(cls, sub_theme_id):
        for sub_theme in cls:
            if sub_theme.sub_theme_id == sub_theme_id:
                return sub_theme
        return None

    @classmethod
    def get_by_sub_theme_title(cls, sub_theme_title):
        for sub_theme in cls:
            if sub_theme.sub_theme_title == sub_theme_title:
                return sub_theme
        return None
