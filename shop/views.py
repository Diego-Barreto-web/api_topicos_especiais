from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Product, Venda
from .serializers import UserSerializer, ProductSerializer, VendaSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone



class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        
class GetUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        active_users = User.objects.filter(deleted_at__isnull=True)
        deleted_users = User.objects.filter(deleted_at__isnull=False)

        active_serializer = UserSerializer(active_users, many=True)
        deleted_serializer = UserSerializer(deleted_users, many=True)

        return Response({
            "active_users": active_serializer.data,
            "deleted_users": deleted_serializer.data
        })


    def post(self, request):
        if not request.user.admin:
            return Response({"message": "Apenas administradores podem criar novos usuários."}, status=status.HTTP_403_FORBIDDEN)

        email = request.data.get("email")

        if User.objects.filter(email=email, deleted_at__isnull=True).exists():
            return Response({"message": "Um usuário com este e-mail já existe."}, status=status.HTTP_400_BAD_REQUEST)

        username = f"{request.data.get('first_name', '')} {request.data.get('last_name', '')}".strip()

        if User.objects.filter(username=username, deleted_at__isnull=True).exists():
            return Response({"message": "Já existe um usuário com esse nome."}, status=status.HTTP_400_BAD_REQUEST)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone = request.data.get('phone')
        password = request.data.get('password')

        new_user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted_at=None
        )
        
        new_user.set_password(password)

        try:
            new_user.save()
            return Response({"message": "Usuário criado com sucesso"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": "Erro ao criar usuário. O nome de usuário pode já estar em uso."}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        if not request.user.admin:
            return Response({"message": "Apenas administradores podem atualizar usuários."}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get("id")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not user_id:
            return Response({"message": "ID do usuário não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id, deleted_at__isnull=True)

            if User.objects.filter(email=email, deleted_at__isnull=True).exclude(id=user.id).exists():
                return Response({"message": "Um usuário com este e-mail já existe."}, status=status.HTTP_400_BAD_REQUEST)

            username = f"{first_name} {last_name}".strip()

            if User.objects.filter(username=username, deleted_at__isnull=True).exclude(id=user.id).exists():
                return Response({"message": "Já existe um usuário com esse nome."}, status=status.HTTP_400_BAD_REQUEST)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if password:
                user.set_password(password)
            user.username = username
            user.updated_at = timezone.now()

            user.save()

            return Response({"message": "Usuário atualizado com sucesso."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Usuário não encontrado ou já deletado."}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):
        if not request.user.admin:
            return Response({"message": "Apenas administradores podem deletar usuários."}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"message": "user_id não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id, deleted_at__isnull=True)
            current_time = timezone.now().strftime('%Y%m%d_%H%M%S')

            user.username = f"DELETADO({user.username}){current_time}"
            user.email = f"DELETADO({user.email}){current_time}"

            user.deleted_at = timezone.now()
            user.save()

            return Response({"message": "Usuário deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"message": "Usuário não encontrado ou já deletado."}, status=status.HTTP_404_NOT_FOUND)
        
class UniqueUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("id")

        if not user_id:
            return Response({"message": "ID do usuário não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id, deleted_at__isnull=True)
            
            user_data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "deleted_at": user.deleted_at,
            }

            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Usuário não encontrado ou já deletado."}, status=status.HTTP_404_NOT_FOUND)



















#EM PRODUÇÃO
class ProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Produto criado com sucesso"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateStockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        stock = request.data.get("stock")
        if stock is not None:
            product.stock = stock
            product.save()
            return Response({"message": "Estoque atualizado com sucesso"}, status=status.HTTP_200_OK)
        return Response({"message": "Valor de estoque inválido"}, status=status.HTTP_400_BAD_REQUEST)


class VendaListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendas = Venda.objects.all()
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data)

    def post(self, request):
        client_id = request.data.get("client_id")
        product_ids = request.data.get("product_ids")

        if not client_id or not product_ids:
            return Response({"message": "client_id e product_ids são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = User.objects.get(id=client_id, admin=False)  # Filtra apenas usuários que não são admin
        except User.DoesNotExist:
            return Response({"message": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(id__in=product_ids)
        if not products or products.count() != len(product_ids):
            return Response({"message": "Um ou mais produtos não encontrados"}, status=status.HTTP_404_NOT_FOUND)

        # Verificar estoque e atualizar
        for product in products:
            if product.stock <= 0:
                return Response({"message": f"Produto {product.name} está sem estoque"}, status=status.HTTP_400_BAD_REQUEST)
            product.stock -= 1  # Diminui o estoque em 1 para cada produto
            product.save()

        # Cria a nova venda
        venda = Venda.objects.create(client=client)
        venda.products.set(products)
        venda.save()

        return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)