from cosmos.config import ProfileConfig, ProjectConfig, ExecutionConfig
from pathlib import Path

import os

# Generate profiles.yml
profile_yml_content = f"""
data_pipeline:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: {os.getenv('SNOWFLAKE_ACCOUNT')}
      user: {os.getenv('SNOWFLAKE_USER')}
      password: {os.getenv('SNOWFLAKE_PASSWORD')}
      warehouse: {os.getenv('DST_SNOWFLAKE_WAREHOUSE')}
      database: {os.getenv('DST_SNOWFLAKE_DATABASE')}
      schema: {os.getenv('DST_SNOWFLAKE_SCHEMA')}
      role: {os.getenv('DST_SNOWFLAKE_ROLE')}
      threads: 10
"""

with open('/usr/local/airflow/include/dbt/profiles.yml', 'w') as f:
    f.write(profile_yml_content)


DBT_CONFIG = ProfileConfig(
    profile_name='data_pipeline',
    target_name='dev',
    profiles_yml_filepath=Path('/usr/local/airflow/include/dbt/profiles.yml')
)

DBT_PROJECT_CONFIG = ProjectConfig(
    dbt_project_path='/usr/local/airflow/include/dbt/',
)

EXECUTION_CONFIG = ExecutionConfig(
    dbt_executable_path="/usr/local/airflow/etl_venv/bin/dbt"
)