# Caixa de Ideias 💡

API para cadastrar e consultar ideias, desenvolvida no
Desafio #3 do programa **Desafio Full Stack Semanal**.

- **Trilha:** Java, Spring Boot e PostgreSQL
- **Nível:** iniciante

## Objetivo

Praticar a construção de uma API REST, desde o recebimento
de uma requisição HTTP até a gravação e consulta dos dados
no PostgreSQL.

## Tecnologias

- Java 21
- Spring Boot
- Spring Web
- Spring Data JPA
- Jakarta Validation
- PostgreSQL 18
- Maven Wrapper
- Visual Studio Code

## Funcionalidades

- Cadastrar uma ideia.
- Listar todas as ideias.
- Consultar uma ideia pelo identificador.
- Validar o título antes do cadastro.
- Manter os registros após reiniciar a aplicação.

Cada ideia possui:

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Long | Identificador gerado pelo banco |
| `titulo` | String | Texto obrigatório de até 100 caracteres |

## Organização do projeto

```text
src/main/
├── java/br/com/desafios/03-caixa_de_ideias/
│   ├── CaixaDeIdeiasApplication.java
│   ├── controller/
│   │   └── IdeiaController.java
│   ├── dto/
│   │   └── CriarIdeiaRequest.java
│   ├── model/
│   │   └── Ideia.java
│   └── repository/
│       └── IdeiaRepository.java
└── resources/
    └── application.properties
```

### Responsabilidades

- **Controller:** recebe requisições HTTP, chama as operações
  necessárias e devolve respostas.
- **DTO:** representa os dados recebidos no cadastro e suas
  regras de validação.
- **Model:** representa a entidade persistida no banco.
- **Repository:** oferece operações para salvar e consultar ideias.

No cadastro, o JSON é convertido em um DTO e validado.
O controller cria a entidade, usa o repository para salvá-la
e devolve a ideia cadastrada na resposta.

## Preparação inicial

### Pré-requisitos

- JDK 21 instalado.
- PostgreSQL instalado.
- VS Code com as extensões:
  - Extension Pack for Java.
  - Spring Boot Extension Pack.

O Maven Wrapper está incluído no projeto.

### Criar o banco

Esta etapa precisa ser feita apenas uma vez.

No PowerShell, conecte ao PostgreSQL:

```powershell
& 'C:\Program Files\PostgreSQL\18\bin\psql.exe' -h localhost -U postgres -d postgres
```

Ajuste o caminho conforme sua instalação e informe a senha
do usuário `postgres`.

No prompt do psql, crie o banco:

```sql
CREATE DATABASE caixa_de_ideias;
```

Se o banco já existir, não é necessário recriá-lo.

Para conectar e conferir:

```text
\c caixa_de_ideias
```

```sql
SELECT current_database(), current_user;
```

Para sair do psql:

```text
\q
```

### Configurar a conexão

Em `src/main/resources/application.properties`:

```properties
spring.application.name=caixa-de-ideias

spring.datasource.url=jdbc:postgresql://localhost:5432/caixa_de_ideias
spring.datasource.username=postgres
spring.datasource.password=${DB_PASSWORD}

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

A senha será informada por variável de ambiente.

A opção `ddl-auto=update` permite que o Hibernate atualize
a estrutura das tabelas a partir das entidades.
Ela é usada aqui para desenvolvimento e estudo local.

## Como iniciar a aplicação no VS Code

### 1. Abrir a pasta correta

Abra a pasta `caixa-de-ideias` que contém os arquivos
`pom.xml` e `mvnw.cmd`.

Depois abra **Terminal → Novo Terminal** e use PowerShell.

### 2. Conferir o serviço PostgreSQL

```powershell
Get-Service -Name 'postgresql-x64-18'
```

O status esperado é `Running`.

Se estiver `Stopped`, abra um PowerShell como administrador:

```powershell
Start-Service -Name 'postgresql-x64-18'
```

Depois volte ao terminal do VS Code.

O nome do serviço pode variar conforme a instalação.

### 3. Selecionar Java 21 para esta sessão

No terminal do VS Code:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-21.0.12'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
```

Ajuste o caminho conforme sua instalação do JDK 21.

Esses comandos valem apenas para o terminal atual e os
programas iniciados por ele. Assim, é possível manter
Java 11 como padrão para os projetos de trabalho.

Confira o Java usado pelo Maven:

```powershell
.\mvnw.cmd -version
```

O resultado deve indicar Java 21.

### 4. Informar a senha do banco

No mesmo terminal:

```powershell
$senhaBanco = Read-Host 'Senha do PostgreSQL' -AsSecureString
$env:DB_PASSWORD = [System.Net.NetworkCredential]::new('', $senhaBanco).Password
Remove-Variable senhaBanco
```

Digite a senha do usuário `postgres`.

Não coloque a senha no código, no README ou no repositório.

### 5. Iniciar

No mesmo terminal:

```powershell
.\mvnw.cmd spring-boot:run
```

Aguarde uma mensagem semelhante a:

