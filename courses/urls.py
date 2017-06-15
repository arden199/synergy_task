from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'),
    url(r'^create/user$', views.UserCreateView.as_view(), name='user_create'),
    url(r'^update/(?P<pk>[0-9]+)/user$', views.UserUpdateView.as_view(), name='user_update'),
    url(r'^delete/(?P<pk>[0-9]+)/user$', views.UserDeleteView.as_view(), name='user_delete'),
    url(r'^courses/$', views.CoursesListView.as_view(), name='courses_list')

]
