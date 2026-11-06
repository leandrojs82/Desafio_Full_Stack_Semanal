# Guia de revisão — Caixa de Ideias

Desafio #3 · Java, Spring Boot e PostgreSQL · Nível iniciante  
Revisão preparada em 31/10/2026 com base nas etapas da conversa e nas quatro classes consultadas no projeto.

Este guia reúne o que foi construído, por que cada parte existe, como executar novamente e como investigar os problemas encontrados. Os códigos abaixo mantêm o comportamento desenvolvido, com formatação e comentários organizados para estudo. Não é necessário substituir os arquivos que já funcionam.

## 1. O que construímos

Uma API local para cadastrar e consultar ideias. Cada ideia tem um identificador gerado pelo banco e um título obrigatório de até 100 caracteres.

| Método | Endereço | Comportamento |
| --- | --- | --- |
| POST | `/ideias` | Cadastra e retorna `201`; título inválido retorna `400` |
| GET | `/ideias` | Retorna `200` com uma lista, inclusive vazia |
| GET | `/ideias/{id}` | Retorna `200` com a ideia ou `404` se não existir |

Não implementamos edição, exclusão, autenticação ou uma interface gráfica. O navegador foi usado para consultar; o PowerShell foi usado para enviar cadastros e conferir os status.

Uma **API** oferece operações para outros programas. O cliente envia uma **requisição HTTP**, e o servidor devolve uma **resposta HTTP**. A resposta pode conter dados em **JSON**, um formato textual de troca de informações.

```json
{"id":1,"titulo":"Criar um organizador de livros"}
```

## 2. Ferramentas e responsabilidades

| Ferramenta | Papel neste projeto |
| --- | --- |
| JDK 21 | Fornece o Java e o compilador necessários ao projeto |
| VS Code | Editor com suporte a Java e Spring |
| Spring Boot | Configura e inicia a aplicação e o servidor embarcado |
| Spring Web | Oferece os recursos para receber requisições e responder em JSON |
| Spring Data JPA | Fornece a implementação do repositório |
| JPA | Define o modelo de mapeamento entre objetos e dados relacionais |
| Hibernate | Implementa JPA e gera o SQL usado na persistência |
| PostgreSQL Driver | Permite a comunicação Java com PostgreSQL via JDBC |
| Jakarta Validation | Define e verifica regras como título obrigatório |
| PostgreSQL | Armazena os registros de forma persistente |
| Maven | Compila o projeto e gerencia dependências |
| Maven Wrapper | Executa a versão de Maven definida pelo projeto |

O **JDK** inclui o compilador `javac`. O comando `java` executa aplicações. Instalar extensões no editor não substitui o JDK.

No VS Code, usamos **Extension Pack for Java** e **Spring Boot Extension Pack**. O projeto foi gerado pelo comando `Spring Initializr: Create a Maven Project`, com Java 21, empacotamento Jar e as dependências Spring Web, Spring Data JPA, PostgreSQL Driver e Validation.

## 3. Estrutura e pacotes

Depois de remover a subpasta extra gerada pelo assistente, a organização desejada é:

```text
Desafio_Full_Stack_Semanal/
├── README.md
├── 01-gerador-qrcode/
├── 02-analise-despesas/
└── 03-caixa-de-ideias/
    ├── README.md
    ├── pom.xml
    ├── mvnw
    ├── mvnw.cmd
    ├── .mvn/
    └── src/main/
        ├── java/br/com/desafios/caixa_de_ideias/
        │   ├── CaixaDeIdeiasApplication.java
        │   ├── controller/IdeiaController.java
        │   ├── dto/CriarIdeiaRequest.java
        │   ├── model/Ideia.java
        │   └── repository/IdeiaRepository.java
        └── resources/application.properties
```

| Pacote | Responsabilidade |
| --- | --- |
| `model` | Representar a entidade salva no banco |
| `dto` | Representar os dados recebidos no cadastro |
| `repository` | Salvar e consultar entidades |
| `controller` | Receber requisições, acionar operações e devolver respostas |

A primeira linha de um arquivo declara seu pacote. O caminho é contado a partir de `src/main/java`:

```java
package br.com.desafios.caixa_de_ideias.model;
```

Essa declaração corresponde à pasta `br/com/desafios/caixa_de_ideias/model`.

### O problema da pasta model

