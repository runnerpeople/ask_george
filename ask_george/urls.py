"""ask_george URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from ask_app import views as ask_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hot/(?P<page>\d+)?$',ask_views.base,{"sort": "hot"}, name="hot_questions"),
    url(r'^tag/(?P<tag>[a-zA-Z0-9]+)/(?P<page>\d+)?$',ask_views.base, name="tag"),
    url(r'^question/(?P<question_id>\d+)/?$',ask_views.question, name="question"),
    url(r'^ask/?',ask_views.ask, name="ask"),
    url(r'^login/?',ask_views.login, name="login"),
    url(r'^signup/?',ask_views.sign_up, name='signup'),

    url(r'^parse/', ask_views.parse_args, name='parse'),
    url(r'^(/)?(?P<page>\d+)?$', ask_views.base, name="home"),
]
