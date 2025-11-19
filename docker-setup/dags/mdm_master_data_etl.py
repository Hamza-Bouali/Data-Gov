from __future__ import annotations

from datetime import datetime

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
    upsert_records,
)
from mdm_data_generator import (
    generate_clients,
    generate_locations,
    generate_services,
    generate_vehicles,
)

DB_USER = "postgres.klqgxqzgxnqzwlxjeevb"
DB_PASSWORD = "12345"
DB_HOST = "aws-1-eu-west-1.pooler.supabase.com"
DB_PORT = "6543"
DB_NAME = "postgres"

CONN_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def transform_locations(record: dict[str, object]) -> dict[str, object]:
    record["Location_ID"] = normalize_upper(record.get("Location_ID"))
    record["Location_Name"] = normalize_title(record.get("Location_Name"))
    record["Location_Type"] = normalize_upper(record.get("Location_Type"))
    record["Address_Line_1"] = normalize_title(record.get("Address_Line_1"))
    record["Address_Line_2"] = normalize_title(record.get("Address_Line_2"))
    record["City"] = normalize_title(record.get("City"))
    record["State_Province"] = normalize_title(record.get("State_Province"))
    record["Postal_Code"] = normalize_upper(record.get("Postal_Code"))
    record["Country"] = normalize_upper(record.get("Country"))
    record["Latitude"] = parse_decimal(record.get("Latitude"))
    record["Longitude"] = parse_decimal(record.get("Longitude"))
    record["Is_Operational"] = normalize_bool(record.get("Is_Operational"))
    record["Opening_Date"] = parse_date(record.get("Opening_Date"))
    record["Closing_Date"] = parse_date(record.get("Closing_Date"))
    return record


def transform_clients(record: dict[str, object]) -> dict[str, object]:
    record["Client_ID"] = normalize_upper(record.get("Client_ID"))
    record["Client_Name"] = normalize_title(record.get("Client_Name"))
    record["Client_Type"] = normalize_upper(record.get("Client_Type"))
    record["Legal_Registration_Number"] = normalize_upper(record.get("Legal_Registration_Number"))
    record["Tax_ID"] = normalize_upper(record.get("Tax_ID"))
    record["Industry_Sector"] = normalize_title(record.get("Industry_Sector"))
    record["Primary_Contact_Name"] = normalize_title(record.get("Primary_Contact_Name"))
    record["Primary_Contact_Email"] = normalize_lower(record.get("Primary_Contact_Email"))
    record["Primary_Contact_Phone"] = normalize_phone(record.get("Primary_Contact_Phone"))
    record["Address_ID"] = normalize_upper(record.get("Address_ID"))
    record["Account_Status"] = normalize_upper(record.get("Account_Status"))
    record["Contract_Start_Date"] = parse_date(record.get("Contract_Start_Date"))
    record["Contract_End_Date"] = parse_date(record.get("Contract_End_Date"))
    record["Billing_Currency"] = normalize_upper(record.get("Billing_Currency"))
    return record


def transform_services(record: dict[str, object]) -> dict[str, object]:
    record["Service_ID"] = normalize_upper(record.get("Service_ID"))
    record["Service_Name"] = normalize_title(record.get("Service_Name"))
    record["Service_Type"] = normalize_upper(record.get("Service_Type"))
    record["Service_Category"] = normalize_title(record.get("Service_Category"))
    record["Description"] = record.get("Description")
    record["Mode_Of_Transport"] = normalize_upper(record.get("Mode_Of_Transport"))
    record["Is_Temperature_Controlled"] = normalize_bool(record.get("Is_Temperature_Controlled"))
    record["Requires_Appointment"] = normalize_bool(record.get("Requires_Appointment"))
    record["Active_Status"] = normalize_upper(record.get("Active_Status"))
    return record


def transform_vehicles(record: dict[str, object]) -> dict[str, object]:
    record["Vehicle_ID"] = normalize_upper(record.get("Vehicle_ID"))
    record["License_Plate"] = normalize_upper(record.get("License_Plate"))
    record["Vehicle_Type"] = normalize_upper(record.get("Vehicle_Type"))
    record["Brand"] = normalize_title(record.get("Brand"))
    record["Model"] = normalize_upper(record.get("Model"))
    record["Year"] = parse_int(record.get("Year"))
    record["Capacity_Weight_Tons"] = parse_decimal(record.get("Capacity_Weight_Tons"))
    record["Fuel_Type"] = normalize_upper(record.get("Fuel_Type"))
    record["Status"] = normalize_upper(record.get("Status"))
    record["Trajectory_one_ID"] = normalize_upper(record.get("Trajectory_one_ID"))
    record["Trajectory_two_Location_ID"] = normalize_upper(record.get("Trajectory_two_Location_ID"))
    record["Next_Maintenance_Due"] = parse_date(record.get("Next_Maintenance_Due"))
    return record


