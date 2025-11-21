# Logistics Master Data Management (MDM) Platform

A comprehensive Master Data Management solution for logistics companies, built on open-source technologies. This platform centralizes and governs core business entities including Locations, Clients, Services, and Vehicles using PostgreSQL, OpenMetadata, and Apache Airflow.

## 📋 Project Overview

### 🎯 Core Objectives
- **Centralized Master Data Hub**: Single source of truth for all logistics entities
- **Data Quality Assurance**: Automated validation and normalization of master data
- **Data Governance & Lineage**: Track data ownership, transformations, and dependencies
- **Automated Data Pipelines**: Daily ETL workflows using Apache Airflow
- **Interactive Metadata Catalog**: Browse and understand all data assets via OpenMetadata

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
│        (Faker-generated test data for demo)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Apache Airflow DAGs                             │
│     (Data generation, transformation, loading)               │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│            PostgreSQL MDM Hub                                │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │  Locations   │   Clients    │  Services    │   Vehicles  │
│  │   (MDM)      │    (MDM)     │   (MDM)      │    (MDM)    │
│  └──────────────┴──────────────┴──────────────┘             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│          OpenMetadata Catalog                                │
│   (Data lineage, glossary, classification)                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (v20.10+)
- **8GB RAM** minimum
- **20GB free disk space**
- **Bash shell** (for helper scripts)

### Installation & Startup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd logistics-mdm
```

#### 2. Configure Environment Variables
```bash
# Copy the template to create your .env file
cp .env.template .env

# Edit with your configuration
nano .env
```

See [Configuration](#-configuration--customization) section below for details on each variable.

#### 3. Start All Services
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start the platform
./scripts/start-environment.sh
```

This will start:
- **PostgreSQL** on port 5432 (MDM database)
- **OpenMetadata** on port 8585 (Data catalog UI)
- **Airflow** on port 8080 (Orchestration & DAG execution)
- **Elasticsearch** on port 9200 (Search backend)
- **MySQL** on port 3306 (OpenMetadata metadata store)

#### 3. Access the Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **OpenMetadata UI** | http://localhost:8585 | admin@open-metadata.org / admin |
| **Airflow UI** | http://localhost:8080 | admin / admin |
| **PostgreSQL** | localhost:5432 | mdm_user / mdm_password |

#### 4. Verify Installation
```bash
# Check all services are running
docker-compose ps

# View service logs
docker-compose logs -f openmetadata-server
```

### Stopping Services
```bash
./scripts/stop-environment.sh
```

## 📊 Master Data Domains

The platform manages four core master data domains:

### 1. **Locations** 🏢
Warehouses, depots, hubs, and distribution centers across global markets.

| Field | Type | Description |
|-------|------|-------------|
| Location_ID | String | Unique identifier (e.g., LOC-001) |
| Location_Name | String | Facility name |
| Location_Type | String | Warehouse, Depot, Hub, Office, etc. |
| City, State, Country | String | Geographic location |
| Is_Operational | Boolean | Current operational status |

**Example Records**: 150 locations across 10+ countries

### 2. **Clients** 👥
Shippers, consignees, suppliers, and partner organizations.

| Field | Type | Description |
|-------|------|-------------|
| Client_ID | String | Unique identifier (e.g., CL-001) |
| Client_Name | String | Company name |
| Client_Type | String | Shipper, Consignee, Supplier, Partner |
| Industry_Sector | String | Automotive, Retail, Food, etc. |
| Account_Status | String | Active, Inactive, Suspended |
| Billing_Currency | String | USD, EUR, GBP, MAD, etc. |

**Example Records**: 140 clients linked to locations

### 3. **Services** 🚚
Logistics services offered: transport modes, warehousing, value-added services.

| Field | Type | Description |
|-------|------|-------------|
| Service_ID | String | Unique identifier (e.g., SRV-001) |
| Service_Type | String | Transport, Warehousing, Value-Added |
| Service_Category | String | Long Haul, Distribution, Cold Chain |
| Mode_Of_Transport | String | Road, Air, Sea, Rail |
| Is_Temperature_Controlled | Boolean | Climate control requirement |

**Example Records**: 120 service configurations

### 4. **Vehicles** 🚛
Fleet assets: trucks, vans, trailers with operational details.

