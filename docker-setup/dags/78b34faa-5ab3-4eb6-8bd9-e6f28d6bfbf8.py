"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/78b34faa-5ab3-4eb6-8bd9-e6f28d6bfbf8.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()