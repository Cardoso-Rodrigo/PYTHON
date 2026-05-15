from google.cloud import bigquery

client = bigquery.Client()

sql_query = """
    SUA CONSULTA AQUI!!
"""

# Configura o Dry Run
job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

# Executa a simulação
dry_run_job = client.query(sql_query, job_config=job_config)

# Calcula o tamanho em Gigabytes
bytes_estimados = dry_run_job.total_bytes_processed
gb_estimados = bytes_estimados / (1024 ** 3)

LIMITE_MAXIMO_GB = 5.0

if gb_estimados > LIMITE_MAXIMO_GB:
    print(f"❌ Query CANCELADA! Ela leria {gb_estimados:.2f} GB (Limite: {LIMITE_MAXIMO_GB} GB).")
    # Aqui você pode disparar uma exceção ou um alerta no Slack
else:
    print(f"✅ Query segura. Estimativa: {gb_estimados:.2f} GB. Executando...")
    # Execução real mudando dry_run para False
    job_config.dry_run = False
    client.query(sql_query, job_config=job_config)
