"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/d9fa5e58-8893-468b-b687-3beecd7f0010.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()