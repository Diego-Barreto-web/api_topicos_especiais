# **Documentação da API de Vendas**

## **Visão Geral**
Esta API é responsável pela gestão de vendas de um sistema de e-commerce. O sistema permite aos clientes visualizar, criar, pagar, atualizar e cancelar vendas, bem como registrar o pagamento das mesmas. Administradores têm acesso a todas as vendas, enquanto clientes têm acesso apenas às suas vendas pendentes.

## **Tecnologias Usadas**
- Django Rest Framework
- Django ORM
- PostgreSQL (ou outro banco de dados suportado)
- UUID para identificação única de vendas e produtos

## **Estrutura da API**

### **Modelos**
1. **Product**
   - Representa um produto.
   - Campos principais:
     - `id`: UUID, identificador único.
     - `name`: Nome do produto.
     - `mark`: Marca do produto.
     - `unit_value`: Valor unitário do produto.
     - `sale_value`: Valor de venda.
     - `stock`: Quantidade em estoque.
     - `expiration_date`: Data de validade.
     - `barcode`: Código de barras.
   
2. **Venda**
   - Representa uma venda realizada por um cliente.
   - Campos principais:
     - `id`: UUID, identificador único.
     - `client`: Referência ao usuário (cliente).
     - `total`: Valor total da venda.
     - `discount`: Desconto aplicado à venda.
     - `status`: Status da venda (PENDENTE, PAGO, CANCELADO).
   
3. **VendaItem**
   - Representa um item em uma venda.
   - Campos principais:
     - `venda`: Referência à venda.
     - `product`: Referência ao produto.
     - `quantity`: Quantidade do produto na venda.

---

## **Endpoints da API**

### **1. /vendas [GET, POST]**

- **GET**: Retorna todas as vendas do cliente autenticado.
  - **URL**: `/vendas`
  - **Método**: GET
  - **Resposta**:
    ```json
    [
        {
            "id": "uuid",
            "client": "username",
            "products": [
                {
                    "product_id": "uuid",
                    "product_name": "Product Name",
                    "quantity": 2
                }
            ],
            "total": "value",
            "discount": "value",
            "status": "PENDENTE",
            "created_at": "timestamp",
            "updated_at": "timestamp"
        }
    ]
    ```
  - **Permissões**: Usuário autenticado.

- **POST**: Cria uma nova venda para o cliente autenticado.
  - **URL**: `/vendas`
  - **Método**: POST
  - **Dados**:
    ```json
    {
        "products": [
            {
                "product_id": "uuid",
                "quantity": 1
            }
        ]
    }
    ```
  - **Resposta**:
    ```json
    {
        "id": "uuid",
        "client": "username",
        "products": [
            {
                "product_id": "uuid",
                "quantity": 1
            }
        ],
        "total": "value",
        "discount": "value",
        "status": "PENDENTE",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
    ```
  - **Permissões**: Usuário autenticado.

---

### **2. /pagar [PUT]**

- **PUT**: Marca a venda como paga.
  - **URL**: `/pagar`
  - **Método**: PUT
  - **Dados**:
    ```json
    {
        "venda_id": "uuid",
        "pagamento": true
    }
    ```
  - **Resposta**:
    ```json
    {
        "message": "Venda paga com sucesso.",
        "venda": {
            "id": "uuid",
            "client": "username",
            "products": [
                {
                    "product_id": "uuid",
                    "quantity": 2
                }
            ],
            "total": "value",
            "discount": "value",
            "status": "PAGO",
            "created_at": "timestamp",
            "updated_at": "timestamp"
        }
    }
    ```
  - **Permissões**: Usuário autenticado.

---

### **3. /vendasList [GET]**

- **GET**: Retorna todas as vendas para administradores.
  - **URL**: `/vendasList`
  - **Método**: GET
  - **Resposta**:
    ```json
    [
        {
            "id": "uuid",
            "client": "username",
            "products": [
                {
                    "product_id": "uuid",
                    "product_name": "Product Name",
                    "quantity": 2
                }
            ],
            "total": "value",
            "discount": "value",
            "status": "PENDENTE",
            "created_at": "timestamp",
            "updated_at": "timestamp"
        }
    ]
    ```
  - **Permissões**: Administrador autenticado.

---