class UserPermission:

    @staticmethod
    def permission_key(user,uuid):
        return f"rbac.{user.id}_{uuid}"


class WECHAT:

    @staticmethod
    def access_token_key():
        return f"wechat.public.access_token"

    @staticmethod
    def chatGpt_time_remain(wechat_id):
        """
            chatGpt剩余时间
        """
        return f"wechat.public.chatGPTModeTimeRemain.{wechat_id}"

    @staticmethod
    def chatGpt_result(wechat_id):
        """
            存放最近一次chatGpt查询结果
        """
        return f"wechat.public.chatGptResult.{wechat_id}"

    @staticmethod
    def chatGpt_request_num(wechat_id):
        """
            chatgpt模式下第几次回调
        """
        return f"wechat.public.chatGptResult.{wechat_id}"


class Weather:
    
    @staticmethod
    def get_weather_key():
        return f"weather.total"
    
    @staticmethod
    def get_city_weather_key(city_id=None):
        return f"weather.city.{city_id}"


