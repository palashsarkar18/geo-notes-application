from rest_framework import generics, permissions
from .models import PointOfInterest
from .serializers import PointOfInterestSerializer


class PointOfInterestListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create points of interest.
    """
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: PointOfInterestSerializer) -> None:
        serializer.save(user=self.request.user)


class PointOfInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete points of interest.
    """
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# TODO: Check if it is okay to define two classes inside views.py
