from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User


class CreateUserView(generics.CreateAPIView):
    """
    API view to create a new user and redirect to the POIs page.
    """
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Call the original create method to create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create a response
        response = Response(serializer.data, status=status.HTTP_201_CREATED)

        # Log in the newly created user if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            login(request, user)
            return HttpResponseRedirect(redirect_to='/api/pois/')

        return response


class LoginView(View):
    """
    View to handle user login via a form.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/api/pois/')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'accounts/login.html')


class LogoutView(View):
    """
    View to handle user logout.
    """
    def post(self, request):
        logout(request)
        messages.success(request, 'Logout successful!')
        return redirect('user-login')
