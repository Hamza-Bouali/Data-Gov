"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/3a377216-7041-41d4-a9e9-e9329b770a65.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()