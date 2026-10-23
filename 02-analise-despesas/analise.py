# Importa a biblioteca pandas.
# "as pd" cria o apelido "pd", usado por convenção em projetos de dados.
import pandas as pd


# pd.read_csv() lê o arquivo CSV e transforma os dados
# em um DataFrame, que funciona como uma tabela do pandas.
despesas = pd.read_csv("despesas.csv")


# head() mostra as cinco primeiras linhas do DataFrame.
# É útil para conferir rapidamente se o arquivo foi lido corretamente.
print("Primeiras cinco despesas:")
print(despesas.head())


# Exibe todos os registros originais.
# Esta variável não será alterada durante a limpeza.
print("\nTabela original completa:")
print(despesas)


# info() apresenta informações como:
# - quantidade de linhas e colunas;
# - quantidade de valores preenchidos;
# - tipo de dado de cada coluna.
print("\nInformações das colunas:")
despesas.info()


# isna() identifica valores ausentes, retornando True ou False.
# sum() soma os valores True e informa quantas ausências existem
# em cada coluna.
print("\nValores ausentes por coluna:")
print(despesas.isna().sum())


# copy() cria uma cópia independente do DataFrame original.
# A limpeza será realizada nessa cópia.
despesas_limpas = despesas.copy()


# len() conta quantas linhas existem no DataFrame.
quantidade_antes = len(despesas_limpas)


# drop_duplicates() remove registros repetidos.
# subset=["id"] define que a coluna "id" será usada
# para identificar as duplicatas.
despesas_limpas = despesas_limpas.drop_duplicates(
    subset=["id"]
)


# Conta quantas linhas restaram depois da remoção.
quantidade_depois = len(despesas_limpas)


# A subtração mostra quantas duplicatas foram removidas.
duplicatas_removidas = quantidade_antes - quantidade_depois

print("\nRegistros duplicados removidos:")
print(duplicatas_removidas)

print("\nTabela sem ids duplicados:")
print(despesas_limpas)


# Seleciona apenas a coluna "categoria".
# isna().sum() conta quantas categorias estão ausentes
# antes do preenchimento.
categorias_ausentes = (
    despesas_limpas["categoria"].isna().sum()
)


# fillna() substitui valores ausentes.
# Neste caso, as categorias desconhecidas recebem
# o texto "Sem categoria".
despesas_limpas["categoria"] = (
    despesas_limpas["categoria"].fillna("Sem categoria")
)

print("\nCategorias preenchidas:")
print(categorias_ausentes)

print("\nAusências depois do preenchimento da categoria:")
print(despesas_limpas.isna().sum())


# Conta quantas despesas não possuem um valor conhecido.
valores_ausentes = despesas_limpas["valor"].isna().sum()


# dropna() remove linhas que possuem valores ausentes.
# subset=["valor"] limita a verificação à coluna "valor".
#
# A linha do Suco será retirada apenas dos cálculos.
# Ela continua preservada nas tabelas "despesas"
# e "despesas_limpas".
despesas_validas = despesas_limpas.dropna(
    subset=["valor"]
)


print("\nDespesas excluídas dos cálculos:")
print(valores_ausentes)

print("\nQuantidade de despesas válidas:")
print(len(despesas_validas))

print("\nDespesas utilizadas nos cálculos:")
print(despesas_validas)


# Seleciona a coluna "valor".
# sum() soma todos os valores conhecidos.
total_gasto = despesas_validas["valor"].sum()


# A letra "f" antes da string permite inserir variáveis
# dentro do texto usando chaves.
#
# :.2f formata o número com duas casas decimais.
print(f"\nTotal gasto conhecido: R$ {total_gasto:.2f}")

# Seleciona a coluna "valor" das despesas válidas.
# mean() calcula a média aritmética:
# soma dos valores dividida pela quantidade de valores.
media_despesas = despesas_validas["valor"].mean()

# Exibe a média formatada com duas casas decimais.
print(f"Média por despesas válida: R$ {media_despesas:.2f}")

# groupby("categoria") reúne as despesas que possuem
# a mesma categoria.
#
# ["valor"] seleciona a coluna que será calculada.
#
# sum() soma os valores dentro de cada categoria.
total_por_categoria = (
    despesas_validas
    .groupby("categoria")["valor"]
    .sum()
)

# Exibe o resultado do agrupamento.
print("\nTotal gasto por categoria:")
print(total_por_categoria)

# Importa o módulo de gráficos da biblioteca matplotlib.
# "plt" é o apelido usado por convenção.
import matplotlib.pyplot as plt

# Cria uma área para o gráfico.
# figsize define a largura e a altura da imagem em polegadas.
figura, eixo = plt.subplots(figsize=(9, 5))

# Cria o gráfico de barras.
#
# total_por_categoria.index contém os nomes das categorias.
# total_por_categoria.values contém os respectivos valores.
barras = eixo.bar(
    total_por_categoria.index,
    total_por_categoria.values,
    color="steelblue"
)

# Define o título apresentado acima do gráfico.
eixo.set_title("Total de gastos por categoria")

# Define os textos dos eixos horizontal e vertical.
eixo.set_xlabel("Categoria")
eixo.set_ylabel("Valor gasto (R$)")

# Percorre cada barra e seu respectivo valor.
# zip() combina as duas listas para que sejam percorridas juntas.
for barra, valor in zip(barras, total_por_categoria.values):
    # Percorre cada barra e seu respectivo valor.
    # zip() combina as duas listas para que sejam percorridas juntas.
    # get_height() informa a altura da barra.
    eixo.text(
        barra.get_x() + barra.get_width()/2,
        barra.get_height(),
        f"R$ {valor:.2f}",
        ha="center",
        va="bottom"
    )

# Ajusta automaticamente os espaços do gráfico
# para evitar que os textos sejam cortados.
plt.tight_layout()

# Salva o gráfico como uma imagem dentro da pasta do projeto.
# dpi=150 define uma boa resolução para visualização.
plt.savefig("gastos_por_categoria.png", dpi=150)

# Abre uma janela para mostrar o gráfico.
plt.show()