Inicialmente, `model` estava ao lado de `caixa_de_ideias`, resultando em `br.com.desafios.model`. Movemos a pasta para dentro do pacote da aplicação.

Na configuração padrão do Spring Boot, a localização da classe principal orienta a descoberta dos componentes, entidades e repositórios. Manter esses pacotes abaixo de `br.com.desafios.caixa_de_ideias` permite que sejam encontrados sem configuração adicional.

`import` permite referenciar uma classe de outro pacote pelo nome simples; ele não move o arquivo nem altera seu pacote.

## 4. Entidade: Ideia.java

```java
package br.com.desafios.caixa_de_ideias.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Entity
public class Ideia {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "O título é obrigatório")
    @Size(max = 100, message = "O título deve ter no máximo 100 caracteres")
    private String titulo;

    public Long getId() {
        return id;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }
}
```

### Como ler essa classe

- `public class Ideia`: declara a classe que representa uma ideia.
- `private`: restringe o acesso direto aos atributos, organizando o acesso por métodos.
- `Long`: é o tipo do identificador e permite `null` antes da geração do ID.
- `String`: representa o texto do título.
- `@Entity`: informa ao JPA que essa classe representa dados persistidos.
- `@Id`: identifica a chave primária.
- `@GeneratedValue(strategy = GenerationType.IDENTITY)`: usa a geração de identificador pelo banco.
- `getId()` e `getTitulo()`: permitem consultar os atributos.
- `setTitulo(...)`: permite atribuir um título.

Não criamos `setId`, porque o cliente não precisa escolher o identificador. A entidade do cadastro é construída a partir do DTO e recebe o ID ao ser salva.

```java
this.titulo = titulo;
```

À esquerda, `this.titulo` é o atributo do objeto atual. À direita, `titulo` é o parâmetro recebido pelo método. A atribuição copia a referência do valor recebido para o atributo.

Como não declaramos nenhum construtor, o Java fornece um construtor sem argumentos. É ele que permite `new Ideia()` e atende à necessidade de construção da entidade pelo JPA neste caso. Se adicionarmos construtores futuramente, precisaremos preservar um construtor sem argumentos apropriado ao JPA.

O arquivo consultado tinha um import de `org.hibernate.annotations.Bag` sem uso. Ele não participa da solução e foi omitido desta versão didática.

## 5. DTO: CriarIdeiaRequest.java

```java
package br.com.desafios.caixa_de_ideias.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CriarIdeiaRequest(
    @NotBlank(message = "O título é obrigatório")
    @Size(max = 100, message = "O título deve ter no máximo 100 caracteres")
    String titulo
) {
}
```

**DTO** significa objeto de transferência de dados. Este DTO define o contrato de entrada: no cadastro, esperamos um título, e não um ID escolhido pelo cliente.

Um `record` é uma forma concisa de declarar dados em Java. Para o componente `titulo`, ele fornece o construtor e o método de leitura `titulo()`, além de métodos como `equals`, `hashCode` e `toString`. Não gera `setTitulo`: o componente não pode ser reatribuído após a construção do record.

Compare:

```java
request.titulo();   // Leitura do componente do record.
ideia.getTitulo(); // Leitura pela convenção de getter da entidade.
```

### Regras de validação

| Regra | O que verifica |
| --- | --- |
| `@NotBlank` | Rejeita null, texto vazio e texto formado apenas por espaços em branco |
| `@Size(max = 100)` | Limita o tamanho do texto |

`@Size` sozinho não rejeita `null`; por isso ele complementa `@NotBlank`.

As regras existem no DTO e na entidade. No endpoint, `@Valid` aciona a validação do DTO antes de executar o corpo do método. A entidade também declara restrições que podem ser verificadas no ciclo de persistência. Não confunda essas anotações com garantias SQL: elas não equivalem, por si só, a definir todas as restrições possíveis na tabela.

## 6. Repositório: IdeiaRepository.java

```java
package br.com.desafios.caixa_de_ideias.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import br.com.desafios.caixa_de_ideias.model.Ideia;

public interface IdeiaRepository extends JpaRepository<Ideia, Long> {
}
```

Uma `interface` declara um contrato. `extends JpaRepository` herda operações de persistência; o Spring Data fornece a implementação em execução.

Em `<Ideia, Long>`:

