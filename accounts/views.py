from django.contrib.auth import login
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
