"""
Criado na Quinta Feira 03 de Abril de 2025 às 23:00:00
@author1: Alberto Nagem
Converte todos os arquivos .dbc do SUS expandidos em .dbf na pasta do script
para um único arquivo .csv (all.csv).

Dependências necessárias:
- pandas (para manipular dados) pip install pandas
- dbfread (para ler arquivos .dbf expandidos) pip install dbfread
- keyboard (para usar a tecla ESC) pip install keyboard
"""


import os
import pandas as pd
from dbfread import DBF
import keyboard

def dbf_to_csv():

    # Mensagem inicial com opção de abortar a conversão dos arquivos
    print("Todos os arquivos .dbc expandidos para .dbf serão convertidos e reunidos em apenas um arquivo de nome all.csv")
    print("Por favor Pressione ENTER para continuar ou ESC para sair...")


    while True:
        if keyboard.is_pressed('esc'):
            print("\ncancelado pelo usuário.")
            return
        if keyboard.is_pressed('enter'):
            break

    # Script para obter o diretório onde o software está localizado
    # Obs: eu escrevi ele sempre para trabalhar na raiz da pasta dos arquivos
    script_dir = os.path.dirname(os.path.abspath(__file__))


    all_dfs = []
    processed_files = 0
    failed_files = 0
    total_rows = 0

    print("\nIniciando conversão de arquivos .dbf para all.csv...")

    encodings_to_try = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']

    for filename in sorted(os.listdir(script_dir)):
        if filename.lower().endswith('.dbf'):
            filepath = os.path.join(script_dir, filename)

            print(f"\nProcessando arquivo: {filename}")

            try:
                for encoding in encodings_to_try:
                    try:
                        dbf = DBF(filepath, encoding=encoding, char_decode_errors='replace')
                        df = pd.DataFrame(iter(dbf))

                        if not df.empty:
                            df['ARQUIVO_ORIGEM'] = filename
                            all_dfs.append(df)
                            processed_files += 1
                            total_rows += len(df)
                            print(f"✔️ Convertido com sucesso! Codificação: {encoding}. Linhas: {len(df)}")
                            break
                        else:
                            print(f"⚠️ {filename} está vazio ou não contém dados válidos")
                            failed_files += 1
                            break

                    except Exception as e:
                        if encoding == encodings_to_try[-1]:
                            print(f"❌ Erro ao converter! Todas as codificações falharam")
                            failed_files += 1
                        continue

            except Exception as e:
                print(f"❌ Erro ao converter! Detalhes: {str(e)}")
                failed_files += 1

    if not all_dfs:
        print("\nNenhum arquivo .dbf foi convertido com sucesso.")
        return

    final_df = pd.concat(all_dfs, ignore_index=True)
    output_path = os.path.join(script_dir, "all.csv")
    final_df.to_csv(output_path, index=False, encoding='utf-8', errors='replace')

    print("\nResumo da conversão:")
    print(f"- Arquivos processados com sucesso: {processed_files}")
    print(f"- Arquivos que falharam: {failed_files}")
    print(f"- Linhas totais no arquivo final: {total_rows}")
    print(f"- Arquivo gerado: {output_path}")
    print("\n✅ Conversão concluída!")

if __name__ == "__main__":
    # Instruções para o usuário caso não tenha a biblioteca keyboard
    try:
        dbf_to_csv()
    except ImportError:
        print("\nErro: A biblioteca 'keyboard' não está instalada.")
        print("Para instalar, execute: pip install keyboard")
        print("Obs: Dependendo do seu ambientes, pode ser necessário executar como administrador")