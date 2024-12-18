from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, VendaItem
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Product, Venda
from .serializers import UserSerializer, ProductSerializer, VendaSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q



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




class ProductMainView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(deleted_at__isnull=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        user_serializer = UserSerializer(user)

        if not user_serializer.data.get('admin'):
            return Response({"message": "Apenas administradores podem criar novos produtos."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"message": "Já existe um produto com esse código de barras."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request):
        user = request.user
        user_serializer = UserSerializer(user)

        if not user_serializer.data.get('admin'):
            return Response({"message": "Apenas administradores podem atualizar produtos."}, status=status.HTTP_403_FORBIDDEN)

        identifier = request.data.get("id") or request.data.get("barcode")

        if not identifier:
            return Response({"message": "ID ou código de barras é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        product = None
        if isinstance(identifier, str) and len(identifier) == 36:
            product = get_object_or_404(Product, id=identifier)
        elif isinstance(identifier, str):
            product = get_object_or_404(Product, barcode=identifier)
        else:
            return Response({"message": "ID ou código de barras inválido."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        user = request.user
        user_serializer = UserSerializer(user)

        if not user_serializer.data.get('admin'):
            return Response({"message": "Apenas administradores podem deletar produtos."}, status=status.HTTP_403_FORBIDDEN)

        identifier = request.data.get("id") or request.data.get("barcode")

        if not identifier:
            return Response({"message": "É necessário fornecer o id ou o código de barras do produto."}, status=status.HTTP_400_BAD_REQUEST)

        product = None
        if isinstance(identifier, str) and len(identifier) == 36:
            product = get_object_or_404(Product, id=identifier)
        elif isinstance(identifier, str):
            product = get_object_or_404(Product, barcode=identifier)
        else:
            return Response({"message": "ID ou código de barras inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
        if product.deleted_at:
            return Response({"message": "Este produto já foi deletado."}, status=status.HTTP_400_BAD_REQUEST)

        product.deleted_at = timezone.now()
        product.save()

        return Response({"message": "Produto deletado com sucesso."}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        identifier = request.query_params.get('identifier', None)

        if not identifier:
            return Response({"message": "É necessário fornecer o id ou o código de barras do produto."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        product = None
        if isinstance(identifier, str) and len(identifier) == 36:
            product = get_object_or_404(Product, id=identifier)
        elif isinstance(identifier, str):
            product = get_object_or_404(Product, barcode=identifier)
        else:
            return Response({"message": "ID ou código de barras inválido."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductStockView(APIView):
    
    def get(self, request):
        products = Product.objects.filter(deleted_at__isnull=True).order_by('stock')[:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class VendaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendas = Venda.objects.filter(client=request.user).select_related('client').prefetch_related('vendaitem_set__product')
        serializer = VendaSerializer(vendas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        products_data = request.data.get("products", [])
        user = request.user

        if not products_data:
            return Response(
                {"message": "A lista de produtos é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST
            )

        venda_pendente = Venda.objects.filter(client=user, status="PENDENTE").first()

        if venda_pendente:
            venda_pendente.status = "CANCELADA"
            venda_pendente.save()

            for venda_item in venda_pendente.vendaitem_set.all():
                product = venda_item.product
                product.stock += venda_item.quantity 
                product.save()

        venda = Venda.objects.create(client=user, status="PENDENTE")
        total = 0

        for product_data in products_data:
            product_id = product_data.get("product_id")
            quantity = product_data.get("quantity", 1)

            if not product_id or quantity <= 0:
                return Response(
                    {"message": "Cada produto deve ter um 'product_id' válido e 'quantity' maior que 0."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product = get_object_or_404(Product, id=product_id, deleted_at__isnull=True)

            if product.stock < quantity:
                return Response(
                    {"message": f"O produto '{product.name}' não tem estoque suficiente."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            VendaItem.objects.create(venda=venda, product=product, quantity=quantity)

            product.stock -= quantity
            product.save()

            total += product.sale_value * quantity

        venda.total = total
        venda.save()

        return Response(
            venda.serialize(),
            status=status.HTTP_201_CREATED
        )
    
    def put(self, request):
        venda = Venda.objects.filter(client=request.user, status='PENDENTE').first()

        if not venda:
            return Response(
                {"message": "Nenhuma venda pendente encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        products_data = request.data.get("products", [])

        if not products_data:
            return Response(
                {"message": "A lista de produtos é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = venda.total

        for product_data in products_data:
            product_id = product_data.get("product_id")
            quantity = product_data.get("quantity", 1)

            if not product_id:
                return Response(
                    {"message": "Cada produto deve ter um 'product_id' válido."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if quantity == 0:
                venda_item = VendaItem.objects.filter(venda=venda, product__id=product_id).first()
                if venda_item:
                    product = venda_item.product
                    product.stock += venda_item.quantity 
                    product.save()
                    total -= venda_item.product.sale_value * venda_item.quantity  
                    venda_item.delete()
                continue 

            product = get_object_or_404(Product, id=product_id, deleted_at__isnull=True)

            if product.stock < quantity and quantity > 0:
                return Response(
                    {"message": f"O produto '{product.name}' não tem estoque suficiente."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            venda_item = VendaItem.objects.filter(venda=venda, product=product).first()

            if venda_item:
                previous_quantity = venda_item.quantity
                venda_item.quantity += quantity

                if venda_item.quantity <= 0:
                    product.stock += previous_quantity
                    product.save()
                    total -= venda_item.product.sale_value * previous_quantity
                    venda_item.delete()
                    continue
                else:
                    if quantity < 0:
                        product.stock -= abs(quantity) 
                    else:
                        product.stock -= quantity
                    product.save()

                    total += product.sale_value * quantity

            else:
                if quantity > 0:
                    venda_item = VendaItem.objects.create(venda=venda, product=product, quantity=quantity)
                    product.stock -= quantity
                    product.save()

                    total += product.sale_value * quantity

            venda_item.save()

        venda.total = total
        venda.save()

        return Response(
            venda.serialize(),
            status=status.HTTP_200_OK
        )
    
    def delete(self, request):
        venda = Venda.objects.filter(client=request.user, status='PENDENTE').first()

        if not venda:
            return Response(
                {"message": "Nenhuma venda pendente encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        venda.status = 'CANCELADA'
        venda.save()

        for venda_item in venda.vendaitem_set.all():
            product = venda_item.product
            product.stock += venda_item.quantity
            product.save()

        return Response(
            {"message": f"Venda {venda.id} cancelada com sucesso e produtos devolvidos ao estoque."},
            status=status.HTTP_200_OK
        )
    
class PayVendaView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        venda = Venda.objects.filter(client=request.user, status='PENDENTE').first()

        if not venda:
            return Response(
                {"message": "Nenhuma venda pendente encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        pagamento = request.data.get("pagamento", False) 

        if not pagamento:
            return Response(
                {"message": "O pagamento não foi informado ou não foi realizado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        venda.status = "PAGO"
        venda.save()

        return Response(
            {"message": "Venda paga com sucesso.", "venda": venda.serialize()},
            status=status.HTTP_200_OK
        )
    
class VendaListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not getattr(request.user, 'admin', False):
            return Response(
                {"message": "Acesso restrito. Somente administradores podem visualizar todas as vendas."},
                status=status.HTTP_403_FORBIDDEN
            )

        vendas = Venda.objects.all()

        serialized_vendas = [venda.serialize() for venda in vendas]

        return Response(serialized_vendas, status=status.HTTP_200_OK)