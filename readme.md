# Projeto de Persistência Poliglota e Geoprocessamento

Este projeto demonstra uma abordagem de persistência poliglota, utilizando dois tipos de bancos de dados (SQL e NoSQL) para gerenciar diferentes tipos de dados dentro da mesma aplicação. Além disso, incorpora funcionalidades de geoprocessamento para calcular distâncias e encontrar locais de interesse por proximidade. A interface do usuário é construída com Streamlit, facilitando a interação e visualização dos dados.

## Funcionalidades

- **Cadastro de Cidades**: Armazena dados estruturados (nome, estado) em um banco de dados **SQLite**.
- **Cadastro de Locais de Interesse**: Salva dados semiestruturados (nome, descrição, coordenadas geográficas) em um banco de dados **MongoDB**.
- **Consulta de Locais**: Permite visualizar os locais de interesse cadastrados por cidade, com exibição em um mapa interativo (Folium).
- **Busca por Proximidade**: Dado um ponto de referência (latitude/longitude) e um raio em quilômetros, a aplicação encontra e exibe os locais de interesse mais próximos, calculando a distância e mostrando os resultados em um mapa.
- **Containerização**: O projeto é totalmente containerizado com Docker e orquestrado com Docker Compose, facilitando a configuração e a execução do ambiente.

## Arquitetura e Tecnologias

A aplicação utiliza uma combinação de tecnologias para alcançar seus objetivos:

- [cite_start]**Linguagem**: Python 3.12 [cite: 162]
- [cite_start]**Interface**: Streamlit [cite: 161]
- **Banco de Dados Relacional (SQL)**: SQLite, para armazenar dados estruturados como as cidades.
- **Banco de Dados Não-Relacional (NoSQL)**: MongoDB, ideal para armazenar dados de locais, que podem ter uma estrutura mais flexível.
- [cite_start]**Geoprocessamento**: A biblioteca `geopy` é usada para calcular a distância geodésica entre dois pontos[cite: 161].
- [cite_start]**Visualização de Mapas**: `Folium` e `streamlit-folium` são utilizados para exibir mapas interativos[cite: 161].
- **Containerização**: Docker e Docker Compose.

### Estrutura do Projeto

```
├── app.py                  # Arquivo principal da aplicação Streamlit
├── db_sqlite.py            # Classe de abstração para interações com o SQLite
├── db_mongo.py             # Classe de abstração para interações com o MongoDB
├── geoprocessamento.py     # Funções para cálculos de distância e proximidade
├── requirements.txt        # Dependências do projeto Python
├── Dockerfile              # Define a imagem Docker para a aplicação
├── docker-compose.yml      # Orquestra os serviços da aplicação e do MongoDB
└── sqlite.db               # Arquivo do banco de dados SQLite
```

## Como Executar o Projeto

Certifique-se de ter o **Docker** e o **Docker Compose** instalados em sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-repositorio>
    ```

2.  **Suba os containers:**
    No diretório raiz do projeto, execute o seguinte comando para construir as imagens e iniciar os serviços:
    ```bash
    docker-compose up --build
    ```
    Este comando irá:
    -   Construir a imagem da aplicação Python a partir do `Dockerfile`, instalando todas as dependências listadas no `requirements.txt`.
    -   Baixar e iniciar um container para o banco de dados MongoDB.
    -   Criar uma rede para que os containers possam se comunicar.

3.  **Acesse a aplicação:**
    Abra seu navegador e acesse a URL:
    [http://localhost:8501](http://localhost:8501)

A aplicação Streamlit estará disponível e pronta para uso.

## Detalhes dos Módulos

### `app.py`

É o ponto de entrada da aplicação. Ele define a interface do usuário usando Streamlit, gerencia a navegação entre as diferentes seções (Cadastrar Cidade, Cadastrar Local, etc.) e chama os módulos de banco de dados e geoprocessamento conforme necessário para executar as operações solicitadas pelo usuário.

### `db_sqlite.py`

Fornece uma classe `Database` que abstrai todas as operações com o banco de dados SQLite. Ela inclui métodos para conectar, criar tabelas, inserir, buscar, atualizar e deletar dados, tratando as conexões e cursores de forma segura.

### `db_mongo.py`

Contém a classe `MongoDatabase` para interagir com o MongoDB. Ela simplifica a conexão com o banco, a inserção e a busca de documentos, sendo utilizada para gerenciar os dados dos locais de interesse.

### `geoprocessamento.py`

Responsável pela lógica de geolocalização. A função `calcular_distancia` utiliza a biblioteca `geopy` para determinar a distância em quilômetros entre dois pontos de coordenadas. A função `locais_proximos` filtra uma lista de locais para encontrar aqueles que estão dentro de um raio específico.