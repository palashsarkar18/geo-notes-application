from typing import Any, Tuple
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from .serializers import UserSerializer
from .models import User


class GetCSRFToken(APIView):
    """
    API view to get CSRF token.
    """
    permission_classes = [AllowAny]

    def get(self, request: Request) -> JsonResponse:
        return JsonResponse({'csrfToken': get_token(request)})


class CreateUserView(generics.CreateAPIView):
    """
    API view to create a new user and redirect to the POIs page.
    """
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self,
               request: Request,
               *args: Any,
               **kwargs: Any) -> JsonResponse:
        # Call the original create method to create the user
        serializer: BaseSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()

        # Create a response
        response: Response = Response(serializer.data,
                                      status=status.HTTP_201_CREATED)

        # Log in the newly created user if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            login(request, user)
            token: Tuple[Token, bool] = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'message': 'User created and logged in successfully',
                'token': token[0].key}, status=201)

        return response


class LoginView(APIView):
    """
    View to handle user login via API.
    """
    permission_classes = [AllowAny]

    def post(self, request: Request) -> JsonResponse:
        username: str = request.data.get('username')
        password: str = request.data.get('password')
        user: User = authenticate(request,
                                  username=username,
                                  password=password)

        if user is not None:
            login(request, user)
            token: Tuple[Token, bool] = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Login successful',
                                 'token': token[0].key},
                                status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'},
                                status=400)


class LogoutView(APIView):
    """
    View to handle user logout via API.
    """
    def post(self, request: Request) -> JsonResponse:
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