DOMAINS = {
    "locations": {
        "config": DomainConfig(
            table="locations_mdm",
            key_columns=["Location_ID"],
            column_order=[
                "Location_ID",
                "Location_Name",
                "Location_Type",
                "Address_Line_1",
                "Address_Line_2",
                "City",
                "State_Province",
                "Postal_Code",
                "Country",
                "Latitude",
                "Longitude",
                "Is_Operational",
                "Opening_Date",
                "Closing_Date",
            ],
            transformer=transform_locations,
        ),
        "generator": lambda: generate_locations(150),
    },
    "clients": {
        "config": DomainConfig(
            table="clients_mdm",
            key_columns=["Client_ID"],
            column_order=[
                "Client_ID",
                "Client_Name",
                "Client_Type",
                "Legal_Registration_Number",
                "Tax_ID",
                "Industry_Sector",
                "Primary_Contact_Name",
                "Primary_Contact_Email",
                "Primary_Contact_Phone",
                "Address_ID",
                "Account_Status",
                "Contract_Start_Date",
                "Contract_End_Date",
                "Billing_Currency",
            ],
            transformer=transform_clients,
        ),
        "generator": lambda max_loc: generate_clients(140, max_loc),
    },
    "services": {
        "config": DomainConfig(
            table="services_mdm",
            key_columns=["Service_ID"],
            column_order=[
                "Service_ID",
                "Service_Name",
                "Service_Type",
                "Service_Category",
                "Description",
                "Mode_Of_Transport",
                "Is_Temperature_Controlled",
                "Requires_Appointment",
                "Active_Status",
            ],
            transformer=transform_services,
        ),
        "generator": lambda: generate_services(120),
    },
    "vehicles": {
        "config": DomainConfig(
            table="vehicles_mdm",
            key_columns=["Vehicle_ID"],
            column_order=[
                "Vehicle_ID",
                "License_Plate",
                "Vehicle_Type",
                "Brand",
                "Model",
                "Year",
                "Capacity_Weight_Tons",
                "Fuel_Type",
                "Status",
                "Trajectory_one_ID",
                "Trajectory_two_Location_ID",
                "Next_Maintenance_Due",
            ],
            transformer=transform_vehicles,
        ),
        "generator": lambda max_loc: generate_vehicles(160, max_loc),
    },
}


@task
def generate_data(domain_key: str, max_location_id: int | None = None) -> list[dict[str, object]]:
    generator = DOMAINS[domain_key]["generator"]
    if max_location_id is not None:
        return generator(max_location_id)
    return generator()


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

    locations_generate = generate_data.override(task_id="generate_locations")("locations")
    locations_transform = transform_domain.override(task_id="transform_locations")(locations_generate, domain_key="locations")
    locations_load = load_domain.override(task_id="load_locations")(locations_transform, domain_key="locations")
    locations_verify = verify_destination.override(task_id="verify_locations")(locations_load, domain_key="locations")
    
    pipelines["locations"] = {"load": locations_load}
    locations_verify >> destination

    clients_generate = generate_data.override(task_id="generate_clients")("clients", max_location_id=150)
    clients_transform = transform_domain.override(task_id="transform_clients")(clients_generate, domain_key="clients")
    clients_load = load_domain.override(task_id="load_clients")(clients_transform, domain_key="clients")
    clients_verify = verify_destination.override(task_id="verify_clients")(clients_load, domain_key="clients")
    
    pipelines["clients"] = {"load": clients_load}
    clients_verify >> destination

    services_generate = generate_data.override(task_id="generate_services")("services")
    services_transform = transform_domain.override(task_id="transform_services")(services_generate, domain_key="services")
    services_load = load_domain.override(task_id="load_services")(services_transform, domain_key="services")
    services_verify = verify_destination.override(task_id="verify_services")(services_load, domain_key="services")
    
    pipelines["services"] = {"load": services_load}
    services_verify >> destination

    vehicles_generate = generate_data.override(task_id="generate_vehicles")("vehicles", max_location_id=150)
    vehicles_transform = transform_domain.override(task_id="transform_vehicles")(vehicles_generate, domain_key="vehicles")
    vehicles_load = load_domain.override(task_id="load_vehicles")(vehicles_transform, domain_key="vehicles")
    vehicles_verify = verify_destination.override(task_id="verify_vehicles")(vehicles_load, domain_key="vehicles")
    
    pipelines["vehicles"] = {"load": vehicles_load}
    vehicles_verify >> destination

    locations_load >> clients_generate
    locations_load >> vehicles_generate


dag = mdm_master_data_etl()
