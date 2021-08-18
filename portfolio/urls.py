from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('profile/<int:id>/', views.display_user_profile_view, name='profile'),
    path('edit-profile/<int:id>/', views.edit_user_profile, name='edit_profile'),
    path('', views.sign_in, name='sign_in'),
    path('home/<int:id>/', views.home, name="home"),
    path('get-all-users/', views.get_users, name="get_all_users")
]