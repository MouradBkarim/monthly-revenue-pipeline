FROM quay.io/astronomer/astro-runtime:11.18.0

# Upgrade root pip
RUN pip install --upgrade pip

# Build one shared venv for Airflow @task.external_python
RUN python -m venv /usr/local/airflow/etl_venv \
    && /usr/local/airflow/etl_venv/bin/pip install --upgrade pip \
    && /usr/local/airflow/etl_venv/bin/pip install \
        -i https://pypi.cloud.soda.io \
        soda-snowflake==1.12.7 \
    && /usr/local/airflow/etl_venv/bin/pip install python-dotenv \
    && /usr/local/airflow/etl_venv/bin/pip install --no-cache-dir dbt-snowflake

