# ------------------------------------------主题end------------------------------------------
# {"orderType":6,"channelId":13,"itemTagCode":["kfx_activity_tag_kfxksyx"],"pcursor":0}
# {"orderType":4,"channelId":13,"itemTagCode":["kfx_activity_tag_kfxksyx"],"pcursor":0}
# {"orderType":0,"channelId":13,"itemTagCode":["kfx_activity_tag_kfxksyx"],"pcursor":0}
# {"orderType":0,"channelId":"商品类目","keyWord":"搜索关键字","itemTagCode":["商品属性"],"priceStart":"券后价开始","priceEnd":"券后价结束","rateStart":"佣金范围开始","rateEnd":"佣金范围结束","soldCountStart":"销量开始","soldCountEnd":"销量结束","requestType":"1_1","pcursor":0}
# 选品中心首页实体
class GoodsInfoHomeReq:
    def __init__(self,  **kwargs):
        # 初始化商品信息请求类
        self.order_type = kwargs.get('order_type')  # 订单类型
        self.channel_id = kwargs.get('channel_id')  # 商品类目ID
        self.key_word = kwargs.get('key_word')  # 搜索关键字
        self.item_tag_code = kwargs.get('item_tag_code')  # 商品属性标签代码
        self.price_start = kwargs.get('price_start')  # 券后价开始
        self.price_end = kwargs.get('price_end')  # 券后价结束
        self.rate_start = kwargs.get('rate_start')  # 佣金比率范围开始
        self.rate_end = kwargs.get('rate_end')  # 佣金比率范围结束
        self.sold_count_start = kwargs.get('sold_count_start')  # 销量开始
        self.sold_count_end = kwargs.get('sold_count_end')  # 销量结束
        self.request_type = kwargs.get('request_type')  # 请求类型
        self.pcursor = kwargs.get('pcursor')  # 游标
        self.theme_id = kwargs.get('theme_id')
        self.sub_theme_id = kwargs.get('sub_theme_id')
    def to_dict(self):
        # 将对象转换为字典，去除无用的值
        result = {
            "orderType": self.order_type,
            "channelId": self.channel_id,
            "keyWord": self.key_word,
            "itemTagCode": self.item_tag_code,
            "priceStart": self.price_start,
            "priceEnd": self.price_end,
            "rateStart": self.rate_start,
            "rateEnd": self.rate_end,
            "soldCountStart": self.sold_count_start,
            "soldCountEnd": self.sold_count_end,
            "requestType": self.request_type,
            "pcursor": self.pcursor
        }
        return {k: v for k, v in result.items() if v is not None}


# 爆款榜单排行榜
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":2,"categoryId":105774}  
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":1,"categoryId":105774}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":3,"categoryId":105774}
# {"resourceId":1,"unitId":2,"positionId":2,"tagId":3,"categoryId":105777}
class HotRankingReq:
    def __init__(self, tag_id, category_id):
        self.resource_id = 1
        self.unit_id = 2
        self.position_id = 2
        self.tag_id = tag_id
        self.category_id = category_id
    def to_dict(self):
        # 将对象转换为字典，去除无用的值
        result = {
            "resourceId": self.resource_id,
            "unitId": self.unit_id,
            "positionId": self.position_id,
            "tagId": self.tag_id,
            "categoryId": self.category_id
        }
        return {k: v for k, v in result.items() if v is not None}


# {"orderType":6,"keyWord":"牛奶","themeId":473,"subThemeId":473001,"pcursor":0}
# {"orderType":0,"keyWord":"","themeId":473,"subThemeId":473002,"pcursor":0}
# {"orderType":0,"keyWord":"","themeId":473,"subThemeId":473003,"pcursor":0}
# {"orderType":0,"keyWord":"","themeId":104,"subThemeId":104002,"pcursor":0}
# {"orderType":0,"keyWord":"","themeId":104,"subThemeId":104001,"pcursor":0}
# {"orderType":6,"keyWord":"","themeId":103,"subThemeId":103001,"pcursor":0}
# {"orderType":0,"keyWord":"","themeId":535,"subThemeId":535004,"pcursor":0}
# 主题商品请求实体
class ThemeGoodsReq:
        
    def __init__(self, theme_id, sub_theme_id,order_type, key_word, pcursor):
        self.theme_id = theme_id  # 主题ID
        self.sub_theme_id = sub_theme_id  # 子主题ID
        self.order_type = order_type  # 排序类型
        self.key_word = key_word  # 搜索关键字
        self.pcursor = pcursor  # 游标
    def to_dict(self):
        # 将对象转换为字典
        result = {
            "themeId": self.theme_id,
            "subThemeId": self.sub_theme_id,
            "orderType": self.order_type,
            "keyWord": self.key_word,
            "pcursor": self.pcursor
        }
        return {k: v for k, v in result.items() if v is not None}
