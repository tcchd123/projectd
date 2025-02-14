from django.db import models

# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=500)
    specialize=models.CharField(max_length=500)
    price = models.DecimalField(
        max_digits=12,  # Supports large amounts (e.g., ₹99,99,99,999.99)
        decimal_places=2,  # Two decimal places for paisa (e.g., ₹999.99)
        help_text="Price in INR (₹)."
    )
    max_distance = models.FloatField(help_text="Maximum distance in km")
    address=models.TextField()
    contact=models.IntegerField()

    def _str_(self):
        return self.name
