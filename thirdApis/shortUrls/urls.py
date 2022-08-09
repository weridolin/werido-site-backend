from django.urls import path,re_path
from thirdApis.shortUrls.apis import ShortUrlRecordApis,RedirectToRealUrl


short_urls = [
    path(r"/shortUrl/create/", ShortUrlRecordApis.as_view(), name="create-short-url"),
    path(r"/shortUrl/<str:short_number>/",RedirectToRealUrl.as_view(),name="redirect"),
    # re_path(r"^/token/$", TokenAccessViews.as_view(), name="token"),
    # re_path(r"^/revoke_token/$", RevokeTokenViews.as_view(), name="revoke-token"),
    # re_path(r"^/userInfo/$", UserInfoByOauthViews.as_view(), name="user-info"),    
]
