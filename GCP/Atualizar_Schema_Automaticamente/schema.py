from google.cloud import bigquery

client = bigquery.Client()
table_id = "projecto.dataset.tabela"

# Dados de entrada(pode ser adaptado para entrada via df)
# O campo "nova_metrica" é o campo novo
dados = [
    {"id_usuario": 1024, "evento": "click", "nova_metrica": 89.5}
]
try:
    # Configura o carregamento tolerante a mudanças de schema
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        # A mágica acontece aqui: permite adicionar novas colunas automaticamente
        schema_update_options=[
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ],
        # Se o schema mudar, o BigQuery atualiza a tabela antes de inserir
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    # Executa o carregamento dos dados
    load_job = client.load_table_from_json(
        dados, table_id, job_config=job_config
    )
    
    load_job.result()  # Aguarda a finalização

    print("Dados carregados e schema atualizado em produção com sucesso!")
except Exception as e:
    print(f"Um erro foi identificado: {e}")
    
