from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import sync_to_async
from adrf.views import APIView
from .serializers import UserSerializer
from .models import User
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken


class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    async def get(self, request):
        return JsonResponse({'csrfToken': get_token(request)})


class CreateUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    async def post(self, request):
        serializer = UserSerializer(data=request.data)
        if await sync_to_async(serializer.is_valid)():
            user = await sync_to_async(serializer.save)()
            await sync_to_async(login)(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'message': 'User created and logged in successfully', 'token': str(refresh.access_token)}, status=201)
        return JsonResponse(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    async def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = await sync_to_async(authenticate)(request, username=username, password=password)
        if user is not None:
            await sync_to_async(login)(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'message': 'Login successful', 'token': str(refresh.access_token)}, status=200)
        return JsonResponse({'error': 'Invalid username or password'}, status=400)


class LogoutView(APIView):
    async def post(self, request):
        await sync_to_async(logout)(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
