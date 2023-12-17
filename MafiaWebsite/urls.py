"""
URL configuration for MafiaWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainpage.views import home, register, login_view
from django.contrib.auth import views as auth_views
from mainpage import views
from allauth.account.views import confirm_email
from GameRoom import views as GameRoom
from game import views as Game
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('accounts/', include('allauth.urls')),

    # Aizmirsu paroli
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/',
         views.reset_password, name='reset_password'),

    # verifikacija epasta
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    # GameRoom
    path('menu/', GameRoom.menu, name='menu'),
    path('game-room/', include('GameRoom.urls', namespace='GameRoom')),
    path('logout/', GameRoom.logout_view, name='logout'),
    path('game/', include('game.urls', namespace='game')),

]
urlpatterns += staticfiles_urlpatterns()


handler404 = views.handler404
handler500 = views.handler500