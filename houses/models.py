from django.db import models

# Create your models here.
class House(models.Model):

    """Model Definition for Houses"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        default=True,
        verbose_name="Pets Allowed?",
        help_text="Are pets allowed here? ",
    )

    def __str__(self):
        return self.name
