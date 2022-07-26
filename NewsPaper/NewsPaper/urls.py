"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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


urlpatterns = [
    path('admin/', admin.site.urls), # путь к панели администратора
    path('', include('newapp.urls')), # перенаправление корневой страницы в приложение newapp
    path('posts/', include('newapp.urls')), # делаем так, чтобы все адреса из нашего приложения (newapp/urls.py) сами автоматически подключались когда мы их добавим.

    path('accounts/', include('allauth.urls')), # accounts/signup/ and accounts/login/
#    path('posts/accounts/', include('allauth.urls'))
]
