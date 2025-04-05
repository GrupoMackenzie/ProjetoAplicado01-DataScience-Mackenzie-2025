"""
Created on segunda, 03/Abril 23:50:00 2025
@author1 : Alberto Nagem.
@author2 : <NOME DO(A) AUTOR(A)>
Data da atualização: 05/Abril 2025 "VERSÃO COM ICONES :)"
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd

# Carrega os dados
try:
    df = pd.read_csv("sisprenatal_limpo.csv")
    print("📁 Dados carregados do arquivo local.")
except FileNotFoundError:
    df = pd.read_csv("https://raw.githubusercontent.com/GrupoMackenzie/ProjetoAplicado01-DataScience-Mackenzie-2025/main/datasets/sisprenatal_limpo.csv")
    print("🌐 Dados carregados do GitHub.")

# -------------------------------
# Inf. gerais
# -------------------------------
print("🔍 Dimensões do dataset:", df.shape)
print("\n📊 Tipos de dados:")
print(df.dtypes)
print("\n❓ Valores ausentes por coluna:")
print(df.isnull().sum())

# -------------------------------
# Estatísticas descritivas
# -------------------------------
print("\n📈 Estatísticas descritivas:")
print(df.describe())

# -------------------------------
# Gráficos: distribuição e outliers
# -------------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(16, 5))

# Histograma
plt.subplot(1, 2, 1)
sns.histplot(df["QT_CONSULT"], bins=30, kde=True, color="skyblue")
plt.title("Distribuição da Quantidade de Consultas")
plt.xlabel("QT_CONSULT")
plt.ylabel("Frequência")

# Boxplot
plt.subplot(1, 2, 2)
sns.boxplot(x=df["QT_CONSULT"], color="lightcoral")
plt.title("Boxplot da Quantidade de Consultas")
plt.xlabel("QT_CONSULT")

plt.tight_layout()
plt.show()

# -------------------------------
# Média de consultas por UF
# -------------------------------
media_por_uf = df.groupby("CO_UF_IBGE")["QT_CONSULT"].mean().round(2).reset_index()
media_por_uf.columns = ["UF", "Media_Consultas"]
print("\n📍 Média de consultas por estado:")
print(media_por_uf.sort_values(by="Media_Consultas", ascending=False))

# -------------------------------
# Mapa Temático por Estado
# -------------------------------

# Carrega a malha geográfica de estados do IBGE
# Fonte alternativa: https://github.com/codeforamerica/click_that_hood/blob/master/public/data/brazil-states.geojson
url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
ufs = gpd.read_file(url)

# Ajustei para merge
codigo_uf_ibge = {
    12: "Acre", 27: "Alagoas", 13: "Amazonas", 16: "Amapá", 29: "Bahia", 23: "Ceará",
    53: "Distrito Federal", 32: "Espírito Santo", 52: "Goiás", 21: "Maranhão",
    31: "Minas Gerais", 50: "Mato Grosso do Sul", 51: "Mato Grosso", 15: "Pará",
    25: "Paraíba", 26: "Pernambuco", 22: "Piauí", 41: "Paraná", 33: "Rio de Janeiro",
    24: "Rio Grande do Norte", 43: "Rio Grande do Sul", 11: "Rondônia", 14: "Roraima",
    42: "Santa Catarina", 28: "Sergipe", 35: "São Paulo", 17: "Tocantins"
}

# Cria a coluna com nome do estado no dataframe de média
media_por_uf["Estado"] = media_por_uf["UF"].map(codigo_uf_ibge)

# Mescla com os dados da geografia
mapa = ufs.merge(media_por_uf, how="left", left_on="name", right_on="Estado")

# Plota o mapa temático solicitado na atividade
plt.figure(figsize=(12, 10))
mapa.plot(column="Media_Consultas", cmap="YlGnBu", legend=True, edgecolor='black')
plt.title("Média de Consultas de Pré-Natal por Estado (Brasil)", fontsize=15)
plt.axis("off")
plt.show()