- `Ideia` é a entidade gerenciada.
- `Long` é o tipo de sua chave primária.

Usamos três operações:

| Método | Uso no projeto |
| --- | --- |
| `save(ideia)` | Salvar a nova entidade e obter o resultado com ID |
| `findAll()` | Consultar a lista de ideias |
| `findById(id)` | Consultar uma ideia, que pode não existir |

O corpo da interface fica vazio porque as operações herdadas atendem ao desafio. O Hibernate transforma essas operações em SQL e o driver comunica com PostgreSQL.

## 7. Controller: IdeiaController.java

```java
package br.com.desafios.caixa_de_ideias.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.desafios.caixa_de_ideias.dto.CriarIdeiaRequest;
import br.com.desafios.caixa_de_ideias.model.Ideia;
import br.com.desafios.caixa_de_ideias.repository.IdeiaRepository;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/ideias")
public class IdeiaController {

    private final IdeiaRepository repository;

    public IdeiaController(IdeiaRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Ideia> listar() {
        return repository.findAll();
    }

    @PostMapping
    public ResponseEntity<Ideia> cadastrar(
            @Valid @RequestBody CriarIdeiaRequest request) {

        Ideia ideia = new Ideia();
        ideia.setTitulo(request.titulo());

        Ideia salva = repository.save(ideia);

        return ResponseEntity
                .created(URI.create("/ideias/" + salva.getId()))
                .body(salva);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Ideia> buscarPorId(@PathVariable Long id) {
        return ResponseEntity.of(repository.findById(id));
    }
}
```

### Anotações do controller

| Anotação | Função |
| --- | --- |
| `@RestController` | Declara um controller cujos retornos são escritos na resposta HTTP |
| `@RequestMapping("/ideias")` | Define a base das rotas da classe |
| `@GetMapping` | Liga um método a requisições GET |
| `@PostMapping` | Liga um método a requisições POST |
| `@RequestBody` | Converte o corpo da requisição no objeto esperado |
| `@Valid` | Solicita a validação dos dados recebidos |
| `@PathVariable` | Extrai o valor de uma variável da URL |

O controller não serve somente para exibir informações: recebe entradas, coordena as operações deste projeto e define a resposta HTTP.

### Construtor e injeção de dependência

```java
private final IdeiaRepository repository;

public IdeiaController(IdeiaRepository repository) {
    this.repository = repository;
}
```

O controller precisa de um repositório. O Spring fornece esse objeto pelo construtor: isso é **injeção de dependência pelo construtor**. Com um único construtor, não precisamos de `@Autowired` aqui.

`final` impede reatribuir o campo após sua inicialização; não significa que o banco ou o objeto inteiro sejam imutáveis.

### Listagem

`List<Ideia>` é uma lista de objetos do tipo Ideia. O Spring converte o retorno para JSON. Sem registros, `findAll()` resulta em uma lista vazia, representada por `[]`; isso não é um erro.

### Cadastro, em ordem

1. O cliente envia `POST /ideias` com JSON.
2. O Spring converte o corpo para `CriarIdeiaRequest`.
3. `@Valid` verifica as restrições; falhas resultam em `400` no comportamento usado aqui.
4. O método cria uma entidade com `new Ideia()`.
5. Copia o título do DTO para a entidade.
6. O repositório salva; o banco gera o ID.
7. `created(...)` monta status `201` e o cabeçalho `Location` com o endereço do recurso.
8. `body(salva)` inclui a entidade na resposta JSON.

O DTO não é salvo diretamente. Ele é a entrada; a entidade é o objeto persistido.

### Consulta por ID e Optional

Em `/ideias/1`, `@PathVariable Long id` recebe `1` convertido para Long.

`findById` devolve um `Optional<Ideia>`: ele representa a possibilidade de haver ou não uma ideia. `ResponseEntity.of(...)` devolve `200` com o objeto quando presente, ou `404` sem corpo quando ausente.

### Por que não criamos service?

Neste exercício pequeno, o controller chama o repository diretamente. Uma camada de serviço pode ser útil para regras de negócio mais elaboradas, mas não foi necessária para o escopo construído.

## 8. Configuração do PostgreSQL

O comando `psql --version` inicialmente não foi reconhecido. Isso não provava falta de instalação: encontramos o executável fora do PATH e o serviço parado.

