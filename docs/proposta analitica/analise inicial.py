import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Substitua pelo caminho do seu arquivo CSV
caminho_arquivo = 'seuarquivo.csv'

# Leitura do dataset
df = pd.read_csv(caminho_arquivo, encoding='latin1')  # latin1 funciona bem com dados do DATASUS

# Visão geral
print("\nDimensão do dataset:", df.shape)
print("\nAmostra dos dados:")
print(df.head())

# Colunas e tipos
print("\nTipos de dados:")
print(df.dtypes)

# Valores ausentes
print("\nValores ausentes por coluna:")
print(df.isnull().sum())

# Valores únicos por coluna (para detectar variáveis categóricas ou mal formatadas)
print("\nValores únicos por coluna:")
print(df.nunique())

# Estatísticas descritivas para colunas numéricas
print("\nEstatísticas descritivas:")
print(df.describe(include=[np.number]))

# Estatísticas para colunas categóricas
print("\nEstatísticas de colunas categóricas:")
print(df.describe(include=[object]))

# Distribuição de colunas categóricas (até 10 únicas)
for col in df.columns:
    if df[col].nunique() <= 10:
        print(f"\nFrequência da coluna '{col}':")
        print(df[col].value_counts(dropna=False))

# Correlação (numéricas)
numericas = df.select_dtypes(include=[np.number])
if not numericas.empty:
    print("\nMatriz de correlação:")
    print(numericas.corr())

    # Mapa de calor
    sns.heatmap(numericas.corr(), annot=True, cmap='coolwarm')
    plt.title('Mapa de Calor - Correlação')
    plt.show()