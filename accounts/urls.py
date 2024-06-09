from django.urls import path
from .views import CreateUserView, LoginView, LogoutView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]
