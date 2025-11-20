"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/4e5a1326-f7c8-455c-917b-17d7f26c1397.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()