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
    url(r'^/?', ask_views.base,name="home"),
    url(r'^hot/$',ask_views.base,{"sort": "hot"},name="hot_questions"),
    url(r'^tag/(?P<tag>[a-z,0-9]+)/$',ask_views.base,{"tags_name":"tag"},name="tag"),
    url(r'^parse/', ask_views.parse_args, name='parse'),
]
