from django.urls import path
from .views import GetCSRFToken, CreateUserView, LoginView, LogoutView

urlpatterns = [
    path('csrf-token/', GetCSRFToken.as_view(), name='get-csrf-token'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
