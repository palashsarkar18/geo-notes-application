from rest_framework import generics, permissions
from .models import PointOfInterest
from .serializers import PointOfInterestSerializer


class PointOfInterestListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create points of interest.
    """
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointOfInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer: PointOfInterestSerializer) -> None:
        serializer.save(user=self.request.user)


class PointOfInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete points of interest.
    """
    serializer_class = PointOfInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointOfInterest.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
