"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/2bf7d3d2-003f-4ac5-8001-5658972f9832.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()