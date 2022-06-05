from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from oauth2_provider.models import (
    AbstractApplication,
    AbstractGrant,
    AbstractIDToken,
    AbstractAccessToken,
    AbstractRefreshToken
    ) 
from oauth2_provider.models import generate_client_secret

class OauthGrantModel(AbstractGrant):
    class Meta:
        swappable = "OAUTH2_PROVIDER_GRANT_MODEL"
        db_table = "oauthGrant"
        verbose_name = u'oauthGrant'
        verbose_name_plural = verbose_name        

class OauthApplicationModel(AbstractApplication):
    class Meta:
        swappable = "OAUTH2_PROVIDER_APPLICATION_MODEL"
        db_table = "oauthApplication"
        verbose_name = u'oauth应用信息表'
        verbose_name_plural = verbose_name
        

    CLIENT_CONFIDENTIAL = "private"
    CLIENT_PUBLIC = "public"
    CLIENT_TYPES = (
        (CLIENT_CONFIDENTIAL, _("私人")),
        (CLIENT_PUBLIC, _("公开")),
    )

    GRANT_AUTHORIZATION_CODE = "authorization-code"
    GRANT_IMPLICIT = "implicit"
    GRANT_PASSWORD = "password"
    GRANT_CLIENT_CREDENTIALS = "client-credentials"
    GRANT_OPENID_HYBRID = "openid-hybrid"
    GRANT_TYPES = (
        (GRANT_AUTHORIZATION_CODE, _("授权码")),
        (GRANT_IMPLICIT, _("Implicit")),
        (GRANT_PASSWORD, _("账号密码")),
        (GRANT_CLIENT_CREDENTIALS, _("Client credentials")),
        (GRANT_OPENID_HYBRID, _("OpenID connect hybrid")),
    )
    
    authorization_grant_type = models.CharField(max_length=32, choices=GRANT_TYPES)
    client_secret_src = models.CharField(
        max_length=255,
        blank=True,
        default=generate_client_secret,
        db_index=True,
        help_text=_("secret src code before hash"),
    )

class AccessTokenModel(AbstractAccessToken):
    class Meta(AbstractAccessToken.Meta):
        swappable = "OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL"
        db_table = "oauthAccessToken"
        verbose_name = u'oauthAccessToken'
        verbose_name_plural = verbose_name    
    


class RefreshTokenModel(AbstractRefreshToken):
    """
    extend the AccessToken model with the external introspection server response
    """
    class Meta(AbstractRefreshToken.Meta):
        swappable = "OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL"
        db_table = "oauthRefreshToken"
        verbose_name = u'oauthRefreshToken'
        verbose_name_plural = verbose_name  

class IDTokenModel(AbstractIDToken):
    """
    extend the AccessToken model with the external introspection server response
    """
    class Meta(AbstractIDToken.Meta):
        swappable = "OAUTH2_PROVIDER_ID_TOKEN_MODEL"
        db_table = "oauthIDToken"
        verbose_name = u'oauthIDToken'
        verbose_name_plural = verbose_name  


# class 
