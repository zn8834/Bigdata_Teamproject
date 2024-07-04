"""
URL configuration for TeamProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from App01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base),
    path('home/', views.home),    
    path('main/', views.main, name='main'),
    path('main02/', views.main02, name='main02'),
    path('main03/', views.main03, name='main03'),
    path('map/', views.naver_api),  # Added trailing slash for consistency
    path('icons/', views.icons_view, name='icons'),
    path('icons02/', views.icons02_view, name='icons02'),
    
    path('write_form/', views.write_form, name='write_form'),
    path('insert/',views.insert),
    path('list/', views.list),
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('recommendation/', views.recommend_district_view, name='recommend_district'),
]