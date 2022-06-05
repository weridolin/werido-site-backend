from django.apps import AppConfig


class OauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oauth'

    def ready(self) -> None:## django start 时会运行
        # 注册所有signals
        import oauth.v1.signals
        return super().ready(),