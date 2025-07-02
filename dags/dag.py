from airflow.decorators import dag, task
from datetime import datetime

from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG, EXECUTION_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig


@dag(
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=['demo'],
    dag_id='monthly_customers_revenu_dag',
    description="Airflow DAG that runs Soda and dbt pipeline for monthly customer revenue"
)
def monthly_customers_revenu_dag():

    # Soda check before transform
    @task.external_python(python='/usr/local/airflow/etl_venv/bin/python')
    def soda_scan_sources(scan_name='soda_scan_sources', checks_subpath='sources', data_source='raw_tpch_data_snowflake'):
        from include.soda.check_function import check
        return check(scan_name, data_source, checks_subpath)


    # I know we tested the source data using Soda, but I also want to demonstrate an alternative approach (for cases where Soda isn’t a requirement).
    @task
    def run_source_tests():
        import subprocess
        subprocess.run([
            "/usr/local/airflow/etl_venv/bin/dbt",
            "test",
            "--project-dir", "/usr/local/airflow/include/dbt",
            "--profiles-dir", "/usr/local/airflow/include/dbt",
            "--profile", "data_pipeline",
            "--target", "dev",
            "--select", "source:tpch"
        ], check=True)

    # Define DbtTaskGroup for dbt_staging
    dbt_staging = DbtTaskGroup(
        group_id='dbt_staging',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        execution_config=EXECUTION_CONFIG,        
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/staging']
        )
    )

    # Define DbtTaskGroup for dbt_intermediate
    dbt_intermediate = DbtTaskGroup(
        group_id='dbt_intermediate',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        execution_config=EXECUTION_CONFIG,        
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/intermediate']
        )
    )

    # Define DbtTaskGroup for dbt_marts
    dbt_marts = DbtTaskGroup(
        group_id='dbt_marts',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        execution_config=EXECUTION_CONFIG,        
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/marts']
        )
    )
    # Soda check after transform(fct_revenue)
    @task.external_python(python='/usr/local/airflow/etl_venv/bin/python')
    def soda_scan_marts(scan_name='soda_check_marts', checks_subpath='marts', data_source='dbt_models_snowflake'):
        from include.soda.check_function import check
        return check(scan_name, data_source, checks_subpath)

    # Define task graph
    soda_load_check = soda_scan_sources()
    dbt_source_tests = run_source_tests()
    soda_post_check = soda_scan_marts()

    soda_load_check >> dbt_source_tests >> dbt_staging >> dbt_intermediate >> dbt_marts >> soda_post_check

# Create Airflow dag:
dag = monthly_customers_revenu_dag()
