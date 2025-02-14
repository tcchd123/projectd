from django.db import models

# Create your models here.
class product(models.Model):
    brand_name=models.CharField(max_length=500)
    product_specialize=models.CharField(max_length=500)
    price = models.DecimalField(
        max_digits=12,  # Supports large amounts (e.g., ₹99,99,99,999.99)
        decimal_places=2,  # Two decimal places for paisa (e.g., ₹999.99)
        help_text="Price in INR (₹)."
    )
    available_from = models.DateField(help_text="Date when the product becomes available.")
    available_until = models.DateField(null=True, blank=True, help_text="Date when the product is no longer available. Leave blank if always available.")
    min_distance = models.FloatField(help_text="Minimum distance in km")
    max_distance = models.FloatField(help_text="Maximum distance in km")
    address=models.TextField()
    contact=models.IntegerField()

    def _str_(self):
        return self.name
