from django.urls import path
from .views import PointOfInterestListCreateView, PointOfInterestDetailView

urlpatterns = [
    path('pois/', PointOfInterestListCreateView.as_view(), name='poi-list-create'),
    path('pois/<int:pk>/', PointOfInterestDetailView.as_view(), name='poi-detail'),
]
