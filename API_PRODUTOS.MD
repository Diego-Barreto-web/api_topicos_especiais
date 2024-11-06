
# API de Produtos

Essa API gerencia as operações CRUD (criar, ler, atualizar e deletar) para o recurso `Produto`.

## Endpoints

### 1. **Listar Produtos**
   **Método:** `GET`  
   **URL:** `/products`  
   **Descrição:** Retorna todos os produtos cujo campo `deleted_at` é `NULL`.  
   **Resposta:**  
   - **Código 200 OK**: Lista de produtos.
   - **Exemplo de resposta:**

     ```json
     [
       {
         "id": "1",
         "name": "Produto A",
         "stock": 10,
         "barcode": "1234567890123",
         "price": 100.0,
         "deleted_at": null
       },
       {
         "id": "2",
         "name": "Produto B",
         "stock": 5,
         "barcode": "9876543210987",
         "price": 50.0,
         "deleted_at": null
       }
     ]
     ```

### 2. **Criar Produto**
   **Método:** `POST`  
   **URL:** `/products`  
   **Descrição:** Cria um novo produto. Apenas administradores podem criar produtos.  
   **Corpo da requisição:**
   ```json
   {
     "name": "Novo Produto",
     "stock": 50,
     "barcode": "1234567899999",
     "price": 200.0
   }
   ```
   **Resposta:**  
   - **Código 201 Created**: Produto criado com sucesso.
   - **Código 403 Forbidden**: Se o usuário não for administrador.
   - **Código 400 Bad Request**: Se o código de barras já existir.
   
   **Exemplo de resposta (201 Created):**
   ```json
   {
     "id": "3",
     "name": "Novo Produto",
     "stock": 50,
     "barcode": "1234567899999",
     "price": 200.0,
     "deleted_at": null
   }
   ```

### 3. **Atualizar Produto**
   **Método:** `PUT`  
   **URL:** `/products`  
   **Descrição:** Atualiza um produto existente. Apenas administradores podem atualizar produtos.  
   **Parâmetros (body):**
   ```json
   {
     "id": "1",
     "name": "Produto Atualizado",
     "stock": 30
   }
   ```
   **Resposta:**  
   - **Código 200 OK**: Produto atualizado com sucesso.
   - **Código 403 Forbidden**: Se o usuário não for administrador.
   - **Código 400 Bad Request**: Se o ID ou código de barras forem inválidos.

### 4. **Deletar Produto (Soft Delete)**
   **Método:** `DELETE`  
   **URL:** `/products`  
   **Descrição:** Deleta um produto logicamente (marca o campo `deleted_at` com a data/hora atual). Apenas administradores podem deletar produtos.  
   **Parâmetros (body):**
   ```json
   {
     "id": "1"
   }
   ```
   **Resposta:**  
   - **Código 200 OK**: Produto deletado com sucesso.
   - **Código 403 Forbidden**: Se o usuário não for administrador.
   - **Código 400 Bad Request**: Se o produto já foi deletado ou se o identificador for inválido.

### 5. **Detalhes do Produto**
   **Método:** `GET`  
   **URL:** `/productDetail`  
   **Descrição:** Retorna os detalhes de um produto baseado no ID ou código de barras.  
   **Parâmetros (query):**
   - `identifier` (string): ID ou código de barras do produto.
   
   **Resposta:**  
   - **Código 200 OK**: Detalhes do produto encontrado.
   - **Código 400 Bad Request**: Se o identificador estiver ausente ou for inválido.

   **Exemplo de URL:**  
   `/productDetail?identifier=1234567890123`

### 6. **Produtos com Menor Estoque**
   **Método:** `GET`  
   **URL:** `/productStock`  
   **Descrição:** Retorna os 4 produtos com o menor estoque (não deletados).  
   **Resposta:**  
   - **Código 200 OK**: Lista de 4 produtos com menor estoque.
   
   **Exemplo de resposta:**
   ```json
   [
     {
       "id": "2",
       "name": "Produto B",
       "stock": 5,
       "barcode": "9876543210987",
       "price": 50.0,
       "deleted_at": null
     },
     {
       "id": "1",
       "name": "Produto A",
       "stock": 10,
       "barcode": "1234567890123",
       "price": 100.0,
       "deleted_at": null
     }
   ]
   ```

## URLs

- `path('products', ProductMainView.as_view(), name='products')`
- `path('productDetail', ProductDetailView.as_view(), name='productDetail')`
- `path('productStock', ProductStockView.as_view(), name='productStock')`