| Field | Type | Description |
|-------|------|-------------|
| Vehicle_ID | String | Unique identifier (e.g., VH-001) |
| License_Plate | String | Vehicle registration |
| Vehicle_Type | String | Truck, Van, Trailer |
| Brand & Model | String | Volvo, Mercedes, Scania, MAN |
| Capacity_Weight_Tons | Integer | Cargo capacity |
| Fuel_Type | String | Diesel, Electric, Hybrid |
| Status | String | Active, Maintenance, Retired |

**Example Records**: 160 vehicles with maintenance schedules

## 🔧 Project Structure

```
logistics-mdm/
├── docker-setup/                    # Docker Compose configuration
│   ├── docker-compose.yml          # Main orchestration file
│   ├── dags/                        # Airflow DAG definitions
│   │   ├── mdm_master_data_etl.py  # Main ETL pipeline
│   │   ├── example_dag.py           # Example DAG template
│   │   └── *-generated-*.py         # Auto-generated ingestion DAGs
│   ├── plugins/                     # Airflow plugins & utilities
│   │   ├── mdm_etl.py              # ETL helper functions
│   │   ├── mdm_data_generator.py   # Test data generation
│   │   └── __init__.py
│   ├── requirements.txt             # Python dependencies
│   ├── .gitignore                   # Git exclusions
│   └── docker-volume/               # Persistent volumes (not tracked)
│
├── database/
│   └── init-scripts/
│       ├── 01-mdm-schema.sql       # Database schema definition
│       └── 02-sample-data.sql      # Sample data insertion
│
├── scripts/
│   ├── start-environment.sh         # Start all services
│   └── stop-environment.sh          # Stop all services
│
├── .gitignore                       # Root-level git exclusions
├── LICENSE                          # Apache 2.0 License
├── README.md                        # This file
└── fix-git.sh                       # Utility to fix git tracking
```

## 🔄 ETL Pipeline Overview

### Main DAG: `mdm_master_data_etl`

The primary Airflow DAG orchestrates daily master data processing:

```
1. GENERATE
   ├── generate_locations (150 records)
   ├── generate_clients (140 records)
   ├── generate_services (120 records)
   └── generate_vehicles (160 records)
         ↓
2. TRANSFORM
   ├── Normalize text fields (UPPER, TITLE, LOWER)
   ├── Validate formats (dates, decimals, booleans)
   ├── Clean phone numbers & postal codes
   └── Apply business rules
         ↓
3. LOAD
   ├── Upsert to PostgreSQL tables
   └── Handle duplicates via primary keys
         ↓
4. VERIFY
   └── Count records & validate data integrity
```

### Execution Schedule
- **Daily at 2:00 AM** (configurable via Airflow UI)
- **Incremental loads** with upsert logic
- **Dependency chains**: Locations load first → Clients & Vehicles depend on Locations

### Key Functions (in `plugins/mdm_etl.py`)

| Function | Purpose |
|----------|---------|
| `normalize_upper()` | Convert text to uppercase |
| `normalize_title()` | Convert text to title case |
| `normalize_phone()` | Extract digits from phone numbers |
| `parse_date()` | Parse date strings (YYYY-MM-DD) |
| `parse_decimal()` | Convert to decimal numbers |
| `parse_int()` | Convert to integers |
| `upsert_records()` | Insert/update with conflict handling |

## 🔍 OpenMetadata Integration

OpenMetadata provides a unified data catalog with:

### Features
- **Table Discovery**: Browse all MDM tables and columns
- **Data Lineage**: Visualize ETL transformations
- **Business Glossary**: Define domain terms (e.g., "Active Client")
- **Data Classification**: Tag PII, business-critical fields
- **Asset Ownership**: Assign stewards to domains
- **Search & Browse**: Full-text search across catalog

### Accessing the Catalog
1. Navigate to **http://localhost:8585**
2. Explore **Data Entities** → **PostgreSQL** → **mdm_hub**
3. View table schemas, sample data, and lineage
4. Add descriptions, tags, and ownership information

## 📈 Database Schema

All MDM tables reside in the `mdm` schema with standardized columns:

### Common Columns (All Tables)
```sql
-- Business Key
primary_key  VARCHAR(50) UNIQUE NOT NULL

-- Data Quality
dq_score INTEGER DEFAULT 100
dq_issues JSONB
last_validated TIMESTAMP

-- Audit Trail
created_by VARCHAR(100) DEFAULT 'system'
created_at TIMESTAMP DEFAULT NOW()
updated_by VARCHAR(100)
updated_at TIMESTAMP DEFAULT NOW()

-- Source Tracking
source_system VARCHAR(50)
source_id VARCHAR(100)
source_timestamp TIMESTAMP
```

