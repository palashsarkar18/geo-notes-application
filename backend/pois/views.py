from rest_framework import generics, permissions
from .models import PointOfInterest
from .serializers import PointOfInterestSerializer


class PointOfInterestListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create points of interest.
    """
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    print("I AM HERE 1c")

    def get_queryset(self):
        print("I AM HERE 1a")
        print(self.request.data)
        return PointOfInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer: PointOfInterestSerializer) -> None:
        print("I AM HERE 1b")
        print(self.request.data)
        serializer.save(user=self.request.user)


class PointOfInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete points of interest.
    """
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointOfInterest.objects.filter(user=self.request.user)
# TODO: Check if it is okay to define two classes inside views.py
