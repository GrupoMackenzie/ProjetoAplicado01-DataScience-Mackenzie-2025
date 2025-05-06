import pandas as pd
from dbfread import DBF

# Caminho do sisnasc
arquivo_dbf = '../datasets/nascidos_vivos_2014.dbf'

# Carrega extenção DBF
dbf = DBF(arquivo_dbf, encoding='latin1')
df = pd.DataFrame(iter(dbf))
df = df[['CODMUNRES', 'CONSPRENAT', 'IDANOMAL', 'IDADEMAE', 'ESCMAE', 'RACACOR', 'ESTCIVMAE']]

df.to_csv('nascidos_vivos_limpo.csv')