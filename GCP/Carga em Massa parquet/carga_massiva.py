import pandas as pd
from google.cloud import storage
from google.cloud import bigquery

# --- Configurações Iniciais ---
bucket_name = "seu-bucket-de-staging"
nome_arquivo = "dados_grandes.parquet"
gcs_uri = f"gs://{bucket_name}/{nome_arquivo}"
table_id = "seu_projeto.seu_dataset.sua_tabela"

# 1. Simulação: Criando dados no Pandas e salvando localmente em Parquet
# O formato Parquet preserva os tipos de dados e compacta o arquivo
df = pd.DataFrame({"id_usuario": range(1000000), "status": ["ativo", "inativo"] * 500000})
caminho_local = "/tmp/dados.parquet"
df.to_parquet(caminho_local, index=False, engine="pyarrow")

print("💾 Arquivo Parquet gerado localmente.")

# 2. Upload do arquivo Parquet para o Google Cloud Storage (GCS)
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(nome_arquivo)

# Upload eficiente via stream de bytes, sem estourar a memória RAM
blob.upload_from_filename(caminho_local)
print(f"🚀 Arquivo enviado com sucesso para o GCS: {gcs_uri}")

# 3. Disparo do Load Job Nativo no BigQuery
bq_client = bigquery.Client()

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
)

# O BigQuery processa o carregamento na infraestrutura DELE, não na sua máquina
load_job = bq_client.load_table_from_uri(
    gcs_uri, table_id, job_config=job_config
)

load_job.result()  # Aguarda a finalização assíncrona do processo

print("✅ Milhões de linhas carregadas no BigQuery sem estourar a memória!")
