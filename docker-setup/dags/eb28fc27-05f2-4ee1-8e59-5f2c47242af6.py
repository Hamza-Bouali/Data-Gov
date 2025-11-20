"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/eb28fc27-05f2-4ee1-8e59-5f2c47242af6.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()