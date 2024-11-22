# Projeto Cloud - 6o Semestre de Engenharia da Computação - INSPER
# Ricardo Wurzmann

Este projeto é uma API RESTful desenvolvida com FastAPI que permite o registro e autenticação de usuários, bem como a consulta a dados externos relacionados a patentes. A aplicação está configurada para utilizar um banco de dados PostgreSQL, onde as credenciais dos usuários são armazenadas. Além disso, a API realiza chamadas a uma API externa para obter informações sobre patentes.

Estrutura do projeto:

📁 app

├── 📄 Dockerfile

├── 📄 main.py

├── 📄 requirements.txt

├── 📄 models.py

├── 📄 requirements.txt

└── 📄 utils.py

📄 docker-compose.yaml

📄 .env


## Como funciona:
- Configuração do Ambiente: 
    O projeto usa um arquivo .env para armazenar variáveis sensíveis, como credenciais do banco de dados.

- Executando a Aplicação: 
    A aplicação é executada dentro de containers Docker, facilitando o gerenciamento de dependências e a consistência entre diferentes ambientes.

- Interação com a API: 
    Os usuários interagem com a API por meio de requisições HTTP. A API valida as requisições, autentica os usuários e retorna os dados solicitados.

## Tecnologias Utilizadas
- FastAPI: Para construir a API RESTful.
- SQLAlchemy: Para interagir com o banco de dados PostgreSQL.
- Pydantic: Para validação de dados.
- Docker: Para containerização da aplicação.
- JWT: Para autenticação de usuários.

## Como executar:
Ter Docker compose instalado na máquina
um arquivo .env na raiz do projeto com:

```
DATABASE_URL=postgresql://user:password@db:5432/mydatabase
POSTGRES_DB=mydatabase
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```

Efetuar: ```docker-compose up -d```

A API estará disponível em http://localhost:8000

## Endpoints API:

- Registro de Usuário (/registrar):
    Permite que novos usuários se registrem fornecendo nome, e-mail e senha.
    As senhas são armazenadas como hashes para garantir a segurança.
    Retorna um token JWT (JSON Web Token) que pode ser usado para autenticação em requisições futuras.

- Login de Usuário (/login):
    Permite que os usuários façam login usando seu e-mail e senha.
    Se as credenciais forem válidas, retorna um token JWT.

- Consulta de Usuários (/usuarios):
    Endpoint protegido que exige um token JWT no cabeçalho de autorização.
    Faz uma chamada para a API externa e retorna um resumo das patentes encontradas.
    API externa retorna aleatoriamente uma pesquisa de patente.


## Screenshots dos Endpoints Testados
Saída POST/registrar:
![Saída POST/registrar](Fotos\foto1.png)

Saída POST/login:
![Saída POST/login](Fotos\foto2.png)

Saída GET/usuarios:
![Saída GET/usuarios](Fotos\foto3.png)

## Vídeo de Execução da Aplicação
[Video aplicação](https://youtu.be/r8JgRR5jRrw)


## Link para o Docker Hub do Projeto
[Repositório Docker Hub](https://hub.docker.com/r/ricardowurzmann/cloud-projeto)


## Compose.yaml
O arquivo docker-compose.yaml está localizado na raiz do projeto.



#AWS:
Abaixo está a parte que configurei meu projeto na AWS
[Video demostrando conhecimento sobre AWS](https://youtu.be/5ntRnw5WX9U)

Os arquivos de configuração do Kubernetes utilizados neste projeto estão disponíveis em [este repositório do GitHub](https://github.com/ricardo-wurzmann/cloud/). Eles incluem as definições de Deployment e Service tanto para a aplicação FastAPI quanto para o banco de dados PostgreSQL.

Após a criação dos documento app.yaml e postgres.yaml (localizados na raíz do projeto) foi feito os seguintes comandos no cloudShell (onde utilizei para configurar):

app.yaml: Contém o Deployment e o Service para a aplicação FastAPI.
    Deployment: Define a imagem Docker, variáveis de ambiente, portas e réplicas.
    Service: Configura um LoadBalancer para expor a aplicação externamente.
    
postgres.yaml: Inclui o Deployment e o Service para o banco de dados PostgreSQL.
    Deployment: Especifica a imagem do PostgreSQL e as credenciais.
    Service: Permite que a aplicação se comunique com o banco de dados dentro do cluster.


kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

