
# API de Produtos

## Visão Geral
A API de produtos permite o gerenciamento completo de produtos, incluindo a criação, leitura, atualização e exclusão (soft delete). Ela utiliza um modelo de dados com campos detalhados para gerenciar os produtos, como ID, nome, marca, preços e muito mais.

## Endpoints

### 1. `GET /products`
**Descrição**: Recupera todos os produtos com `deleted_at` igual a `null`.

**Resposta de Sucesso**:
```json
[
  {
    "id": "UUID do produto",
    "name": "Nome do produto",
    "mark": "Marca do produto",
    "unit_value": "Valor unitário",
    "sale_value": "Valor de venda",
    "stock": "Quantidade em estoque",
    "expiration_date": "Data de validade",
    "barcode": "Código de barras",
    "created_at": "Data de criação",
    "updated_at": "Data de atualização",
    "deleted_at": null
  }
]
```

### 2. `POST /products`
**Descrição**: Cria um novo produto. Apenas administradores podem criar produtos.

**Corpo da Solicitação**:
```json
{
  "name": "Nome do produto",
  "mark": "Marca do produto",
  "unit_value": "Valor unitário",
  "sale_value": "Valor de venda",
  "stock": "Quantidade em estoque",
  "expiration_date": "Data de validade",
  "barcode": "Código de barras"
}
```

**Resposta de Sucesso**:
```json
{
  "id": "UUID do produto",
  "name": "Nome do produto",
  "mark": "Marca do produto",
  "unit_value": "Valor unitário",
  "sale_value": "Valor de venda",
  "stock": "Quantidade em estoque",
  "expiration_date": "Data de validade",
  "barcode": "Código de barras",
  "created_at": "Data de criação",
  "updated_at": "Data de atualização",
  "deleted_at": null
}
```

**Erros Comuns**:
- `400 Bad Request`: Caso o código de barras já esteja em uso ou o corpo da solicitação seja inválido.

### 3. `PUT /products`
**Descrição**: Atualiza um produto existente. O produto pode ser identificado por `id` ou `barcode`.

**Corpo da Solicitação**:
```json
{
  "id": "UUID do produto",
  "name": "Nome do produto",
  "mark": "Marca do produto",
  "unit_value": "Valor unitário",
  "sale_value": "Valor de venda",
  "stock": "Quantidade em estoque",
  "expiration_date": "Data de validade",
  "barcode": "Código de barras"
}
```

**Resposta de Sucesso**:
```json
{
  "id": "UUID do produto",
  "name": "Nome do produto",
  "mark": "Marca do produto",
  "unit_value": "Valor unitário",
  "sale_value": "Valor de venda",
  "stock": "Quantidade em estoque",
  "expiration_date": "Data de validade",
  "barcode": "Código de barras",
  "created_at": "Data de criação",
  "updated_at": "Data de atualização",
  "deleted_at": null
}
```

### 4. `DELETE /products`
**Descrição**: Realiza o soft delete de um produto, marcando o campo `deleted_at` com a data e hora atuais.

**Corpo da Solicitação**:
```json
{
  "id": "UUID do produto"
}
```

**Resposta de Sucesso**:
```json
{
  "message": "Produto deletado com sucesso."
}
```

**Erros Comuns**:
- `400 Bad Request`: Caso o produto já tenha sido deletado ou o identificador fornecido seja inválido.

### 5. `GET /productDetail`
**Descrição**: Recupera detalhes de um produto com base no `id` ou `barcode`.

**Parâmetros**:
- `identifier`: Pode ser o `id` ou o `barcode` do produto.

**Resposta de Sucesso**:
```json
{
  "id": "UUID do produto",
  "name": "Nome do produto",
  "mark": "Marca do produto",
  "unit_value": "Valor unitário",
  "sale_value": "Valor de venda",
  "stock": "Quantidade em estoque",
  "expiration_date": "Data de validade",
  "barcode": "Código de barras",
  "created_at": "Data de criação",
  "updated_at": "Data de atualização",
  "deleted_at": null
}
```

### 6. `GET /productStock`
**Descrição**: Recupera os 4 produtos com `deleted_at = null` com o menor estoque.

**Resposta de Sucesso**:
```json
[
  {
    "id": "UUID do produto",
    "name": "Nome do produto",
    "mark": "Marca do produto",
    "unit_value": "Valor unitário",
    "sale_value": "Valor de venda",
    "stock": "Quantidade em estoque",
    "expiration_date": "Data de validade",
    "barcode": "Código de barras",
    "created_at": "Data de criação",
    "updated_at": "Data de atualização",
    "deleted_at": null
  }
]
```

---

## URLs

- `path('products', ProductMainView.as_view(), name='products')`
- `path('productDetail', ProductDetailView.as_view(), name='productDetail')`
- `path('productStock', ProductStockView.as_view(), name='productStock')`