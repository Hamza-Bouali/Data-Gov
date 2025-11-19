# dags

This folder is intended to hold Airflow DAGs for local development when running the ingestion container.

Notes:
- Files placed here are helpful for testing Airflow DAGs locally and for keeping DAG source under version control.
- The provided `docker-compose.yml` in `docker-setup/` mounts a named Docker volume for DAGs. If you prefer using this local folder as a bind mount, update the `ingestion` service volumes to bind `./docker-setup/dags:/opt/airflow/dags`.

Example bind-mount in `docker-compose.yml` (replace the existing `ingestion` volume mapping):

```
    volumes:
      - ./docker-setup/dags:/opt/airflow/dags
```

Create DAG files with `.py` extension. The repository includes `example_dag.py` as a minimal example.
