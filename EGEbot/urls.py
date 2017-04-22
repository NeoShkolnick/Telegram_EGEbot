from django.conf.urls import include, url
from .views import CommandReceiveView
urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view()),
]