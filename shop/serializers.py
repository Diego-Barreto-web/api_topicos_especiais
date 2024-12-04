from rest_framework import serializers
from .models import User, Product, Venda, VendaItem

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name', 'admin', 'created_at', 'updated_at', 'deleted_at', 'password']
        read_only_fields = ['username', 'created_at', 'updated_at', 'deleted_at']

    def create(self, validated_data):
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        validated_data['username'] = f"{first_name} {last_name}".strip()
        
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate_barcode(self, value):
        if self.instance is not None:
            if value != self.instance.barcode:
                if Product.objects.filter(barcode=value, deleted_at__isnull=True).exists():
                    raise serializers.ValidationError("Já existe um produto com este código de barras.")
        else:
            if Product.objects.filter(barcode=value, deleted_at__isnull=True).exists():
                raise serializers.ValidationError("Já existe um produto com este código de barras.")
        return value



class VendaItemSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')
    product_name = serializers.CharField(source='product.name')
    quantity = serializers.IntegerField()

    class Meta:
        model = VendaItem
        fields = ['product_id', 'product_name', 'quantity']

class VendaSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source="client.username")
    products = VendaItemSerializer(source='vendaitem_set', many=True)

    class Meta:
        model = Venda
        fields = ["id", "client", "products", "total", "discount", "status", "created_at", "updated_at"]