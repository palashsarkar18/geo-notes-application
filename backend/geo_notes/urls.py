"""
URL configuration for geo_notes project.

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
from django.urls import path, include
from rest_framework.authtoken import views
from accounts.views import GetCSRFToken, LoginView, LogoutView, CreateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/register/', CreateUserView.as_view(), name='user-register'),
    path('api/accounts/login/', LoginView.as_view(), name='user-login'),
    path('api/accounts/logout/', LogoutView.as_view(), name='user-logout'),
    path('api/csrf-token/', GetCSRFToken.as_view(), name='csrf-token'),
    path('api/pois/', include('pois.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]
