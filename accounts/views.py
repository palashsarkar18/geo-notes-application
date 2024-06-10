from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import UserSerializer
from .models import User
from django.middleware.csrf import get_token


class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({'csrfToken': get_token(request)})


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
            return JsonResponse({'message': 'User created and logged in successfully', 'token': 'dummy-token'}, status=201)

        return response


class LoginView(APIView):
    """
    View to handle user login via API.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'token': 'dummy-token'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)


class LogoutView(APIView):
    """
    View to handle user logout via API.
    """
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
