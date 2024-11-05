
# Documentação da API de Usuários

Esta API fornece funcionalidades para gerenciar usuários, incluindo login, recuperação de informações de usuários, criação, atualização e exclusão. A API é protegida e requer autenticação para acessar a maioria dos endpoints.

## Tecnologias Utilizadas

- **Django**
- **Django REST Framework**
- **SQLite3**

## Endpoints

### 1. Login de Usuário

- **URL:** `/login`
- **Método:** `POST`
- **Descrição:** Realiza o login do usuário e retorna tokens de acesso e atualização.

**Requisição:**

```json
{
    "username": "seu_username",
    "password": "sua_senha"
}
```

**Resposta de Sucesso:**

```json
{
    "refresh": "refresh_token_value",
    "access": "access_token_value"
}
```

**Resposta de Erro:**

```json
{
    "message": "Credenciais inválidas"
}
```

---

### 2. Obter Informações do Usuário Logado

- **URL:** `/getUser`
- **Método:** `GET`
- **Descrição:** Recupera as informações do usuário autenticado.

**Resposta:**

```json
{
    "id": 1,
    "username": "seu_username",
    "email": "seu_email@example.com",
    "first_name": "Seu",
    "last_name": "Nome",
    "phone": "1234567890",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "deleted_at": null
}
```

---

### 3. Gerenciar Usuários (Administração)

- **URL:** `/users`
- **Método:** `GET`, `POST`, `PUT`, `DELETE`
- **Descrição:** Permite listar usuários ativos e deletados, além de criar, atualizar e excluir usuários.

#### a. Listar Usuários

- **Método:** `GET`

**Resposta:**

```json
{
    "active_users": [
        {
            "id": 1,
            "username": "seu_username",
            "email": "seu_email@example.com",
            ...
        }
    ],
    "deleted_users": [
        {
            "id": 2,
            "username": "deletado_username",
            "email": "deletado_email@example.com",
            ...
        }
    ]
}
```

#### b. Criar Novo Usuário

- **Método:** `POST`

**Requisição:**

```json
{
    "first_name": "Nome",
    "last_name": "Sobrenome",
    "email": "novo_email@example.com",
    "phone": "1234567890",
    "password": "nova_senha"
}
```

**Resposta de Sucesso:**

```json
{
    "message": "Usuário criado com sucesso"
}
```

**Resposta de Erro:**

```json
{
    "message": "Um usuário com este e-mail já existe."
}
```

#### c. Atualizar Usuário

- **Método:** `PUT`

**Requisição:**

```json
{
    "id": 1,
    "first_name": "NovoNome",
    "last_name": "NovoSobrenome",
    "email": "novo_email@example.com",
    "password": "nova_senha"
}
```

**Resposta de Sucesso:**

```json
{
    "message": "Usuário atualizado com sucesso."
}
```

**Resposta de Erro:**

```json
{
    "message": "Usuário não encontrado ou já deletado."
}
```

#### d. Excluir Usuário

- **Método:** `DELETE`

**Requisição:**

```json
{
    "user_id": 1
}
```

**Resposta de Sucesso:**

```json
{
    "message": "Usuário deletado com sucesso."
}
```

**Resposta de Erro:**

```json
{
    "message": "Usuário não encontrado ou já deletado."
}
```

---

### 4. Obter Informações de um Usuário Específico

- **URL:** `/getUniqueUser`
- **Método:** `GET`
- **Descrição:** Recupera as informações de um usuário específico, se não estiver deletado.

**Requisição:**

`GET /getUniqueUser?id=1`

**Resposta:**

```json
{
    "id": 1,
    "username": "seu_username",
    "email": "seu_email@example.com",
    "first_name": "Seu",
    "last_name": "Nome",
    "phone": "1234567890",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "deleted_at": null
}
```

---

## Autenticação

Todos os endpoints, exceto `/login`, requerem que o usuário esteja autenticado. O token de acesso deve ser incluído no cabeçalho da requisição da seguinte forma:

```
Authorization: Bearer <token>
```

---

## Considerações Finais

Esta API é projetada para facilitar a gestão de usuários em um sistema. A autenticação é um aspecto crucial, garantindo que apenas usuários autorizados possam realizar operações sensíveis.

