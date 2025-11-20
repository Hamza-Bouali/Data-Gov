"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/a2bab30b-211c-452b-8df6-f2b424c7f43c.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()