### Connecting to PostgreSQL

```bash
# From your terminal
psql -h localhost -U mdm_user -d mdm_hub

# Example queries
SELECT COUNT(*) FROM mdm.clients;
SELECT * FROM mdm.locations LIMIT 5;
```

## 🛠️ Configuration & Customization

### Modifying ETL Pipeline

#### Add a New Domain
1. Create generator function in `plugins/mdm_data_generator.py`
2. Define transformer in `plugins/mdm_etl.py`
3. Add table to `database/init-scripts/01-mdm-schema.sql`
4. Update `DOMAINS` dictionary in `dags/mdm_master_data_etl.py`
5. Add DAG tasks for generate → transform → load → verify

#### Change Data Generation Volume
Edit `dags/mdm_master_data_etl.py`:
```python
# Increase or decrease record counts
generate_locations(150)  # Change to desired count
generate_clients(140)    # Change to desired count
```

#### Modify Transformation Rules
Edit transformer functions in `plugins/mdm_etl.py`:
```python
def transform_clients(record):
    record["Client_Name"] = normalize_title(record.get("Client_Name"))
    # Add custom validation or formatting here
    return record
```

### Scheduling

Default schedule is **@daily** (2 AM UTC). To modify:

1. Via Airflow UI:
   - Go to **DAGs** → **mdm_master_data_etl**
   - Edit schedule in DAG details

2. Via Code (`dags/mdm_master_data_etl.py`):
   ```python
   @dag(
       dag_id="mdm_master_data_etl",
       schedule="0 2 * * *",  # 2 AM daily
       # or use: "@weekly", "@monthly", etc.
   )
   ```

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check Docker daemon
docker ps

# View detailed logs
docker-compose logs -f

# Rebuild images if needed
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### PostgreSQL Connection Issues
```bash
# Verify PostgreSQL is running
docker-compose ps postgres-mdm

# Check logs
docker-compose logs postgres-mdm

# Test connection
docker-compose exec postgres-mdm psql -U mdm_user -d mdm_hub -c "SELECT 1"
```

### Airflow DAG Not Running
```bash
# Check DAG parsing
docker-compose exec ingestion airflow dags list

# View DAG logs
docker-compose logs ingestion | grep mdm_master_data_etl

# Trigger manually
docker-compose exec ingestion airflow dags trigger mdm_master_data_etl
```

### OpenMetadata Not Showing Data
```bash
# Wait for database initialization (3-5 minutes on first start)
docker-compose logs openmetadata-server

# Manually trigger PostgreSQL ingestion
# Via UI: Admin → Ingestion → Create Ingestion
```

## 📦 Dependencies

See `docker-setup/requirements.txt`:
- **psycopg2-binary**: PostgreSQL adapter
- **pandas**: Data manipulation
- **faker**: Test data generation

Docker images:
- `openmetadata/server`: Data governance platform
- `openmetadata/ingestion`: Metadata ingestion pipeline
- `postgres`: PostgreSQL database
- `mysql`: OpenMetadata backend
- `elasticsearch`: Full-text search

## 📄 License

Licensed under the **Apache License 2.0** - see [LICENSE](LICENSE) file for details.

## 🆘 Support & Contributing

### Getting Help
- Check logs: `docker-compose logs -f [service-name]`
- Review DAG executions in Airflow UI
- Inspect database directly via psql

### Contributing
1. Create a feature branch: `git checkout -b feature/my-improvement`
2. Make changes and test locally
3. Commit with clear messages: `git commit -m "Add new feature"`
4. Push and create a Pull Request

## 🎯 Next Steps

- [ ] Deploy services: `./scripts/start-environment.sh`
- [ ] Access OpenMetadata at http://localhost:8585
- [ ] Browse generated test data in PostgreSQL
- [ ] Review ETL pipeline in Airflow UI (http://localhost:8080)
- [ ] Customize domains for your logistics use cases
- [ ] Configure production data sources (ERP, CRM, etc.)
- [ ] Set up data steward teams

---

**Version**: 1.0.0 | **Last Updated**: November 2025
