"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/51e09034-6acb-4540-ace8-819e96bc2630.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()