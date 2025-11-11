-- Create MDM Schema
CREATE SCHEMA IF NOT EXISTS mdm;

-- Clients Master Table
CREATE TABLE mdm.clients (
    golden_id SERIAL PRIMARY KEY,
    client_code VARCHAR(50) UNIQUE NOT NULL,
    raison_sociale VARCHAR(255) NOT NULL,
    siret VARCHAR(14),
    adresse TEXT,
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    pays VARCHAR(100) DEFAULT 'France',
    contact_principal VARCHAR(100),
    email VARCHAR(150),
    telephone VARCHAR(20),
    segment_client VARCHAR(50),
    statut VARCHAR(20) DEFAULT 'actif',
    
    -- Data Quality Metrics
    dq_score INTEGER DEFAULT 100,
    dq_issues JSONB,
    last_validated TIMESTAMP,
    
    -- Audit Fields
    created_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Source System Tracking
    source_system VARCHAR(50),
    source_id VARCHAR(100),
    source_timestamp TIMESTAMP
);

-- Fournisseurs Master Table
CREATE TABLE mdm.fournisseurs (
    golden_id SERIAL PRIMARY KEY,
    fournisseur_code VARCHAR(50) UNIQUE NOT NULL,
    raison_sociale VARCHAR(255) NOT NULL,
    siret VARCHAR(14),
    adresse TEXT,
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    pays VARCHAR(100) DEFAULT 'France',
    contact_principal VARCHAR(100),
    email VARCHAR(150),
    telephone VARCHAR(20),
    categorie_fournisseur VARCHAR(50),
    conditions_paiement VARCHAR(50),
    statut VARCHAR(20) DEFAULT 'actif',
    
    dq_score INTEGER DEFAULT 100,
    dq_issues JSONB,
    last_validated TIMESTAMP,
    
    created_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    source_system VARCHAR(50),
    source_id VARCHAR(100),
    source_timestamp TIMESTAMP
);

-- Produits Master Table
CREATE TABLE mdm.produits (
    golden_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    poids DECIMAL(10,2),
    dimensions VARCHAR(100),
    prix_achat DECIMAL(15,2),
    prix_vente DECIMAL(15,2),
    categorie_produit VARCHAR(100),
    stock_securite INTEGER DEFAULT 0,
    statut VARCHAR(20) DEFAULT 'actif',
    
    dq_score INTEGER DEFAULT 100,
    dq_issues JSONB,
    last_validated TIMESTAMP,
    
    created_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    source_system VARCHAR(50),
    source_id VARCHAR(100),
    source_timestamp TIMESTAMP
);

-- Sites Master Table
CREATE TABLE mdm.sites (
    golden_id SERIAL PRIMARY KEY,
    site_code VARCHAR(50) UNIQUE NOT NULL,
    nom_site VARCHAR(255),
    adresse TEXT,
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    pays VARCHAR(100) DEFAULT 'France',
    capacite_stockage DECIMAL(15,2),
    type_site VARCHAR(50),
    statut VARCHAR(20) DEFAULT 'actif',
    
    dq_score INTEGER DEFAULT 100,
    dq_issues JSONB,
    last_validated TIMESTAMP,
    
    created_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    source_system VARCHAR(50),
    source_id VARCHAR(100),
    source_timestamp TIMESTAMP
);

-- Véhicules Master Table
CREATE TABLE mdm.vehicules (
    golden_id SERIAL PRIMARY KEY,
    immatriculation VARCHAR(20) UNIQUE NOT NULL,
    marque VARCHAR(100),
    modele VARCHAR(100),
    capacite_charge DECIMAL(15,2),
    type_vehicule VARCHAR(50),
    nom_chauffeur VARCHAR(100),
    permis_required VARCHAR(50),
    statut VARCHAR(20) DEFAULT 'actif',
    
    dq_score INTEGER DEFAULT 100,
    dq_issues JSONB,
    last_validated TIMESTAMP,
    
    created_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    source_system VARCHAR(50),
    source_id VARCHAR(100),
    source_timestamp TIMESTAMP
);

-- Data Quality Results Table
CREATE TABLE mdm.dq_results (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    check_description TEXT,
    passed_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    error_message TEXT,
    execution_time INTERVAL,
    executed_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_clients_code ON mdm.clients(client_code);
CREATE INDEX idx_clients_siret ON mdm.clients(siret);
CREATE INDEX idx_fournisseurs_code ON mdm.fournisseurs(fournisseur_code);
CREATE INDEX idx_produits_sku ON mdm.produits(sku);
CREATE INDEX idx_sites_code ON mdm.sites(site_code);
CREATE INDEX idx_vehicules_immat ON mdm.vehicules(immatriculation);
CREATE INDEX idx_dq_results_table ON mdm.dq_results(table_name);
CREATE INDEX idx_dq_results_executed ON mdm.dq_results(executed_at);