```text
Started CaixaDeIdeiasApplication
```

A aplicação atende em:

http://localhost:8080

Para consultar a listagem:

http://localhost:8080/ideias

Para encerrar a aplicação, pressione `Ctrl + C`.

### Ao iniciar em outro dia

1. Confira se o PostgreSQL está rodando.
2. Selecione Java 21 no terminal.
3. Defina novamente `DB_PASSWORD`.
4. Execute `.\mvnw.cmd spring-boot:run`.

A seleção do Java, a definição da senha e a execução
devem acontecer no mesmo terminal.

Não é necessário recriar o banco nem cadastrar novamente
os registros existentes.

## Endpoints

| Método | Caminho | Resultado |
|---|---|---|
| POST | `/ideias` | Cadastra uma ideia e retorna `201` |
| GET | `/ideias` | Retorna `200` e uma lista |
| GET | `/ideias/{id}` | Retorna `200` ou `404` |

### Cadastrar uma ideia

Requisição:

```http
POST /ideias
Content-Type: application/json
```

Corpo:

```json
{
  "titulo": "Criar um organizador de livros"
}
```

Exemplo de resposta com status `201 Created`:

```json
{
  "id": 1,
  "titulo": "Criar um organizador de livros"
}
```

O identificador é gerado pelo banco e pode variar.

### Listar ideias

```http
GET /ideias
```

Exemplo de resposta com status `200 OK`:

```json
[
  {
    "id": 1,
    "titulo": "Criar um organizador de livros"
  }
]
```

Quando não há registros, a resposta é:

```json
[]
```

### Consultar pelo identificador

```http
GET /ideias/1
```

Se a ideia existir, retorna `200 OK` com seus dados.

Se não existir, retorna `404 Not Found`, sem corpo.

## Validação do título

O título:

- É obrigatório.
- Não pode ser vazio.
- Não pode conter apenas espaços.
- Deve ter no máximo 100 caracteres.

Requisições que descumprem essas regras retornam
`400 Bad Request` e não criam registros.

## Exemplo de cadastro pelo PowerShell

Com a aplicação rodando, abra um segundo terminal:

```powershell
$corpo = @{
    titulo = 'Criar um organizador de livros'
} | ConvertTo-Json

$resposta = Invoke-WebRequest `
    -Uri 'http://localhost:8080/ideias' `
    -Method Post `
    -ContentType 'application/json; charset=utf-8' `
    -Body $corpo `
    -UseBasicParsing `
    -ErrorAction Stop

$resposta.StatusCode
$resposta.Content
```

Cada execução bem-sucedida desse comando cadastra uma nova ideia.

## Verificações manuais realizadas

| Cenário | Resultado observado |
|---|---|
| Listar antes do primeiro cadastro | Lista vazia |
| Cadastrar título válido | `201`, com identificador gerado |
| Listar após o cadastro | Ideia cadastrada presente |
| Consultar identificador existente | `200`, com a ideia |
| Consultar identificador inexistente | `404` |
| Cadastrar título vazio | `400` |
| Cadastrar sem título | `400` |
| Cadastrar título com apenas espaços | `400` |
| Cadastrar título com 101 caracteres | `400` |
| Listar após os cadastros inválidos | Nenhum registro adicional |
| Consultar após reiniciar a aplicação | Registro preservado |

Essas verificações foram manuais.
Não foi criada uma suíte de testes automatizados dos endpoints.

## Dificuldades e aprendizado

Minha maior dificuldade foi entender a organização dos pacotes
e a responsabilidade de cada classe. Pratiquei essa separação
criando a entidade, o DTO, o repositório e o controller.

Durante o desenvolvimento, também aprendi a:

- Selecionar Java 21 apenas no terminal do projeto,
  preservando Java 11 para o trabalho.
- Configurar a conexão com PostgreSQL usando variável de ambiente.
- Organizar os pacotes para que o Spring encontre os componentes.
- Mapear URLs com `@GetMapping` e `@PostMapping`.
- Validar dados com `@Valid`, `@NotBlank` e `@Size`.
- Diferenciar os status HTTP `200`, `201`, `400` e `404`.
- Conferir a persistência dos registros após reiniciar.

## Problemas comuns

| Problema | O que conferir |
|---|---|
| `release version 21 not supported` | Confira `JAVA_HOME` e execute `.\mvnw.cmd -version`; o Maven deve usar Java 21 |
| `mvnw.cmd` não encontrado | Abra o terminal na pasta que contém `pom.xml` e `mvnw.cmd` |
| Falha de autenticação | Confira a senha definida em `DB_PASSWORD` no terminal da aplicação |
| Conexão recusada | Confira se o PostgreSQL está rodando e se a porta configurada está correta |
| `404` para uma ideia existente | Confira a URL, `@GetMapping("/{id}")` e se a aplicação foi reiniciada após salvar |
| Porta 8080 ocupada | Confira se outra instância da aplicação continua rodando |

## Escopo

Esta versão oferece cadastro, listagem e consulta por identificador.
Não possui interface gráfica, autenticação, edição ou exclusão.