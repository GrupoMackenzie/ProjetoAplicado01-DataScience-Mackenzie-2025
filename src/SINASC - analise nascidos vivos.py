import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

try:
    df = pd.read_csv("../datasets/nascidos_vivos_limpo.csv", encoding='latin1')
    print("Dataset nascidos vivos encontrado com sucesso!")
except FileNotFoundError:
    print("Dataset nascidos vivos não encontrado!")
    
#média de consultas prenatal por gestante por UF
media_por_uf = df.groupby('CODUFNATU')['CONSPRENAT'].mean().round(2).reset_index()
media_por_uf.columns = ["UF", "Media_Consultas"]
print("Média de consultas por estado:")
print(media_por_uf.sort_values(by="Media_Consultas", ascending=False))

#Código por unidade federativa
codigo_uf_ibge = {
    12: "Acre", 27: "Alagoas", 13: "Amazonas", 16: "Amapá", 29: "Bahia", 23: "Ceará",
    53: "Distrito Federal", 32: "Espírito Santo", 52: "Goiás", 21: "Maranhão",
    31: "Minas Gerais", 50: "Mato Grosso do Sul", 51: "Mato Grosso", 15: "Pará",
    25: "Paraíba", 26: "Pernambuco", 22: "Piauí", 41: "Paraná", 33: "Rio de Janeiro",
    24: "Rio Grande do Norte", 43: "Rio Grande do Sul", 11: "Rondônia", 14: "Roraima",
    42: "Santa Catarina", 28: "Sergipe", 35: "São Paulo", 17: "Tocantins"
}

# Mapa Temático por Estado
# Carrega a malha geográfica de estados do IBGE
# Fonte alternativa: https://github.com/codeforamerica/click_that_hood/blob/master/public/data/brazil-states.geojson
url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
ufs = gpd.read_file(url)

# Cria a coluna com nome do estado no dataframe de média
media_por_uf["Estado"] = media_por_uf["UF"].map(codigo_uf_ibge)

# Mescla com os dados da geografia
mapa = ufs.merge(media_por_uf, how="left", left_on="name", right_on="Estado")

# Plota o mapa temático solicitado na atividade
plt.figure(figsize=(12, 10))
mapa.plot(column="Media_Consultas", cmap="YlGnBu", legend=True, edgecolor='black')
plt.title("Média de Consultas de \nPré-Natal de nascidos vivos por gestante por Estado (Brasil)", fontsize=15)
plt.axis("off")
plt.show()
