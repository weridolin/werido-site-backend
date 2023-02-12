from thirdApis.shortUrls.urls import short_urls
from thirdApis.apiCollector.urls import api_collector_urls
from thirdApis.chatGPT.urls import chatGPT_urls

urlpatterns = []
urlpatterns.extend(short_urls)
urlpatterns.extend(api_collector_urls)
urlpatterns.extend(chatGPT_urls)