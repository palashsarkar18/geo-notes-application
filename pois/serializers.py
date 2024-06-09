from rest_framework import serializers
from .models import PointOfInterest


class PointOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = ['id', 'user', 'description', 'latitude', 'longitude', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
