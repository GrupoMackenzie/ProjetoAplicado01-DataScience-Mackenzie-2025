"""
Created on Quinta Feira, 03/Abril 23:00:00 2025
@author1 : Alberto Nagem.
@author2 : <NOME DO(A) AUTOR(A)>
Data da atualização: <DATA>"04/Abril/2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", palette="Set2")
plt.rcParams['figure.figsize'] = (12, 6)

# Carregar os dados, se necessário aponte o local do arquivo sisprenatal.csv
try:
    df = pd.read_csv(
        "https://raw.githubusercontent.com/GrupoMackenzie/ProjetoAplicado01-DataScience-Mackenzie-2025/main/datasets/sisprenatal_limpo.csv",
        encoding='latin1',
        dtype={'CO_UF_IBGE': 'int32', 'QT_CONSULT': 'float64'},
        low_memory=False
    )
except Exception as e:
    print(f"Erro ao carregar arquivo: {e}")
    exit()

# Converter QT_CONSULT para numérico "correção de erro de colunas"
df['QT_CONSULT'] = pd.to_numeric(df['QT_CONSULT'], errors='coerce')

# Mapear as Unidades Federativas
uf_map = {
    12: "AC", 27: "AL", 13: "AM", 16: "AP", 29: "BA", 23: "CE", 53: "DF",
    32: "ES", 52: "GO", 21: "MA", 31: "MG", 50: "MS", 51: "MT", 15: "PA",
    25: "PB", 26: "PE", 22: "PI", 41: "PR", 33: "RJ", 24: "RN", 43: "RS",
    11: "RO", 14: "RR", 42: "SC", 28: "SE", 35: "SP", 17: "TO"
}

# Análise de gestantes sem pré-natal "reportou zero como esperado"
sem_prenatal = df[df['QT_CONSULT'] == 0]
estado_zeros = sem_prenatal.groupby('CO_UF_IBGE', observed=True).size().reset_index(name='qtd').sort_values('qtd', ascending=False)
estado_zeros['UF'] = estado_zeros['CO_UF_IBGE'].map(uf_map)

# Gráfico de gestantes sem consultas "removido do código, gráfico vazio"
"""plt.figure()
sns.barplot(x='UF', y='qtd', data=estado_zeros, color='tomato')
plt.title('Quantidade de gestantes sem consultas de pré-natal por estado (2014)')
plt.xlabel('Estado (UF)')
plt.ylabel('Quantidade de gestantes com 0 consultas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

# Cobertura pré-natal "criei uma regra para consultas 1-3 baixa, 4-6 média e 7+ alta
df_com_prenatal = df[df['QT_CONSULT'] >= 1].copy()

# Classificação de cobertura usando pd.cut()
df_com_prenatal['COBERTURA'] = pd.cut(
    df_com_prenatal['QT_CONSULT'],
    bins=[0, 3, 6, float('inf')],
    labels=['Baixa cobertura', 'Média cobertura', 'Alta cobertura'],
    right=True
)

# Print para distribuir as categorias
print("\nDistribuição das categorias de cobertura:")
print(df_com_prenatal['COBERTURA'].value_counts().sort_index())

# Apresenta gráfico da distribuição geral
plt.figure()
sns.countplot(x='COBERTURA', data=df_com_prenatal)
plt.title('Distribuição da Cobertura Pré-Natal')
plt.xlabel('Categoria de Cobertura')
plt.ylabel('Número de Gestantes')
plt.show()

# Análise por estado
cobertura_uf = df_com_prenatal.groupby(['CO_UF_IBGE', 'COBERTURA'], observed=True).size().reset_index(name='qtd')
cobertura_uf['UF'] = cobertura_uf['CO_UF_IBGE'].map(uf_map)  # Garante que a coluna UF existe

# Apresenta o gráfico de proporção por Estado
plt.figure(figsize=(14, 8))
sns.barplot(
    x='UF',
    y='qtd',
    hue='COBERTURA',
    data=cobertura_uf,
    estimator=lambda x: sum(x)/len(cobertura_uf)*100
)
plt.title('Proporção de Cobertura Pré-Natal por Estado (%)')
plt.xlabel('Estado (UF)')
plt.ylabel('Proporção (%)')
plt.xticks(rotation=45)
plt.legend(title='Cobertura')
plt.tight_layout()
plt.show()

# Cálculo de taxas por 100 mil gestantes
total_gestantes_uf = df.groupby('CO_UF_IBGE', observed=True).size().reset_index(name='total_gestantes')
total_gestantes_uf['UF'] = total_gestantes_uf['CO_UF_IBGE'].map(uf_map)

# Juntando os dados e garantindo que todas as colunas necessárias existem
cobertura_com_taxas = pd.merge(
    cobertura_uf,
    total_gestantes_uf,
    on='CO_UF_IBGE'
)
cobertura_com_taxas['taxa_por_100mil'] = round((cobertura_com_taxas['qtd'] / cobertura_com_taxas['total_gestantes']) * 100000, 1)

# Garantir que a coluna UF existe antes de pivotar
if 'UF' not in cobertura_com_taxas.columns:
    cobertura_com_taxas['UF'] = cobertura_com_taxas['CO_UF_IBGE'].map(uf_map)

# Tabela de taxas usando pivot_table com observed=True
tabela_taxas = cobertura_com_taxas.pivot_table(
    index='UF',
    columns='COBERTURA',
    values='taxa_por_100mil',
    aggfunc='first',
    observed=True
).fillna(0).sort_values('Alta cobertura', ascending=False)

print("\nTaxa de cobertura pré-natal por 100 mil gestantes em cada estado:")
print(tabela_taxas.reset_index().to_string(index=False))

# Gráfico comparativo de taxas
plt.figure(figsize=(14, 8))
sns.barplot(
    x='UF',
    y='taxa_por_100mil',
    hue='COBERTURA',
    data=cobertura_com_taxas
)
plt.title('Taxa de Cobertura Pré-Natal por 100 mil gestantes')
plt.xlabel('Estado (UF)')
plt.ylabel('Taxa por 100 mil gestantes')
plt.xticks(rotation=45)
plt.legend(title='Categoria')
plt.tight_layout()
plt.show()

# Tabela resumo com um ranking
tabela_resumo = cobertura_com_taxas.groupby('UF').agg(
    Taxa_Baixa=('taxa_por_100mil', lambda x: x[cobertura_com_taxas['COBERTURA'] == 'Baixa cobertura'].sum()),
    Taxa_Média=('taxa_por_100mil', lambda x: x[cobertura_com_taxas['COBERTURA'] == 'Média cobertura'].sum()),
    Taxa_Alta=('taxa_por_100mil', lambda x: x[cobertura_com_taxas['COBERTURA'] == 'Alta cobertura'].sum())
).reset_index()

tabela_resumo['Ranking Segurança'] = tabela_resumo['Taxa_Alta'].rank(ascending=False, method='min')
tabela_resumo = tabela_resumo.sort_values('Taxa_Alta', ascending=False)

print("\nTabela comparativa com ranking de segurança:")
print(tabela_resumo.to_string(index=False))

# Salvar resultados em Excel para analise posterior _\/_ :-)
try:
    with pd.ExcelWriter('resultados_analise_prenatal.xlsx') as writer:
        tabela_taxas.to_excel(writer, sheet_name='Taxas por UF')
        tabela_resumo.to_excel(writer, sheet_name='Ranking Segurança', index=False)
        estado_zeros.to_excel(writer, sheet_name='Zero Consultas', index=False)
    print("\nResultados salvos em 'resultados_analise_prenatal.xlsx'")
except Exception as e:
    print(f"\nErro ao salvar resultados: {e}")
