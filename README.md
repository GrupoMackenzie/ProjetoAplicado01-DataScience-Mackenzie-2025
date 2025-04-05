{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![Banner](https://github.com/user-attachments/assets/bce12192-a20a-4cf4-a5f5-7e7f445aecaf)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "446eb0cb",
   "metadata": {},
   "source": [
    "# 📊 Análise dos Dados do SISPRENATAL\n",
    "Este notebook tem como objetivo consolidar a análise exploratória realizada com base no banco de dados do SISPRENATAL, utilizando scripts previamente desenvolvidos.\n",
    "---\n",
    "**Seções:**\n",
    "1. Análise de colunas e estrutura do dataset\n",
    "2. Análise preliminar 2\n",
    "3. Análise final com tratamentos e conclusões"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2b3092cb",
   "metadata": {},
   "source": [
    "## 🔍 Parte 1 – Análise de Colunas\n",
    "Nesta seção, analisamos as colunas do dataset original do SISPRENATAL para entender melhor os dados disponíveis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1fa83fa5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "# Caminho do arquivo (ajuste conforme necessário)\n",
    "caminho_arquivo = '../datasets/SISPRENATAL.csv'\n",
    "# Leitura do dataset\n",
    "df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4cc1f98f",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e9b60b70",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b387f28",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.nunique().sort_values()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d8931ae7",
   "metadata": {},
   "source": [
    "## 🧪 Parte 2 – Análise Preliminar 2\n",
    "Análises estatísticas iniciais e observações específicas por colunas selecionadas."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f3165797",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['IDADEGESTANTE'].describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4389c705",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['RACACOR'].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8220bd76",
   "metadata": {},
   "outputs": [],
   "source": [
    "pd.crosstab(df['ESCMAE'], df['RACACOR'], margins=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b3cca674",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['CONSULTAS'].value_counts().sort_index()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f7e69255",
   "metadata": {},
   "source": [
    "## 🧠 Parte 3 – Análise Final\n",
    "Nesta seção, aplicamos tratamentos finais nos dados, analisamos relações importantes e preparamos os primeiros insights."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9f4c0372",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_filtrado = df[(df['IDADEGESTANTE'] >= 10) & (df['IDADEGESTANTE'] <= 50)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a87ff88c",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_filtrado[['IDADEGESTANTE', 'CONSULTAS']].corr()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "67d50684",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "plt.scatter(df_filtrado['IDADEGESTANTE'], df_filtrado['CONSULTAS'])\n",
    "plt.xlabel('Idade da Gestante')\n",
    "plt.ylabel('Consultas Pré-Natal')\n",
    "plt.title('Consultas x Idade')\n",
    "plt.grid(True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dafc4bb2",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['ESCMAE'] = df['ESCMAE'].fillna('Ignorado')\n",
    "df['ESCMAE'].value_counts()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "89c17601",
   "metadata": {},
   "source": [
    "## ✅ Conclusão\n",
    "Este notebook consolidou a análise dos dados do SISPRENATAL com base em três scripts:\n",
    "- Avaliação geral das colunas e estrutura\n",
    "- Estatísticas descritivas iniciais\n",
    "- Tratamentos finais para extração de insights\n\n",
    "📌 **Próximos Objetivos:**\n",
    "- Aplicar modelos preditivos\n",
    "- Gerar dashboards interativos\n",
    "- Apresentar visualizações segmentadas por região, idade ou escolaridade"
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
