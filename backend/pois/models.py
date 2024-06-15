from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class PointOfInterest(models.Model):
    """
    Model representing a point of interest.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-90.0),
            MaxValueValidator(90.0)
        ]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-180.0),
            MaxValueValidator(180.0)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.description} at ({self.latitude}, {self.longitude})'

    @property
    def username(self) -> str:
        return self.user.username
