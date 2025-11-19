from __future__ import annotations

import random
from datetime import date, datetime

from faker import Faker

fake = Faker()

LOCATION_TYPES = ["Warehouse", "Depot", "Hub", "Office", "Client Address"]

WORLD_CITIES = {
    "Morocco": ["Casablanca", "Rabat", "Tangier", "Agadir"],
    "USA": ["New York", "Chicago", "Los Angeles", "Dallas"],
    "Canada": ["Toronto", "Vancouver", "Montreal"],
    "Germany": ["Berlin", "Hamburg", "Frankfurt"],
    "France": ["Paris", "Lyon", "Marseille"],
    "Spain": ["Madrid", "Barcelona", "Valencia"],
    "UK": ["London", "Manchester", "Birmingham"],
    "UAE": ["Dubai", "Abu Dhabi"],
    "India": ["Mumbai", "Delhi", "Bangalore"],
    "China": ["Shanghai", "Beijing", "Shenzhen"],
    "Japan": ["Tokyo", "Osaka", "Nagoya"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília"],
}

CURRENCIES = ["USD", "EUR", "GBP", "MAD", "CAD", "JPY", "AED", "INR", "BRL", "CNY"]

SERVICE_TYPES = ["Transport", "Warehousing", "Value-Added", "Customs"]
SERVICE_CATEGORIES = ["Long Haul", "Distribution", "Cold Chain", "Cross-Docking"]
TRANSPORT_MODES = ["Road", "Air", "Sea", "Rail", None]

CLIENT_TYPES = ["Shipper", "Consignee", "Supplier", "Partner"]
INDUSTRIES = ["Automotive", "Retail", "Food", "Chemicals", "Textile"]
ACCOUNT_STATUSES = ["Active", "Inactive", "Suspended"]

VEHICLE_TYPES = ["Truck", "Van", "Trailer"]
BRANDS_MODELS = {
    "Volvo": ["FH16", "FMX", "VNR"],
    "Mercedes": ["Actros", "Arocs", "Econic"],
    "Scania": ["R500", "S730", "P360"],
    "MAN": ["TGX", "TGS", "TGM"],
}
FUEL_TYPES = ["Diesel", "Electric", "Hybrid"]
STATUS_TYPES = ["Active", "Maintenance", "Retired"]


def generate_location(i: int) -> dict[str, object]:
    country = random.choice(list(WORLD_CITIES.keys()))
    city = random.choice(WORLD_CITIES[country])
    return {
        "Location_ID": f"LOC-{i:03d}",
        "Location_Name": f"{city} Site {i}",
        "Location_Type": random.choice(LOCATION_TYPES),
        "Address_Line_1": fake.street_address(),
        "Address_Line_2": fake.secondary_address(),
        "City": city,
        "State_Province": f"{city} Region",
        "Postal_Code": fake.postcode(),
        "Country": country,
        "Latitude": fake.latitude(),
        "Longitude": fake.longitude(),
        "Is_Operational": random.choice([True, False]),
        "Opening_Date": fake.date_between(start_date="-10y", end_date="today"),
        "Closing_Date": random.choice([None, fake.date_between(start_date="-1y", end_date="today")]),
    }


def generate_service(i: int) -> dict[str, object]:
    return {
        "Service_ID": f"SRV-{i:03d}",
        "Service_Name": f"Service {i}",
        "Service_Type": random.choice(SERVICE_TYPES),
        "Service_Category": random.choice(SERVICE_CATEGORIES),
        "Description": fake.text(60),
        "Mode_Of_Transport": random.choice(TRANSPORT_MODES),
        "Is_Temperature_Controlled": random.choice([True, False]),
        "Requires_Appointment": random.choice([True, False]),
        "Active_Status": random.choice(["Active", "Inactive"]),
    }


def generate_client(i: int, max_location_id: int = 150) -> dict[str, object]:
    return {
        "Client_ID": f"CL-{i:03d}",
        "Client_Name": fake.company(),
        "Client_Type": random.choice(CLIENT_TYPES),
        "Legal_Registration_Number": f"RC-{random.randint(100000, 999999)}",
        "Tax_ID": f"ICE-{random.randint(10000000, 99999999)}",
        "Industry_Sector": random.choice(INDUSTRIES),
        "Primary_Contact_Name": fake.name(),
        "Primary_Contact_Email": fake.email(),
        "Primary_Contact_Phone": fake.phone_number(),
        "Address_ID": f"LOC-{random.randint(1, max_location_id):03d}",
        "Account_Status": random.choice(ACCOUNT_STATUSES),
        "Contract_Start_Date": fake.date_between(start_date="-5y", end_date="today"),
        "Contract_End_Date": random.choice([None, fake.date_between(start_date="today", end_date="+3y")]),
        "Billing_Currency": random.choice(CURRENCIES),
    }


def generate_vehicle(i: int, max_location_id: int = 150) -> dict[str, object]:
    brand = random.choice(list(BRANDS_MODELS.keys()))
    return {
        "Vehicle_ID": f"VH-{i:03d}",
        "License_Plate": fake.license_plate(),
        "Vehicle_Type": random.choice(VEHICLE_TYPES),
        "Brand": brand,
        "Model": random.choice(BRANDS_MODELS[brand]),
        "Year": random.randint(2010, 2024),
        "Capacity_Weight_Tons": random.randint(5, 40),
        "Fuel_Type": random.choice(FUEL_TYPES),
        "Status": random.choice(STATUS_TYPES),
        "Trajectory_one_ID": f"LOC-{random.randint(1, max_location_id):03d}",
        "Trajectory_two_Location_ID": f"LOC-{random.randint(1, max_location_id):03d}",
        "Next_Maintenance_Due": fake.date_between(start_date="+30d", end_date="+365d"),
    }


def generate_locations(num: int = 150) -> list[dict[str, object]]:
    return [generate_location(i) for i in range(1, num + 1)]


def generate_services(num: int = 120) -> list[dict[str, object]]:
    return [generate_service(i) for i in range(1, num + 1)]


def generate_clients(num: int = 140, max_location_id: int = 150) -> list[dict[str, object]]:
    return [generate_client(i, max_location_id) for i in range(1, num + 1)]


def generate_vehicles(num: int = 160, max_location_id: int = 150) -> list[dict[str, object]]:
    return [generate_vehicle(i, max_location_id) for i in range(1, num + 1)]

