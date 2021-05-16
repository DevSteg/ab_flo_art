from django.db import models

# Create your models here.


class Order(models.Model):

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(max_length=300, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=False)
    town_city = models.CharField(max_length=50, null=False, blank=False)
    county = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=60, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
