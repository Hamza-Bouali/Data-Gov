"""
This file has been generated from dag_runner.j2
"""
from airflow import DAG
from openmetadata_managed_apis.workflows import workflow_factory

workflow = workflow_factory.WorkflowFactory.create("/opt/airflow/dag_generated_configs/95fc1357-aba8-46ff-8daf-b95c0ccf3b2d.json")
workflow.generate_dag(globals())
dag = workflow.get_dag()