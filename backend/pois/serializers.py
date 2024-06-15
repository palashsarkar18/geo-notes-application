from rest_framework import serializers
from .models import PointOfInterest


class PointOfInterestSerializer(serializers.ModelSerializer):
    """
    Serializer for PointOfInterest model.
    """
    latitude: serializers.DecimalField = serializers.DecimalField(
        max_digits=9,
        decimal_places=6)
    longitude: serializers.DecimalField = serializers.DecimalField(
        max_digits=9,
        decimal_places=6)

    class Meta:
        model = PointOfInterest
        fields: list[str] = ['id', 'username', 'description', 'latitude',
                             'longitude', 'created_at', 'updated_at']
        read_only_fields: list[str] = ['username', 'created_at', 'updated_at']
