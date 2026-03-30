from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.models import BaseOperator
from datetime import datetime, timedelta
import logging

# 1. Argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1), # Se cambió 1900 por algo más práctico
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# 4. Operador Personalizado
class TimeDiffOperator(BaseOperator):
    def __init__(self, diff_date, **kwargs):
        super().__init__(**kwargs)
        self.diff_date = diff_date

    def execute(self, context):
        target_date = datetime.strptime(self.diff_date, '%Y-%m-%d')
        now = datetime.now()
        diff = now - target_date
        logging.info(f"La diferencia entre ahora y {self.diff_date} es de {diff.days} días.")

# Definición del DAG
with DAG(
    'test',
    default_args=default_args,
    schedule_interval='0 3 * * *', # 3:00 UTC cada día
    catchup=False
) as dag:

    # 2. Start y End
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # 3. Lista de tareas N (ejemplo con 4 tareas)
    tasks = [DummyOperator(task_id=f'task_{n}') for n in range(4)]
    
    # Lógica: Tareas pares dependen de todas las impares
    odds = [t for i, t in enumerate(tasks) if i % 2 != 0]
    evens = [t for i, t in enumerate(tasks) if i % 2 == 0]

    for even in evens:
        even << odds  # Los pares dependen de los impares

    # 4. Tarea con operador personalizado
    diff_task = TimeDiffOperator(
        task_id='calc_time_diff',
        diff_date='2024-01-01'
    )

    # Orden general: Start -> Tareas -> Diff -> End
    start >> tasks >> diff_task >> end

"""
5. RESPUESTA TEÓRICA:
- Conexión: Es el 'qué' y 'dónde'. Almacena credenciales (host, user, pass, port) en la DB de Airflow.
- Hook: Es el 'cómo'. Es una interfaz de Python que usa la Conexión para hablar con el sistema externo 
  (ej. PostgresHook simplifica hacer SELECT sin escribir todo el código de conexión manual).
"""
