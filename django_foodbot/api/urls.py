'''API urls defined for views.'''

from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from api import views


urlpatterns = [
    url(r'^menu/$', views.MenuList.as_view(), name='menulist'),
    url(r'^rating/all/$', views.RatingList.as_view(), name='ratinglist'),
    url(r'^rating/week/$', views.WeeklyRatings.as_view(),
        name='weeklyratinglist'),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