```powershell
# Localiza o cliente no diretório padrão de instalação.
Get-ChildItem -Path 'C:\Program Files\PostgreSQL\*\bin\psql.exe' -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty FullName

# Consulta os serviços relacionados ao PostgreSQL.
Get-Service -Name '*postgres*' -ErrorAction SilentlyContinue
```

O serviço deste ambiente chama-se `postgresql-x64-18`. Para iniciá-lo quando necessário, use PowerShell como administrador:

```powershell
Start-Service -Name 'postgresql-x64-18'
```

Para conectar:

```powershell
& 'C:\Program Files\PostgreSQL\18\bin\psql.exe' -h localhost -U postgres -d postgres
```

O `&` executa o programa cujo caminho entre aspas contém espaços. `-h` informa o servidor, `-U` o usuário e `-d` o banco inicial. Digite a senha do PostgreSQL no prompt, sem compartilhá-la.

### Comandos dentro do psql

```sql
-- Executar somente se o banco ainda não existir.
CREATE DATABASE caixa_de_ideias;
```

```text
\c caixa_de_ideias
```

```sql
SELECT current_database(), current_user;
```

O resultado esperado identifica o banco `caixa_de_ideias` e o usuário `postgres`. Criar um banco não muda a conexão atual; `\c` faz essa troca. Se o banco já existe, basta conectar a ele, sem apagar ou recriar.

Para sair:

```text
\q
```

Comandos SQL, como `SELECT`, terminam com `;`. Os comandos de psql `\c` e `\q` não precisam disso.

## 9. application.properties

```properties
spring.application.name=caixa-de-ideias

spring.datasource.url=jdbc:postgresql://localhost:5432/caixa_de_ideias
spring.datasource.username=postgres
spring.datasource.password=${DB_PASSWORD}

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

| Configuração | Significado |
| --- | --- |
| `localhost:5432` | Endereço e porta do PostgreSQL local |
| `/caixa_de_ideias` | Nome do banco usado pela aplicação |
| `${DB_PASSWORD}` | Lê a senha de uma propriedade de ambiente |
| `ddl-auto=update` | Permite atualizar a estrutura das tabelas neste ambiente de estudo |
| `show-sql=true` | Mostra o SQL no terminal |

`ddl-auto=update` não cria o banco PostgreSQL. Criamos o banco antes; o Hibernate criou a tabela dentro dele. Essa opção é conveniente aqui e não substitui um processo de migrações de banco para outros contextos.

O log enviado confirmou a conexão JDBC e a criação de uma tabela semelhante a:

```sql
create table ideia (
    id bigint generated by default as identity,
    titulo varchar(255),
    primary key (id)
);
```

O limite de 100 do título foi conferido na validação da API. Não conclua que a coluna do banco tem limite 100 só por causa de `@Size`: o log de criação apresentado mostrou `varchar(255)`.

O aviso sobre `open-in-view` não impediu a execução. Mensagens INFO ou WARN devem ser lidas no contexto; não equivalem automaticamente a uma falha.

## 10. Como iniciar amanhã, mantendo Java 11 no trabalho

### Passo 1 — Abra a pasta certa

Abra no VS Code a pasta `03-caixa-de-ideias` que contém `pom.xml` e `mvnw.cmd`. Abra um terminal PowerShell nela.

```powershell
Get-Item .\pom.xml, .\mvnw.cmd
```

Se não encontrar os arquivos, confira `Get-Location` e `Get-ChildItem` antes de executar Maven.

### Passo 2 — Confira o PostgreSQL

```powershell
Get-Service -Name 'postgresql-x64-18'
```

Se estiver parado, inicie como indicado na seção anterior.

### Passo 3 — Selecione Java 21 apenas neste terminal

```powershell
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-21.0.12'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"

