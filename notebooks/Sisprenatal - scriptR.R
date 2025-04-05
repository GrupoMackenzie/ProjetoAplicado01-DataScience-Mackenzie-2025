#Created on Sexta Feira, 04/Abril 12:00:00 2025
#@author1 : Alberto Nagem.
#@author2 : <NOME DO(A) AUTOR(A)>
#Data da atualização: <DATA>"04/Abril/2025 17:00:00

# Carrega os pacotes necessários:
library(readr)

# Lê o CSV "se necessário refazer o apontamento para o sisprenatal.csv"
setwd("https://raw.githubusercontent.com/GrupoMackenzie/ProjetoAplicado01-DataScience-Mackenzie-2025/main/datasets/sisprenatal_limpo.csv")
df <- read_csv("sisprenatal.csv", locale = locale(encoding = "Latin1"))

# Corrige/converte a coluna QT_CONSULT para numérico
df$QT_CONSULT <- as.numeric(df$QT_CONSULT)

# Vê as 5 primeiras linhas
head(df)

# Obtem os nomes das colunas
names(df)

# Instala todos os pacotes se necessário
# install.packages("ggplot2")
# install.packages("dplyr")
# install.packages("readr")

library(ggplot2)
library(dplyr)
library(readr)

# Lê o CSV "ajuste o encoding se necessário"
df <- read_csv("sisprenatal.csv", locale = locale(encoding = "Latin1"))

# Corrige novamente após a segunda leitura
df$QT_CONSULT <- as.numeric(df$QT_CONSULT)

# Filtra gestantes com 0 consultas
sem_prenatal <- df %>% filter(QT_CONSULT == 0)

# Agrupar por estado
estado_zeros <- sem_prenatal %>%
  group_by(CO_UF_IBGE) %>%
  summarise(qtd = n()) %>%
  arrange(desc(qtd))

# Mapeia códigos de Unidades Federativas para siglas
uf_map <- c(
  "12" = "AC", "27" = "AL", "13" = "AM", "16" = "AP", "29" = "BA", "23" = "CE", "53" = "DF",
  "32" = "ES", "52" = "GO", "21" = "MA", "31" = "MG", "50" = "MS", "51" = "MT", "15" = "PA",
  "25" = "PB", "26" = "PE", "22" = "PI", "41" = "PR", "33" = "RJ", "24" = "RN", "43" = "RS",
  "11" = "RO", "14" = "RR", "42" = "SC", "28" = "SE", "35" = "SP", "17" = "TO"
)

estado_zeros$UF <- uf_map[as.character(estado_zeros$CO_UF_IBGE)]

