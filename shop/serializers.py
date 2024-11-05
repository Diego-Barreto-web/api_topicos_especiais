from rest_framework import serializers
from .models import User, Product, Venda

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
        fields = ['id', 'name', 'price', 'stock', 'created_at', 'updated_at', 'deleted_at']

class VendaSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)  # Inclui os detalhes do cliente na resposta
    products = ProductSerializer(many=True, read_only=True)  # Inclui os detalhes dos produtos na resposta

    class Meta:
        model = Venda
        fields = ['id', 'client', 'products', 'created_at', 'updated_at', 'deleted_at']
