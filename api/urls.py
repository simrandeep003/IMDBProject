from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
  url(r'^movies/$', views.MovieList.as_view()),
  url(r'^movies/(?P<pk>[0-9]+)/$', views.MovieDetail.as_view()),
  url(r'^search$', views.MovieSearch.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)