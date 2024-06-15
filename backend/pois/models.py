from django.db import models
from accounts.models import User


class PointOfInterest(models.Model):
    """
    Model representing a point of interest.
    """
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    description: models.TextField = models.TextField()
    latitude: models.DecimalField = models.DecimalField(max_digits=9,
                                                        decimal_places=6)
    longitude: models.DecimalField = models.DecimalField(max_digits=9,
                                                         decimal_places=6)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.description} at ({self.latitude}, {self.longitude})'
