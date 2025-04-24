import pandas as pd

try:
    df = pd.read_csv("../datasets/nascidos_vivos.csv", encoding='latin1')
    print("Dataset nascidos vivos encontrado com sucesso!")
except FileNotFoundError:
    print("Dataset nascidos vivos não encontrado!")

# Filtrando colunas e eliminando duplicados
df.drop_duplicates(inplace=True)
df = df[['CONSPRENAT', 'CODUFNATU']] 
df.to_csv('nascidos_vivos_limpo.csv')