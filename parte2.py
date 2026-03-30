import pandas as pd
import requests
from google.cloud import bigquery
import os

# 1. Configurar credenciales (Apunta a tu archivo JSON)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

class APIConnector:
    def fetch_data(self):
        # Obtenemos 100 registros de posts de ejemplo
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        return response.json()[:100]

class BQUploader:
    def __init__(self):
        self.client = bigquery.Client()

    def upload(self, data, table_id):
        df = pd.DataFrame(data)
        # Añadir columna de fecha de carga
        df['load_date'] = pd.Timestamp.now()
        
        job = self.client.load_table_from_dataframe(df, table_id)
        job.result()  # Esperar a que termine
        print(f"Cargados {len(df)} registros en {table_id}")

# Ejecución
if __name__ == "__main__":
    api = APIConnector()
    datos = api.fetch_data()
    
    loader = BQUploader()
    loader.upload(datos, "agatangelo-anton-sandbox1.SANDBOX_mi_app.raw_data")
