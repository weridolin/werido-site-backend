from rest_framework import routers
from covid19.v1.apis import CovidApis

router = routers.SimpleRouter(trailing_slash=True)
router.register("info",CovidApis,basename="covid19")

urlpatterns = [
]
urlpatterns += router.urls