# Gráfico
ggplot(estado_zeros, aes(x = reorder(UF, -qtd), y = qtd)) +
  geom_bar(stat = "identity", fill = "tomato") +
  labs(
    title = "Quantidade de gestantes sem consultas de pré-natal por estado (2014)",
    x = "Estado (UF)",
    y = "Quantidade de gestantes com 0 consultas"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# ------------------------------------------------------------------------------
# NOVA ANÁLISE "CLASSIFICAÇÃO DE COBERTURA PRÉ-NATAL"
# ------------------------------------------------------------------------------

# Filtrar apenas gestantes com pelo menos 1 consulta
df_com_prenatal <- df %>% filter(QT_CONSULT >= 1)

# Cria a classificação de cobertura que eu quero:
# 1-3 consultas = Baixa cobertura
# 4-6 consultas = Média cobertura
# 7+ consultas = Alta cobertura
df_com_prenatal <- df_com_prenatal %>%
  mutate(
    COBERTURA = case_when(
      QT_CONSULT <= 3 ~ "Baixa cobertura",
      QT_CONSULT <= 6 ~ "Média cobertura",
      TRUE ~ "Alta cobertura"  # Caso contrário (7+)
    ),
    COBERTURA = factor(COBERTURA, levels = c("Baixa cobertura", "Média cobertura", "Alta cobertura"))
  )

# Visualiza a distribui todas categorias
print("Distribuição das categorias de cobertura:")
table(df_com_prenatal$COBERTURA)

# Apresentar Gráfico de barras da distribuição
ggplot(df_com_prenatal, aes(x = COBERTURA)) +
  geom_bar(fill = "steelblue") +
  labs(
    title = "Distribuição da Cobertura Pré-Natal",
    x = "Categoria de Cobertura",
    y = "Número de Gestantes"
  ) +
  theme_minimal()

# ------------------------------------------------------------------------------
# Análise por estado - seguindo o mesmo padrão do meu código original
# ------------------------------------------------------------------------------

cobertura_uf <- df_com_prenatal %>%
  group_by(CO_UF_IBGE, COBERTURA) %>%
  summarise(qtd = n(), .groups = 'drop') %>%
  mutate(UF = uf_map[as.character(CO_UF_IBGE)])

# Gráfico de barras "proporção por estado"
ggplot(cobertura_uf, aes(x = UF, y = qtd, fill = COBERTURA)) +
  geom_bar(position = "fill", stat = "identity") +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title = "Proporção de Cobertura Pré-Natal por Estado",
    x = "Estado (UF)",
    y = "Proporção",
    fill = "Cobertura"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# ------------------------------------------------------------------------------
# Atualização: CÁLCULO DE TAXAS POR 100 MIL GESTANTES
# ------------------------------------------------------------------------------

# Calcula o total de gestantes por estado
total_gestantes_uf <- df %>%
  group_by(CO_UF_IBGE) %>%
  summarise(total_gestantes = n()) %>%
  mutate(UF = uf_map[as.character(CO_UF_IBGE)])

# Junta os dados de cobertura e corrige os nomes das colunas
cobertura_com_taxas <- cobertura_uf %>%
  mutate(CO_UF_IBGE = as.numeric(CO_UF_IBGE)) %>%
  left_join(total_gestantes_uf, by = "CO_UF_IBGE") %>%
  rename(UF = UF.y) %>%  # Usar UF.y que veio do join
  select(-UF.x) %>%     # Remover a coluna UF.x se ela existir
  mutate(
    taxa_por_100mil = round((qtd / total_gestantes) * 100000, 1)
  )

# 3. Cria a tabela pivotada
tabela_taxas <- cobertura_com_taxas %>%
  select(UF, COBERTURA, taxa_por_100mil) %>%
  spread(key = COBERTURA, value = taxa_por_100mil) %>%
  arrange(desc(`Alta cobertura`))

# Visualizar a tabela
print("Taxa de cobertura pré-natal por 100 mil gestantes em cada estado:")
print(as.data.frame(tabela_taxas))

# Gráfico comparativo
ggplot(cobertura_com_taxas, aes(x = reorder(UF, -taxa_por_100mil), y = taxa_por_100mil, fill = COBERTURA)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title = "Taxa de Cobertura Pré-Natal por 100 mil gestantes",
    subtitle = "Comparação ajustada por população de gestantes",
    x = "Estado (UF)",
    y = "Taxa por 100 mil gestantes",
    fill = "Categoria"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Tabela resumo com um ranking
tabela_resumo <- cobertura_com_taxas %>%
  group_by(UF) %>%
  summarise(
    `Taxa Baixa` = sum(taxa_por_100mil[COBERTURA == "Baixa cobertura"]),
    `Taxa Média` = sum(taxa_por_100mil[COBERTURA == "Média cobertura"]),
    `Taxa Alta` = sum(taxa_por_100mil[COBERTURA == "Alta cobertura"]),
    .groups = 'drop'
  ) %>%
  mutate(
    `Ranking Segurança` = rank(-`Taxa Alta`, ties.method = "min")
  ) %>%
  arrange(desc(`Taxa Alta`))

print("Tabela comparativa com ranking de segurança:")
print(as.data.frame(tabela_resumo))