.\mvnw.cmd -version
```

O Maven deve informar Java 21. Ajuste o caminho se a instalação mudar.

Esses comandos alteram somente o processo do terminal e os programas iniciados por ele. Não alteram permanentemente as variáveis do Windows. Outros terminais e projetos de trabalho podem continuar com Java 11.

### Passo 4 — Informe a senha

```powershell
$senhaBanco = Read-Host 'Senha do PostgreSQL' -AsSecureString
$env:DB_PASSWORD = [System.Net.NetworkCredential]::new('', $senhaBanco).Password
Remove-Variable senhaBanco
```

A entrada fica oculta; o valor convertido é disponibilizado à aplicação por variável de ambiente. Não grave a senha no README nem no Git. Remover `senhaBanco` não remove `DB_PASSWORD`: esta precisa continuar disponível enquanto o processo da aplicação a utiliza.

### Passo 5 — Inicie no mesmo terminal

```powershell
.\mvnw.cmd spring-boot:run
```

Aguarde `Started CaixaDeIdeiasApplication` e o Tomcat na porta 8080. Consulte:

http://localhost:8080/ideias

Para parar, pressione `Ctrl + C`. Se somente reiniciar no mesmo terminal, as variáveis continuam disponíveis. Em terminal novo, repita a seleção do JDK e a senha. Não recrie o banco.

O ajuste de `JAVA_HOME` descrito aqui é para a execução por terminal. Este roteiro não configura separadamente o botão Run do VS Code.

## 11. Testes manuais no PowerShell

Mantenha a aplicação rodando em um terminal e faça as requisições em outro. O segundo não precisa da senha do banco, pois acessa a API por HTTP.

Usamos `-UseBasicParsing` para evitar o aviso apresentado pelo Windows PowerShell. O acento grave no fim de uma linha continua o comando na seguinte; não acrescente espaços depois dele.

### Cadastrar

```powershell
$corpo = @{ titulo = 'Criar um organizador de livros' } | ConvertTo-Json

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

Esperado: `201` e um JSON com ID e título. O ID pode variar; executar novamente cadastra outra ideia. A aplicação não implementa bloqueio de títulos repetidos.

### Listar

```powershell
$lista = Invoke-WebRequest -Uri 'http://localhost:8080/ideias' -UseBasicParsing -ErrorAction Stop
$lista.StatusCode
$lista.Content
```

Esperado: `200` e uma lista JSON.

### Consultar pelo ID

Use um identificador que apareceu no cadastro ou na listagem:

```powershell
try {
    $consulta = Invoke-WebRequest `
        -Uri 'http://localhost:8080/ideias/1' `
        -UseBasicParsing `
        -ErrorAction Stop

    "Status: $($consulta.StatusCode)"
    $consulta.Content
} catch {
    if ($null -ne $_.Exception.Response) {
        "Status: $([int]$_.Exception.Response.StatusCode)"
    }
    $_.Exception.Message
    $_.ErrorDetails.Message
}
```

Esperado para registro existente: `200`. Troque por um ID não cadastrado, como `999999` no conjunto usado no teste: deve retornar `404`.

### Testar os quatro títulos inválidos

```powershell
$casos = @(
    @{ nome = 'Título vazio'; corpo = @{ titulo = '' } },
    @{ nome = 'Título ausente'; corpo = @{} },
    @{ nome = 'Título com espaços'; corpo = @{ titulo = '   ' } },
    @{ nome = 'Título com 101 caracteres'; corpo = @{ titulo = ('a' * 101) } }
)

