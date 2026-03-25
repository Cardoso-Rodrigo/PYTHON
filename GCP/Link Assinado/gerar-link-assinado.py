import os
from datetime import timedelta
from google.cloud import storage
from google.oauth2 import service_account


KEY_PATH = r"[caminho da sua chave .json]"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

def gerar_link_assinado(bucket_name, blob_name):
    """Gera uma URL assinada para um arquivo no GCS."""
    try:
        # 2. Carrega as credenciais uma única vez
        creds = service_account.Credentials.from_service_account_file(KEY_PATH)
        client = storage.Client(credentials=creds)

        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # 3. Geração da URL
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=12), #seta o tempo de ativação do link antes de ser desativado
            method="GET"
        )
        return url
    except Exception as e:
        return f"Erro ao gerar link: {e}"

if __name__ == '__main__':
    meu_bucket = 'SEU BUCKET'
    meu_arquivo = 'PASTA_DE_DESTINO/ARQUIVO.EXTENSAO'
    
    link = gerar_link_assinado(meu_bucket, meu_arquivo)

    print(f"Link assinado (válido por 12h):\n{link}")
