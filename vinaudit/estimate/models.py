from django.db import models

# Create your models here.

# vin,year,make,model,trim,dealer_name,dealer_street,dealer_city,dealer_state,
# dealer_zip,listing_price,listing_mileage,used,certified,style,driven_wheels,
# engine,fuel_type,exterior_color,interior_color,seller_website,first_seen_date,
# last_seen_date,dealer_vdp_last_seen_date,listing_status
 
class CarValueData(models.Model):
    vin = models.CharField(unique=True, max_length=200, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    make = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    trim = models.CharField(max_length=200, null=True, blank=True)
    dealer_name = models.CharField(max_length=200, null=True, blank=True)
    dealer_street = models.CharField(max_length=200, null=True, blank=True)
    dealer_city = models.CharField(max_length=200, null=True, blank=True)
    dealer_state = models.CharField(max_length=200, null=True, blank=True)
    dealer_zip = models.CharField(max_length=200, null=True, blank=True)
    listing_price = models.FloatField(null=True, blank=True)
    listing_mileage = models.FloatField(null=True, blank=True)
    used = models.BooleanField(null=True, blank=True)
    certified = models.BooleanField(null=True, blank=True)
    style = models.CharField(max_length=200, null=True, blank=True)
    driven_wheels = models.CharField(max_length=200, null=True, blank=True)
    engine = models.CharField(max_length=200, null=True, blank=True)
    fuel_type = models.CharField(max_length=200, null=True, blank=True)
    exterior_color = models.CharField(max_length=200, null=True, blank=True)
    interior_color = models.CharField(max_length=200, null=True, blank=True)
    seller_website = models.CharField(max_length=200, null=True, blank=True)
    first_seen_date = models.DateField(null=True, blank=True)
    last_seen_date = models.DateField(null=True, blank=True)
    dealer_vdp_last_seen_date = models.DateField(null=True, blank=True)
    listing_status = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
class EstimatedData(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE) ==> in future
    year = models.IntegerField(null=True, blank=True)
    make = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    estimated_price = models.FloatField(null=True, blank=True)
    listing_mileage = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
        
    