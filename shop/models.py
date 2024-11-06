from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid_extensions import uuid7

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False) 
    admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False) 
    name = models.CharField(max_length=100,null=True, blank=True)
    mark = models.CharField(max_length=100, null=True, blank=True)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    expiration_date = models.DateField(null=True, blank=True)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.mark + " - " + str(self.stock)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": str(self.price),
            "stock": self.stock,
        }
    
class Venda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False) 
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discont = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=100, default="PENDENTE")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "client": self.client.serialize(),
            "products": [p.serialize() for p in self.products.all()],
            "created_at": self.created_at,
        }