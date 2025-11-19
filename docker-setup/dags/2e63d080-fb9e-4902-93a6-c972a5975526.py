"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/2e63d080-fb9e-4902-93a6-c972a5975526.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()