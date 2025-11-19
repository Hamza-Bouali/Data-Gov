from __future__ import annotations

from datetime import datetime
from pathlib import Path

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator

from mdm_etl import (
    DomainConfig,
    count_rows,
    normalize_bool,
    normalize_lower,
    normalize_phone,
    normalize_title,
    normalize_upper,
    parse_date,
    parse_decimal,
    parse_int,
    read_csv_records,
    upsert_records,
)

DATA_DIR = Path("/opt/data/raw")
CONN_URI = "postgresql://airflow:airflow@postgres:5432/mdm"

def transform_locations(record: dict[str, object]) -> dict[str, object]:
    record["location_id"] = normalize_upper(record.get("location_id"))
    record["location_name"] = normalize_title(record.get("location_name"))
    record["location_type"] = normalize_upper(record.get("location_type"))
    record["address_line_1"] = normalize_title(record.get("address_line_1"))
    record["address_line_2"] = normalize_title(record.get("address_line_2"))
    record["city"] = normalize_title(record.get("city"))
    record["state_province"] = normalize_title(record.get("state_province"))
    record["postal_code"] = normalize_upper(record.get("postal_code"))
    record["country"] = normalize_upper(record.get("country"))
    record["latitude"] = parse_decimal(record.get("latitude"))
    record["longitude"] = parse_decimal(record.get("longitude"))
    record["is_operational"] = normalize_bool(record.get("is_operational"))
    record["opening_date"] = parse_date(record.get("opening_date"))
    record["closing_date"] = parse_date(record.get("closing_date"))
    return record


def transform_clients(record: dict[str, object]) -> dict[str, object]:
    record["client_id"] = normalize_upper(record.get("client_id"))
    record["client_name"] = normalize_title(record.get("client_name"))
    record["client_type"] = normalize_upper(record.get("client_type"))
    record["legal_registration_number"] = normalize_upper(record.get("legal_registration_number"))
    record["tax_id"] = normalize_upper(record.get("tax_id"))
    record["industry_sector"] = normalize_title(record.get("industry_sector"))
    record["primary_contact_name"] = normalize_title(record.get("primary_contact_name"))
    record["primary_contact_email"] = normalize_lower(record.get("primary_contact_email"))
    record["primary_contact_phone"] = normalize_phone(record.get("primary_contact_phone"))
    record["address_id"] = normalize_upper(record.get("address_id"))
    record["account_status"] = normalize_upper(record.get("account_status"))
    record["contract_start_date"] = parse_date(record.get("contract_start_date"))
    record["contract_end_date"] = parse_date(record.get("contract_end_date"))
    return record


def transform_services(record: dict[str, object]) -> dict[str, object]:
    record["service_id"] = normalize_upper(record.get("service_id"))
    record["service_name"] = normalize_title(record.get("service_name"))
    record["service_type"] = normalize_upper(record.get("service_type"))
    record["service_category"] = normalize_title(record.get("service_category"))
    record["mode_of_transport"] = normalize_upper(record.get("mode_of_transport"))
    record["is_temperature_controlled"] = normalize_bool(record.get("is_temperature_controlled"))
    record["requires_appointment"] = normalize_bool(record.get("requires_appointment"))
    record["active_status"] = normalize_upper(record.get("active_status"))
    return record


def transform_vehicles(record: dict[str, object]) -> dict[str, object]:
    record["vehicle_id"] = normalize_upper(record.get("vehicle_id"))
    record["license_plate"] = normalize_upper(record.get("license_plate"))
    record["vehicle_type"] = normalize_upper(record.get("vehicle_type"))
    record["brand"] = normalize_title(record.get("brand"))
    record["model"] = normalize_upper(record.get("model"))
    record["year"] = parse_int(record.get("year"))
    record["capacity_weight_tons"] = parse_decimal(record.get("capacity_weight_tons"))
    record["fuel_type"] = normalize_upper(record.get("fuel_type"))
    record["status"] = normalize_upper(record.get("status"))
    record["trajectory_one_id"] = normalize_upper(record.get("trajectory_one_id"))
    record["trajectory_two_location_id"] = normalize_upper(record.get("trajectory_two_location_id"))
    record["next_maintenance_due"] = parse_date(record.get("next_maintenance_due"))
    return record