foreach ($caso in $casos) {
    $json = ConvertTo-Json -InputObject $caso.corpo -Compress

    try {
        $resultado = Invoke-WebRequest `
            -Uri 'http://localhost:8080/ideias' `
            -Method Post `
            -ContentType 'application/json; charset=utf-8' `
            -Body $json `
            -UseBasicParsing `
            -ErrorAction Stop

        "$($caso.nome): $($resultado.StatusCode)"
    } catch {
        if ($null -ne $_.Exception.Response) {
            "$($caso.nome): $([int]$_.Exception.Response.StatusCode)"
        } else {
            "$($caso.nome): $($_.Exception.Message)"
        }
    }
}
```

Esperado: `400` nos quatro casos e nenhuma ideia adicional na listagem. `foreach` percorre os casos; `ConvertTo-Json` monta o corpo; `try/catch` permite inspecionar a resposta de erro.

### Conferir persistência

1. Cadastre uma ideia e anote o ID.
2. Pare e inicie novamente a aplicação, sem recriar o banco.
3. Consulte a lista e o ID anotado.
4. Confira se os dados continuam disponíveis.

## 12. Evidências obtidas durante o desafio

| Verificação | Resultado informado e revisado |
| --- | --- |
| Compilação e inicialização com Java 21 | Aplicação iniciou na porta 8080 |
| Descoberta do repository | Log encontrou uma interface JPA |
| Conexão e tabela | Log confirmou PostgreSQL e criação da tabela ideia |
| Listagem inicial | `[]` |
| Cadastro válido | `201`, ID 1 e título esperado |
| Listagem após cadastro | Continha a ideia 1 |
| Consulta de ID existente | `200` com a ideia 1 |
| Consulta de ID inexistente | `404` |
| Título vazio, ausente, só espaços ou com 101 caracteres | `400` em todos |
| Ausência de inserções inválidas | Usuário confirmou somente o registro original |
| Persistência após reiniciar | Ideia 1 continuou disponível |

Foram testes manuais. A compilação da classe de teste exibida pelo Maven não é evidência de execução de uma suíte de testes dos endpoints. Não registramos essa suíte como implementada ou executada.

## 13. Erros encontrados e como raciocinamos

### psql não reconhecido

Verificamos a instalação antes de tentar reinstalar. O executável existia; usamos o caminho completo. O serviço estava parado e precisou ser iniciado.

### Falha de autenticação

O PostgreSQL respondeu, mas recusou a senha. Isso diferenciou autenticação de indisponibilidade do servidor. A conexão foi obtida com a senha correta, sem compartilhá-la no chat.

### Banco já existe e conexão ainda em postgres

Criar `caixa_de_ideias` não muda a conexão. Usamos `\c caixa_de_ideias`. A consulta `current_database()` mostrou a diferença entre banco criado e banco atualmente selecionado.

### mvnw.cmd não reconhecido

O terminal estava um nível acima do arquivo. Entramos na pasta correta. Após reorganizar o projeto, o terminal deve ficar diretamente em `03-caixa-de-ideias`, onde está o wrapper.

### release version 21 not supported

Embora `java` e `javac` encontrados no PATH fossem Java 21, o Maven estava usando Java 11 indicado em `JAVA_HOME`.

```powershell
.\mvnw.cmd -version
$env:JAVA_HOME
(Get-Command javac).Source
java -XshowSettings:properties -version 2>&1 | Select-String 'java.home'
```

Esses comandos mostraram qual instalação cada ferramenta usava. Ajustamos Java 21 só no terminal, preservando o ambiente de trabalho com Java 11.

### Ideia não reconhecida ou pacote incorreto

Conferimos a declaração `package`, a localização do arquivo e o `import`. Movemos `model` para baixo do pacote principal. Sugerir um pacote que acompanha a pasta atual não significa que aquela pasta seja a organização desejada para o projeto.

### getMapping não reconhecido

Java diferencia maiúsculas e minúsculas. O correto é `@GetMapping`, com G maiúsculo, e o import correspondente.

### ID existente retornando 404

A listagem mostrava a ideia 1. Ao ler o controller, encontramos ausência de `@GetMapping("/{id}")` no método. Adicionamos a anotação, salvamos, reiniciamos e a consulta retornou `200`.

Um `404` isolado não prova que o registro inexiste: também pode indicar uma rota não mapeada.

### Status 201 mostrado depois de uma consulta que falhou

O PowerShell podia conservar o valor anterior de `$resposta` quando a nova atribuição falhava. Passamos a mostrar os resultados dentro do bloco `try`, e os erros dentro de `catch`, evitando interpretar um resultado antigo como resposta nova.

### Caracteres estranhos na cópia para o chat

Nas mensagens apareceram marcas como `&#x20;`, `*this*` e `List\<Ideia>`. No arquivo Java, usamos `this` e `List<Ideia>` sem essas marcas. A leitura dos arquivos reais confirmou que o código não continha essa formatação do chat.

## 14. Reorganização da pasta

O assistente gerou inicialmente `03-caixa-de-ideias/caixa-de-ideias`. Movendo todo o conteúdo da pasta interna para a externa, a raiz Maven passou a ser `03-caixa-de-ideias`.

Para essa operação: pare a aplicação, inclua arquivos ocultos, preserve `.mvn`, `.gitignore` e os demais arquivos e confira conflitos antes de substituir qualquer coisa. Reabra a nova raiz no VS Code e ajuste as instruções do README. Não é necessário mudar os pacotes Java, o artifactId ou o banco só por mover a raiz do projeto.

Os registros ficam no PostgreSQL, não dentro da pasta `target` nem na pasta do código.

