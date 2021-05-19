from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('songs/', views.songs, name='songs'),
    path('songs/<int:id>', views.songpost, name='songs'),
    path('login',views.login , name = 'login'),
    path('signup',views.signup, name = 'signup'), 
    path('Watchlater',views.watchlater,name = 'Watchlater'),
    path('logout_user',views.logout_user,name = 'logout_user'),
    path('history',views.history,name='history'),
]