from google.cloud import bigquery
import pandas as pd

path_destino_xlsx = r'C:\bases\Rels\extracaoBQ.xlsx'
colunas_formato_datas=['MES']
colunas_formato_num=['Soma_Quantidade','Soma_Montante']

# Cria o cliente do BigQuery
#Necessario que a chave json para o seu projeto esteja como variavel de ambiente. Caso não esteja é necessario declarar ela nesse ponto.

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\SUA_CHAVE.json"

client = bigquery.Client()

# Query de exemplo
query = """
SELECT  DATE_TRUNC(dt_lancamento, MONTH) MES
        ,SUM(QTDE) as Soma_Quantidade
        ,SUM(MONTANTE) as Soma_Montante
  FROM `tbl_atuais.tbl_atual_mb51`
  WHERE DT_LANCAMENTO >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY), MONTH)
  GROUP BY 1 
  ORDER BY 1 DESC 
"""

# Executa a query
df = client.query(query).to_dataframe()

try:
  # Convertendo as datas para o formato "DD/MM/AAAA"
  for col in colunas_formato_datas:
      df[col] = pd.to_datetime(df[col], errors='coerce')
      df[col] = df[col].dt.strftime("%d/%m/%Y")
  for col in colunas_formato_num:
      df[col] = pd.to_numeric(df[col], errors='coerce')
      df[colunas_formato_num] = df[colunas_formato_num].round(2)
  with pd.ExcelWriter(path_destino_xlsx, engine='xlsxwriter', date_format='DD/MM/YYYY') as writer:
    df.to_excel(writer, sheet_name='extracao_BQ', index=False)
    workbook  = writer.book
    worksheet = writer.sheets['extracao_BQ']

    # FORMATO: Milhar com ponto e decimal com vírgula (Padrão BR)
    formato_br = workbook.add_format({'num_format': '#,##0.00'})
    # Aplicando nas colunas de valor (exemplo: colunas B e C são índices 1 e 2)
    # O i é a posição da coluna no seu DataFrame
    for i, col in enumerate(df.columns):
        if col in colunas_formato_num:
            worksheet.set_column(i, i, 18, formato_br)
  print("Arquivo gerado com sucesso!")
except Exception as e:
  print(f"Foi encontrado um erro no processo: {e}")
