🚀 Data Pipeline: Prueba Técnica (GCP + BigQuery + Airflow)

Este proyecto consiste en un pipeline de datos que extrae información de una API pública, la carga en una capa de "Sandbox" en Google BigQuery, realiza una transformación idempotente y se orquestaría mediante Apache Airflow.

🛠️ Tecnologías utilizadas
* **Lenguaje:** Python 3.x
* **Nube:** Google Cloud Platform (GCP)
* **Base de Datos:** BigQuery (Capa de datos y transformaciones SQL)
* **Orquestación:** Apache Airflow (Cloud Composer)
* **Repositorio:** GitHub

---

📂 Estructura del Repositorio
* `parte2.py`: Script de Python con clases para la descarga de datos (API) y carga en BigQuery.
* `sql/transform.sql`: Consulta SQL idempotente para la transformación de datos (Sandbox a Integration).
* `dag_test.py`: Definición del DAG de Airflow y operador personalizado `TimeDiffOperator`.

---

⚙️ Pasos realizados

1. Ingesta (Python + API)
Se desarrolló una solución modular con dos clases principales:
- `APIConnector`: Descarga los primeros 100 registros de posts de ejemplo.
- `BQUploader`: Gestiona la conexión y subida de datos a BigQuery mediante `google-cloud-bigquery`.

<img width="712" height="614" alt="Captura de pantalla 2026-03-24 200151" src="https://github.com/user-attachments/assets/86991dec-ad4d-4b68-8c89-24cbdfd3aa70" />



2. Almacenamiento y Transformación (BigQuery)
Los datos se almacenan inicialmente en `SANDBOX_mi_app.raw_data`. Posteriormente, mediante el script `transform.sql`, se procesan e insertan en `INTEGRATION.integration_prueba_tecnica`.
- **Idempotencia:** Se utiliza la sentencia `MERGE` para asegurar que ejecuciones repetidas no dupliquen los datos.

<img width="631" height="256" alt="Captura de pantalla 2026-03-24 200253" src="https://github.com/user-attachments/assets/8e4fe5d2-98ae-4bd1-8825-840b0322261c" />


3. Orquestación (Airflow)
Se diseñó un DAG que incluye:
- Operadores `DummyOperator` para marcar inicio y fin.
- Tareas paralelas generadas dinámicamente.
- Un **Operador Personalizado** (`TimeDiffOperator`) que calcula la diferencia de días entre una fecha dada y el momento de ejecución.

---

**🚀 Cómo ejecutar el proyecto (Resumen)**
1. Configurar una Service Account en GCP con roles de BigQuery Editor y Job User.
2. Descargar el archivo de credenciales y renombrarlo a `credentials.json`.
3. Crear las tablas en BigQuery en los datasets "SANDBOX_my_app" e "INTEGRATION"
4. Ejecutar el script de ingesta en Python.
5. Ejecutar la consulta de transformación en BigQuery con el Merge para asegurar que ejecuciones repetidas no dupliquen los datos.
6. Ejecutar el script en Airflow (Cloud Composer):

1) Crear el entorno
En Google Cloud, busca Composer.
Dale a "Crear entorno" -> Composer 2.
Ponle un nombre (airflow-prueba-técnica) y elige la ubicación más cercana. Nota: Tardará unos 15-20 minutos en crearse.

<img width="1529" height="205" alt="image" src="https://github.com/user-attachments/assets/0a8b7a93-4d79-46c7-92cc-5728bfb7a86f" />

2. Subir el DAG (Tu archivo dag_test.py)
Una vez creado el entorno:
Verás una columna que dice Carpeta de DAGs. Haz clic en el enlace (te llevará a un bucket de Google Cloud Storage).
Dale a Subir archivos y sube el archivo dag_test.py que ya tienes programado.

<img width="1529" height="205" alt="Captura de pantalla 2026-03-24 201126" src="https://github.com/user-attachments/assets/e9befaa3-b44b-4544-a4d0-664635d8b62f" />


Automáticamente, Airflow lo detectará y empezará a ejecutarlo según el horario que pusiste (schedule_interval).


**¿Cómo verificar que el DAG está funcionando?**
Para terminar de completar este apartado de la prueba, sigue estos pasos:

En la Imagen 2, haz clic en el enlace azul que dice "Airflow" (bajo la columna "Webserver de Airflow"). Se abrirá una pestaña nueva con la interfaz propia de Apache Airflow.
Busca en la lista un DAG llamado test (que es el nombre que le pusiste en el código).

<img width="1576" height="512" alt="Captura de pantalla 2026-03-24 201515" src="https://github.com/user-attachments/assets/67da7134-74b8-470c-9402-938d9a4fb364" />


<img width="1564" height="458" alt="Captura de pantalla 2026-03-24 202005" src="https://github.com/user-attachments/assets/f93ed373-7108-406f-a474-78406c7a481e" />


Actívalo: Si ves un interruptor (Toggle) al lado del nombre en "Off", cámbialo a "On".
Mira el gráfico: Haz clic en el nombre test y luego en la pestaña "Graph". Deberías ver la estructura que programaste: start -> tasks -> diff_task -> end.

<img width="1579" height="703" alt="Captura de pantalla 2026-03-25 080154" src="https://github.com/user-attachments/assets/9eed9849-4397-444d-a934-23724ba8311c" />

