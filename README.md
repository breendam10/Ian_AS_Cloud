# ☁ AS - Projeto Cloud
Este projeto constitui em uma API para gerenciamento de Exibições artísticas, suas obras e artistas.

[Painel Swagger](https://ian-as-cloud-ddbfe6e4fqd5gnhz.centralus-01.azurewebsites.net/api/docs/)

### ⚙ Projeto desenvolvido por **Ian Esteves**

---

## 👨‍💻 Tecnologias Utilizadas

- **Python - Flask**
- **Docker**
- **Azure Web App**
- **Azure MySQL Flexible Server**
- **GitHub Actions**

---

### 🌐 API (Web App no Azure)


**MÉTODOS**:

---

### Autenticação de Usuários

- ✅ **POST /api/auth/signup** – Registra um novo usuário
  ```json
  {
    "username": "usuario_exemplo",
    "password": "senhaSegura123"
  }
  ```
  **Descrição**: Cria um usuário com nome de usuário e senha (armazenada como hash). Retorna mensagem de sucesso.

  **Resposta (201)**:
  ```json
  {
    "message": "Usuário criado"
  }
  ```
  **Erros**:
  - 400: Se o nome de usuário já existir.

---

- ✅ **POST /api/auth/login** – Realiza login e inicia sessão
  ```json
  {
    "username": "usuario_exemplo",
    "password": "senhaSegura123"
  }
  ```
  **Descrição**: Valida as credenciais. Se válidas, inicia sessão (login_user) e retorna mensagem de sucesso.

  **Resposta (200)**:
  ```json
  {
    "message": "Logado com sucesso"
  }
  ```
  **Erros**:
  - 401: Se usuário ou senha estiverem incorretos.

---

- ✅ **POST /api/auth/logout** – Encerra a sessão do usuário
  ```json
  {}
  ```
  **Descrição**: Exige que o usuário esteja autenticado (`@login_required`) e encerra a sessão (logout_user).
  **Resposta (200)**:
  ```json
  {
    "message": "Deslogado"
  }
  ```

---

### Artistas

- 🔍 **GET /api/artists/** – Retorna a lista de todos os artistas
  **Descrição**: Busca todos os registros na tabela `Artist`.
  **Resposta (200)**:
  ```json
  [
    {
      "id": 1,
      "name": "Vincent van Gogh",
      "biography": "Pintor pós-impressionista holandês...",
      "birth_date": "1853-03-30"
    },
    {
      "id": 2,
      "name": "Frida Kahlo",
      "biography": "Artista mexicana conhecida por seus autorretratos...",
      "birth_date": "1907-07-06"
    }
    // …
  ]
  ```

---

- ✅ **POST /api/artists/** – Cria um novo artista
  ```json
  {
    "name": "Claude Monet",
    "biography": "Fundador do Impressionismo francês...",
    "birth_date": "1840-11-14"
  }
  ```
  **Descrição**: Insere um registro na tabela `Artist`.
  **Resposta (201)**:
  ```json
  {
    "id": 3,
    "name": "Claude Monet",
    "biography": "Fundador do Impressionismo francês...",
    "birth_date": "1840-11-14"
  }
  ```
  **Erros**:
  - 400: Se algum campo obrigatório (`name`) estiver faltando ou inválido.

---

- 🔍 **GET /api/artists/{id}** – Retorna um artista pelo ID
  **Exemplo de URL**: `/api/artists/3`
  **Descrição**: Busca um artista específico por chave primária.
  **Resposta (200)**:
  ```json
  {
    "id": 3,
    "name": "Claude Monet",
    "biography": "Fundador do Impressionismo francês...",
    "birth_date": "1840-11-14"
  }
  ```
  **Erros**:
  - 404: Se não existir artista com o `id` informado.

---

- 🔄 **PUT /api/artists/{id}** – Atualiza um artista existente
  ```json
  {
    "name": "Claude Monet",
    "biography": "Pintor impressionista francês, famoso pelas séries de ninfeias...",
    "birth_date": "1840-11-14"
  }
  ```
  **Descrição**: Altera os campos `name`, `biography` e `birth_date` do artista de `id` informado.
  **Resposta (200)**:
  ```json
  {
    "id": 3,
    "name": "Claude Monet",
    "biography": "Pintor impressionista francês, famoso pelas séries de ninfeias...",
    "birth_date": "1840-11-14"
  }
  ```
  **Erros**:
  - 404: Se não existir artista com o `id` informado.
  - 400: Se o payload tiver campos inválidos.

---

- 🗑 **DELETE /api/artists/{id}** – Exclui um artista
  **Exemplo de URL**: `/api/artists/3`
  **Descrição**: Deleta o registro de `Artist` com o `id` especificado.
  **Resposta (200)**:
  ```json
  {
    "message": "Artista \"Claude Monet\" removido com sucesso."
  }
  ```
  **Erros**:
  - 404: Se não existir artista com o `id` informado.

---

### Obras de Arte

- 🔍 **GET /api/artworks/** – Retorna a lista de todas as obras
  **Descrição**: Recupera todos os registros de `Artwork`.
  **Resposta (200)**:
  ```json
  [
    {
      "id": 1,
      "title": "A Noite Estrelada",
      "description": "Pintura de Van Gogh...",
      "creation_date": "1889-06-01",
      "image_url": "https://exemplo.com/noite_estrela.jpg",
      "artist_id": 1
    },
    {
      "id": 2,
      "title": "As Meninas",
      "description": "Pintura de Diego Velázquez...",
      "creation_date": "1656-01-01",
      "image_url": "https://exemplo.com/as_meninas.jpg",
      "artist_id": 4
    }
    // …
  ]
  ```

---

- ✅ **POST /api/artworks/** – Cria uma nova obra de arte
  ```json
  {
    "title": "Impressão, Nascer do Sol",
    "description": "Pináculo que deu nome ao Impressionismo...",
    "creation_date": "1872-11-13",
    "image_url": "https://exemplo.com/impressao_nascer_sol.jpg",
    "artist_id": 5
  }
  ```
  **Descrição**: Valida se o `artist_id` existe na tabela `Artist`. Se existir, insere um novo registro em `Artwork`.
  **Resposta (201)**:
  ```json
  {
    "id": 3,
    "title": "Impressão, Nascer do Sol",
    "description": "Pináculo que deu nome ao Impressionismo...",
    "creation_date": "1872-11-13",
    "image_url": "https://exemplo.com/impressao_nascer_sol.jpg",
    "artist_id": 5
  }
  ```
  **Erros**:
  - 400: Se o `artist_id` não existir ou se o payload estiver incompleto/ inválido.

---

- 🔍 **GET /api/artworks/{id}** – Retorna uma obra pelo ID
  **Exemplo de URL**: `/api/artworks/2`
  **Descrição**: Busca um registro de `Artwork` por chave primária.
  **Resposta (200)**:
  ```json
  {
    "id": 2,
    "title": "As Meninas",
    "description": "Pintura de Diego Velázquez...",
    "creation_date": "1656-01-01",
    "image_url": "https://exemplo.com/as_meninas.jpg",
    "artist_id": 4
  }
  ```
  **Erros**:
  - 404: Se não existir obra com o `id` informado.

---

- 🔄 **PUT /api/artworks/{id}** – Atualiza uma obra existente
  ```json
  {
    "title": "As Meninas",
    "description": "Obra-prima de Diego Velázquez, Museu do Prado, 1656",
    "creation_date": "1656-01-01",
    "image_url": "https://exemplo.com/as_meninas_atual.jpg",
    "artist_id": 4
  }
  ```
  **Descrição**: Valida se o `artist_id` existe; atualiza campos de `Artwork` de acordo com o `id`.
  **Resposta (200)**:
  ```json
  {
    "id": 2,
    "title": "As Meninas",
    "description": "Obra-prima de Diego Velázquez, Museu do Prado, 1656",
    "creation_date": "1656-01-01",
    "image_url": "https://exemplo.com/as_meninas_atual.jpg",
    "artist_id": 4
  }
  ```
  **Erros**:
  - 404: Se não existir obra com o `id` informado.
  - 400: Se o `artist_id` não for encontrado ou payload inválido.

---

- 🗑 **DELETE /api/artworks/{id}** – Exclui uma obra
  **Exemplo de URL**: `/api/artworks/2`
  **Descrição**: Remove o registro de `Artwork` com o `id` especificado.
  **Resposta (200)**:
  ```json
  {
    "message": "Obra \"As Meninas\" removida com sucesso."
  }
  ```
  **Erros**:
  - 404: Se não existir obra com o `id` informado.

---

### Exposições

- 🔍 **GET /api/exhibitions/** – Lista todas as exposições
  **Descrição**: Recupera todos os registros de `Exhibition`, incluindo as IDs de obras associadas.
  **Resposta (200)**:
  ```json
  [
    {
      "id": 1,
      "name": "Impressionistas de Paris",
      "description": "Mostra dos principais pintores impressionistas do século XIX.",
      "date": "2025-09-15",
      "artwork_ids": [1, 3, 5]
    },
    {
      "id": 2,
      "name": "Arte Barroca",
      "description": "Exposição de obras barrocas europeias.",
      "date": "2025-10-01",
      "artwork_ids": [2, 4]
    }
    // …
  ]
  ```

---

- ✅ **POST /api/exhibitions/** – Cria uma nova exposição
  ```json
  {
    "name": "Renascimento Italiano",
    "description": "Coleção de obras-primas do Renascimento.",
    "date": "2025-11-20",
    "artwork_ids": [6, 7, 8]
  }
  ```
  **Descrição**: Para cada `artwork_id` enviado, verifica se existe obra em `Artwork`. Se todos existirem, cria o registro em `Exhibition` e associa as obras indicadas.
  **Resposta (201)**:
  ```json
  {
    "id": 3,
    "name": "Renascimento Italiano",
    "description": "Coleção de obras-primas do Renascimento.",
    "date": "2025-11-20",
    "artwork_ids": [6, 7, 8]
  }
  ```
  **Erros**:
  - 400: Se qualquer `artwork_id` não for encontrado ou payload inválido.

---

- 🔍 **GET /api/exhibitions/{id}** – Detalha uma exposição pelo ID
  **Exemplo de URL**: `/api/exhibitions/3`
  **Descrição**: Retorna as informações de `Exhibition` correspondentes ao `id`, incluindo a lista de IDs de obras.
  **Resposta (200)**:
  ```json
  {
    "id": 3,
    "name": "Renascimento Italiano",
    "description": "Coleção de obras-primas do Renascimento.",
    "date": "2025-11-20",
    "artwork_ids": [6, 7, 8]
  }
  ```
  **Erros**:
  - 404: Se não existir exposição com o `id` informado.

---

- 🔄 **PUT /api/exhibitions/{id}** – Atualiza uma exposição existente
  ```json
  {
    "name": "Renascimento Italiano – Edição Revisada",
    "description": "Coleção revisitada de obras do Renascimento Italiano.",
    "date": "2025-11-25",
    "artwork_ids": [6, 7, 9]
  }
  ```
  **Descrição**: Busca `Exhibition` por `id`; atualiza `name`, `description`, `date` e associações de obras. Valida existência de cada `artwork_id`.
  **Resposta (200)**:
  ```json
  {
    "id": 3,
    "name": "Renascimento Italiano – Edição Revisada",
    "description": "Coleção revisitada de obras do Renascimento Italiano.",
    "date": "2025-11-25",
    "artwork_ids": [6, 7, 9]
  }
  ```
  **Erros**:
  - 404: Se não existir exposição com o `id` informado.
  - 400: Se algum `artwork_id` não existir ou payload inválido.

---

- 🗑 **DELETE /api/exhibitions/{id}** – Exclui uma exposição
  **Exemplo de URL**: `/api/exhibitions/3`
  **Descrição**: Remove o registro de `Exhibition` e as associações com as obras (tabela auxiliar).
  **Resposta (200)**:
  ```json
  {
    "message": "Exposição \"Renascimento Italiano – Edição Revisada\" removida com sucesso."
  }
  ```
  **Erros**:
  - 404: Se não existir exposição com o `id` informado.

---

> **Observação geral**:
> - Quaisquer métodos **POST**, **PUT** ou **DELETE** (exceto os sob `/api/auth`) exigem que o usuário esteja autenticado (retorna 401 se não estiver logado).
> - Os modelos de payload seguem os campos definidos nos **models** do Flask-RESTX (e são validados automaticamente).
> - As datas devem obedecer ao formato **YYYY-MM-DD**.
> - As rotas de listagem (`GET /api/artists/`, `GET /api/artworks/`, `GET /api/exhibitions/`) retornam arrays JSON dos respectivos objetos mapeados pelo `@marshal_list_with`.
> - Em caso de falha de validação (artista ou obra não encontrada, payload inválido), retorna **400 Bad Request** (ou **404 Not Found**, quando aplicável), com mensagem de erro no JSON.