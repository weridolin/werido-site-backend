'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 02:00:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 11:12:26
'''

# from rest_framework import urlpatterns
from drug.views import DrugWordsViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("words",DrugWordsViewSet,basename="words")
urlpatterns = router.urls