## 15. Documentação e publicação no GitHub

O README do desafio registra objetivo, tecnologias, estrutura, execução, endpoints, testes e dificuldades. O README da raiz reúne os três projetos e aponta para suas pastas.

Para revisar e publicar a partir da raiz do repositório:

```powershell
cd 'C:\Users\Dev\Documents\LEANDRO\Desafio_Full_Stack_Semanal'

git status
git remote -v
```

O remoto informado foi `https://github.com/leandrojs82/Desafio_Full_Stack_Semanal.git`. Adicione `origin` somente se ainda não existir:

```powershell
git remote add origin https://github.com/leandrojs82/Desafio_Full_Stack_Semanal.git
```

O `.gitignore` do projeto deve ignorar `target/` e `.env`. Um `.gitignore` não remove arquivos que já estavam sendo rastreados; confira o que realmente entrou no commit. Não envie senha real em nenhum arquivo.

```powershell
git add README.md 03-caixa-de-ideias/

git diff --cached --stat
git diff --cached

git commit -m "Adiciona desafio 03: API Caixa de Ideias"
git push -u origin HEAD
```

`add` prepara, `diff --cached` revisa os arquivos preparados, `commit` registra localmente e `push` envia a branch atual. Os comandos foram orientados na conversa; não houve confirmação de publicação bem-sucedida. Se houver conflito ou rejeição, leia a mensagem antes de tentar outro comando; não é necessário usar push forçado neste roteiro.

## 16. Perguntas para revisar sem olhar o código

1. O que o controller faz além de devolver informações?
2. Por que o DTO de cadastro não tem ID?
3. Qual a diferença entre `request.titulo()` e `ideia.getTitulo()`?
4. O que significa `this.titulo = titulo`?
5. O que representa `JpaRepository<Ideia, Long>`?
6. O que `findById` devolve quando não encontra a ideia?
7. Como se combinam `/ideias` e `/{id}`?
8. Por que precisamos de `@Valid` no parâmetro do cadastro?
9. Por que `@Size` não substitui `@NotBlank`?
10. Como manter Java 11 no trabalho e usar Java 21 neste projeto?
11. Por que reiniciar a aplicação não apaga as ideias?
12. O que diferencia `200`, `201`, `400` e `404`?

### Respostas para conferência

1. Recebe e interpreta requisições, coordena as operações e devolve a resposta HTTP.
2. O cadastro aceita o título; o banco gera o identificador.
3. O primeiro é o acessor gerado pelo record; o segundo é um getter escrito na entidade.
4. Atribui ao atributo do objeto o valor recebido como parâmetro.
5. Repositório de entidades Ideia com chave do tipo Long.
6. Um Optional vazio; neste controller ele se transforma em resposta 404.
7. A rota da classe e a do método formam `/ideias/{id}`.
8. Para solicitar a validação do DTO antes da execução do cadastro.
9. Tamanho máximo não garante presença nem rejeita somente espaços.
10. Definir JAVA_HOME e PATH somente no terminal usado para executar o desafio.
11. Os dados estão persistidos no PostgreSQL e não apenas na memória da aplicação.
12. Sucesso da consulta; recurso criado; entrada inválida; recurso não encontrado.

## 17. Leituras usadas no programa

Os links abaixo foram verificados quando o desafio foi apresentado, em 26/10/2026. Servem como material complementar; este guia se baseia também no código e nas evidências da implementação.

- [Métodos HTTP — MDN, em português](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Methods).
- [Spring REST — guia oficial](https://spring.io/guides/gs/rest-service/).
- [Spring Data JPA — guia oficial](https://spring.io/guides/gs/accessing-data-jpa/). O exemplo usa H2; nosso projeto utiliza PostgreSQL.
- [PostgreSQL — criação de tabelas](https://www.postgresql.org/docs/current/tutorial-table.html).
- [PostgreSQL — consultas SELECT](https://www.postgresql.org/docs/current/tutorial-select.html).
- [Spring Boot no VS Code](https://code.visualstudio.com/docs/java/java-spring-boot), consultado durante a configuração.

Para revisar, comece pelo fluxo do cadastro, explique as quatro classes com suas palavras e execute novamente os testes manuais. Use os erros registrados para praticar diagnóstico: leia a mensagem, confira qual componente falhou e só depois altere a configuração ou o código.
