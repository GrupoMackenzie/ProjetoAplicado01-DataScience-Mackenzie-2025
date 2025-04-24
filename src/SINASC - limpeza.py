import pandas as pd

try:
    df = pd.read_csv("../datasets/nascidos_vivos.csv", encoding='latin1')
    print("Dataset nascidos vivos encontrado com sucesso!")
except FileNotFoundError:
    print("Dataset nascidos vivos não encontrado!")
#média de consultas prenatal por gestante por UF
df = df[['CONSPRENAT', 'CODUFNATU']] # Filtrando colunas
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df.to_csv('nascidos_vivos.csv')