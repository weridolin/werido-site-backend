class UserPermission:

    @staticmethod
    def permission_key(user,uuid):
        return f"rbac.{user.id}_{uuid}"


class WECHAT:

    @staticmethod
    def access_token_key():
        return f"wechat.public.access_token"


class Weather:
    
    @staticmethod
    def get_weather_key():
        return f"weather.total"
    
    @staticmethod
    def get_city_weather_key(city_id=None):
        return f"weather.city.{city_id}"

