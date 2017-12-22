from django.conf.urls import url

from api.views import LoginAPIView, TestRequiredToken

urlpatterns = [
    url(r'^/login', LoginAPIView.as_view()),
    url(r'^/test', TestRequiredToken.as_view()),
]
