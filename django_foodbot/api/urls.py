'''API urls defined for views.''' 

from django.conf.urls import url, include, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from api import views



urlpatterns = [
    url(r'^menu/$', views.MenuList.as_view(),name ='menulist'),

]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
