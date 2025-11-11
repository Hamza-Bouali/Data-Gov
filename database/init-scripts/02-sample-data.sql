-- Insert sample clients
INSERT INTO mdm.clients (client_code, raison_sociale, siret, adresse, ville, code_postal, email, telephone, segment_client) VALUES
('CLI001', 'Logistique Express France', '12345678901234', '123 Rue de la Logistique', 'Lyon', '69001', 'contact@logexpress.fr', '+33123456789', 'ENTERPRISE'),
('CLI002', 'Transport Rapid SA', '98765432109876', '456 Avenue des Transports', 'Paris', '75001', 'info@transportrapid.com', '+33123456790', 'SMB');

-- Insert sample fournisseurs
INSERT INTO mdm.fournisseurs (fournisseur_code, raison_sociale, siret, adresse, ville, code_postal, email, telephone, categorie_fournisseur) VALUES
('FOUR001', 'Pneus Pro France', '11112222333344', '789 Boulevard des Pneus', 'Lille', '59000', 'ventes@pneuspro.fr', '+33123456791', 'EQUIPEMENT'),
('FOUR002', 'Carburant Total', '55556666777788', '321 Route du Carburant', 'Marseille', '13001', 'commercial@total-fr.com', '+33123456792', 'CARBURANT');

-- Insert sample produits
INSERT INTO mdm.produits (sku, description, poids, dimensions, prix_achat, prix_vente, categorie_produit, stock_securite) VALUES
('PROD001', 'Palette Europe 800x1200', 25.00, '800x1200x144mm', 15.50, 25.00, 'EMBALLAGE', 100),
('PROD002', 'Caisse carton renforcée', 2.50, '600x400x400mm', 3.20, 6.50, 'EMBALLAGE', 500);

-- Insert sample sites
INSERT INTO mdm.sites (site_code, nom_site, adresse, ville, code_postal, capacite_stockage, type_site) VALUES
('SITE001', 'Entrepôt Central Lyon', '123 Zone Industrielle', 'Lyon', '69007', 5000.00, 'ENTREPOT'),
('SITE002', 'Dépôt Paris Nord', '456 Parc Logistique', 'Paris', '95000', 2500.00, 'DEPOT');

-- Insert sample véhicules
INSERT INTO mdm.vehicules (immatriculation, marque, modele, capacite_charge, type_vehicule, nom_chauffeur, permis_required) VALUES
('AB-123-CD', 'Renault', 'Master', 3500.00, 'UTILITAIRE', 'Pierre Martin', 'B'),
('EF-456-GH', 'Mercedes', 'Actros', 18000.00, 'POIDS_LOURD', 'Jean Dupont', 'C');