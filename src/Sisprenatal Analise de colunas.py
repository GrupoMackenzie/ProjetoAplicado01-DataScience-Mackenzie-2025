"""
Criado na Sexta Feira 04 de Abril de 2025 às 01:44:00
@author1: Alberto Nagem
"""

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/GrupoMackenzie/ProjetoAplicado01-DataScience-Mackenzie-2025/main/datasets/sisprenatal_limpo.csv", encoding="latin1")
print(df.columns)
print(df.head())
