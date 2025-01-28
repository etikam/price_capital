-- Création de la base de données principale
CREATE DATABASE prices_capital_db;

-- Création de l'utilisateur principal
CREATE USER prices_capital_user WITH PASSWORD '${POSTGRES_PASSWORD}';

-- Donner tous les privilèges sur la base de données à l'utilisateur
GRANT ALL PRIVILEGES ON DATABASE prices_capital_db TO prices_capital_user;

-- Permettre à l'utilisateur de créer des tables
ALTER USER prices_capital_user CREATEDB;

-- Configuration supplémentaire pour les extensions PostgreSQL
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
