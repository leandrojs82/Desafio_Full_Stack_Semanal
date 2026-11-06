# Empréstimos de uma Biblioteca

**Desafio #4 · Trilha C — Análise de Dados · Nível iniciante**

## Objetivo

Usar SQL no PostgreSQL para analisar 12 empréstimos fictícios de uma biblioteca. O projeto identifica quais categorias tiveram mais empréstimos e quantos ainda estão em aberto.

## Dados

Cada linha da tabela `emprestimo` representa um empréstimo. Os registros vão de 2 a 7 de novembro de 2026.

| Coluna | Descrição |
|---|---|
| `id` | Identificador único gerado pelo PostgreSQL |
| `categoria` | Categoria do livro |
| `data_emprestimo` | Data em que o livro foi emprestado |
| `devolvido` | `TRUE` para devolvido e `FALSE` para em aberto |

## Como executar

Conecte-se a um banco PostgreSQL local destinado ao exercício. Com a tabela ainda por criar, execute os arquivos nesta ordem:

| Ordem | Arquivo | O que faz |
|---:|---|---|
| 1 | `estrutura.sql` | Cria a tabela `emprestimo` |
| 2 | `dados.sql` | Insere os 12 registros fictícios |
| 3 | `consultas.sql` | Lista os registros por data e ID e calcula as contagens |

Execute `dados.sql` uma vez para evitar duplicar a carga.

## Resultados

| Categoria | Total de empréstimos | Em aberto |
|---|---:|---:|
| Tecnologia | 5 | 3 |
| Literatura | 4 | 2 |
| História | 3 | 1 |
| **Total** | **12** | **6** |

1. Metade dos empréstimos está em aberto, o que corresponde a 6 dos 12 registros.
2. Tecnologia lidera nas duas contagens, com 5 empréstimos no total e 3 em aberto.
3. A base não registra o prazo de devolução, por isso não permite identificar atrasos. Para calcular a duração dos empréstimos encerrados, também seria necessário registrar a data de devolução.

## Conferência dos resultados

A listagem começa com os IDs 1 e 2, ambos de 2 de novembro, seguidos pelo ID 3, de 3 de novembro. A soma dos totais por categoria é 12 e a soma dos empréstimos em aberto é 6, de acordo com as contagens gerais.

## O que pratiquei

- Criar uma tabela com chave primária e campos obrigatórios.
- Inserir registros com datas e valores booleanos.
- Usar `WHERE` para filtrar e `ORDER BY` para ordenar.
- Combinar `COUNT(*)` e `GROUP BY` para comparar categorias.