DOMAINS = {
    "locations": {
        "csv": DATA_DIR / "locations.csv",
        "config": DomainConfig(
            table="mdm_locations",
            key_columns=["location_id"],
            column_order=[
                "location_id",
                "location_name",
                "location_type",
                "address_line_1",
                "address_line_2",
                "city",
                "state_province",
                "postal_code",
                "country",
                "latitude",
                "longitude",
                "is_operational",
                "opening_date",
                "closing_date",
            ],
            transformer=transform_locations,
        ),
    },
    "clients": {
        "csv": DATA_DIR / "clients.csv",
        "config": DomainConfig(
            table="mdm_clients",
            key_columns=["client_id"],
            column_order=[
                "client_id",
                "client_name",
                "client_type",
                "legal_registration_number",
                "tax_id",
                "industry_sector",
                "primary_contact_name",
                "primary_contact_email",
                "primary_contact_phone",
                "address_id",
                "account_status",
                "contract_start_date",
                "contract_end_date",
            ],
            transformer=transform_clients,
        ),
    },
    "services": {
        "csv": DATA_DIR / "services.csv",
        "config": DomainConfig(
            table="mdm_services",
            key_columns=["service_id"],
            column_order=[
                "service_id",
                "service_name",
                "service_type",
                "service_category",
                "description",
                "mode_of_transport",
                "is_temperature_controlled",
                "requires_appointment",
                "active_status",
            ],
            transformer=transform_services,
        ),
    },
    "vehicles": {
        "csv": DATA_DIR / "vehicles.csv",
        "config": DomainConfig(
            table="mdm_vehicles",
            key_columns=["vehicle_id"],
            column_order=[
                "vehicle_id",
                "license_plate",
                "vehicle_type",
                "brand",
                "model",
                "year",
                "capacity_weight_tons",
                "fuel_type",
                "status",
                "trajectory_one_id",
                "trajectory_two_location_id",
                "next_maintenance_due",
            ],
            transformer=transform_vehicles,
        ),
    },
}


@task
def extract_csv(csv_path: str) -> list[dict[str, object]]:
    return read_csv_records(csv_path)


@task
def transform_domain(records: list[dict[str, object]], domain_key: str) -> list[dict[str, object]]:
    transformer = DOMAINS[domain_key]["config"].transformer
    if transformer:
        return [transformer(record.copy()) for record in records]
    return records


@task
def load_domain(records: list[dict[str, object]], domain_key: str) -> int:
    config: DomainConfig = DOMAINS[domain_key]["config"]
    upsert_records(CONN_URI, config, records)
    return len(records)


@task
def verify_destination(_rows_loaded: int, domain_key: str) -> int:
    table = DOMAINS[domain_key]["config"].table
    return count_rows(CONN_URI, table)


default_args = {
    "owner": "data-gov",
    "retries": 1,
}


@dag(
    dag_id="mdm_master_data_etl",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["mdm", "data-gov"],
)
def mdm_master_data_etl():
    destination = EmptyOperator(task_id="postgres_destination")
    pipelines = {}

    for domain_key, meta in DOMAINS.items():
        extract = extract_csv.override(task_id=f"extract_{domain_key}")(str(meta["csv"]))
        transform = transform_domain.override(task_id=f"transform_{domain_key}")(extract, domain_key=domain_key)
        load = load_domain.override(task_id=f"load_{domain_key}")(transform, domain_key=domain_key)
        verify = verify_destination.override(task_id=f"verify_{domain_key}")(load, domain_key=domain_key)
        verify >> destination
        pipelines[domain_key] = {
            "extract": extract,
            "load": load,
        }

    pipelines["locations"]["load"] >> pipelines["clients"]["extract"]
    pipelines["locations"]["load"] >> pipelines["services"]["extract"]
    pipelines["locations"]["load"] >> pipelines["vehicles"]["extract"]


dag = mdm_master_data_etl()