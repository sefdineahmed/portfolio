# PostgreSQL : Création et alimentation d'une table depuis un fichier CSV

## Objectif

Ce document présente étape par étape comment :

1. Se connecter à PostgreSQL ;
2. Créer un utilisateur ;
3. Créer une base de données ;
4. Créer un schéma ;
5. Créer une table ;
6. Importer des données depuis un fichier CSV ;
7. Vérifier les données importées ;
8. Préparer la base pour Apache Superset.

L'exemple utilise le projet **Hotel Booking Analytics**.


# 1. Prérequis

Les outils utilisés sont :

* PostgreSQL
* `psql`
* Python / Pandas pour préparer le fichier CSV
* Apache Superset pour la visualisation

Vérifier l'installation de PostgreSQL :

```bash
psql --version
```

Exemple :

```text
psql (PostgreSQL 16.x)
```


# 2. Démarrer PostgreSQL

Sur Ubuntu / Xubuntu :

```bash
sudo systemctl status postgresql
```

Si PostgreSQL n'est pas démarré :

```bash
sudo systemctl start postgresql
```

Pour démarrer automatiquement PostgreSQL au démarrage :

```bash
sudo systemctl enable postgresql
```


# 3. Se connecter en administrateur

Par défaut, PostgreSQL possède un utilisateur administrateur appelé `postgres`.

```bash
sudo -u postgres psql
```

Vous devriez obtenir :

```text
psql (16.x)
Type "help" for help.

postgres=#
```


# 4. Créer l'utilisateur PostgreSQL

Dans `psql` :

```sql
CREATE USER sefdine WITH PASSWORD 'sefdine';
```

Vérifier les utilisateurs :

```sql
\du
```

Vous devriez retrouver :

```text
sefdine
```

> Pour un environnement professionnel, utiliser un mot de passe fort et ne pas stocker les identifiants directement dans les fichiers du projet.


# 5. Créer la base de données

Créer la base `hotel_booking` :

```sql
CREATE DATABASE hotel_booking
    OWNER sefdine;
```

Vérifier les bases disponibles :

```sql
\l
```

La base devrait apparaître :

```text
hotel_booking
```


# 6. Se connecter à la nouvelle base

Quitter `psql` :

```sql
\q
```

Puis :

```bash
psql -U sefdine -d hotel_booking -h localhost
```

Entrer le mot de passe :

```text
sefdine
```


# 7. Créer le schéma

Un schéma permet d'organiser les tables dans une base PostgreSQL.

Nous allons créer :

```text
HotelBookings
```

Commande :

```sql
CREATE SCHEMA "HotelBookings";
```

Donner les droits au propriétaire :

```sql
GRANT ALL ON SCHEMA "HotelBookings" TO sefdine;
```

Vérifier :

```sql
\dn
```

Résultat attendu :

```text
      Name
----------------
 HotelBookings
 public
```


# 8. Préparer le fichier CSV

Dans notre projet, Python/Pandas prépare le fichier :

```text
hotel_bookings_superset.csv
```

Chemin :

```text
outputs/cleaned/hotel_bookings_superset.csv
```

Exemple :

```text
hotel,arrival_date,arrival_year,arrival_month_num,arrival_date_month,lead_time,lead_time_category,total_guests,total_nights,is_cancelled,adr,estimated_revenue,...
City Hotel,2015-07-01,2015,7,July,342,>90 days,2,5,false,50.0,250.0,...
```

Avant l'importation, il est recommandé de vérifier le fichier :

```bash
head -5 /home/sefdine/github/sefdine-portfolio/hotel-booking/outputs/cleaned/hotel_bookings_superset.csv
```

Vérifier également le nombre de lignes :

```bash
wc -l /home/sefdine/github/sefdine-portfolio/hotel-booking/outputs/cleaned/hotel_bookings_superset.csv
```


# 9. Créer la table PostgreSQL

Nous allons créer la table :

```text
HotelBookings.hotelbookings
```

Commande :

```sql
CREATE TABLE "HotelBookings"."hotelbookings" (

    hotel                   VARCHAR(50),

    arrival_date            DATE,

    arrival_year            INTEGER,

    arrival_month_num       INTEGER,

    arrival_date_month      VARCHAR(20),

    lead_time               INTEGER,

    lead_time_category      VARCHAR(20),

    total_guests            NUMERIC(10,2),

    total_nights            INTEGER,

    is_cancelled            BOOLEAN,

    adr                     NUMERIC(12,2),

    estimated_revenue       NUMERIC(14,2),

    market_segment          VARCHAR(50),

    distribution_channel    VARCHAR(50),

    customer_type           VARCHAR(50),

    meal                    VARCHAR(30),

    country                 VARCHAR(10),

    deposit_type             VARCHAR(50),

    reservation_status       VARCHAR(50)
);
```


# 10. Vérifier la structure de la table

Utiliser :

```sql
\d "HotelBookings"."hotelbookings"
```

PostgreSQL affiche les colonnes, les types et les contraintes de la table.


# 11. Importer le CSV avec `\copy`

## Méthode recommandée

La commande `\copy` est exécutée depuis le client `psql`.

```sql
\copy "HotelBookings"."hotelbookings"
FROM '/home/sefdine/github/sefdine-portfolio/hotel-booking/outputs/cleaned/hotel_bookings_superset.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);
```

Si l'importation fonctionne, PostgreSQL affiche quelque chose comme :

```text
COPY 119390
```

Le nombre exact dépend du fichier utilisé.


# 12. Pourquoi utiliser `\copy` plutôt que `COPY` ?

Il existe une différence importante.

### `COPY`

```sql
COPY table
FROM '/chemin/fichier.csv';
```

Le fichier doit être accessible par le **serveur PostgreSQL**.

### `\copy`

```sql
\copy table
FROM '/chemin/fichier.csv';
```

Le fichier est lu par le **client `psql`**.

Pour un fichier présent dans votre dossier personnel :

```text
/home/sefdine/...
```

`\copy` est généralement beaucoup plus simple.

---

# 13. Vérifier le nombre de lignes

Après l'importation :

```sql
SELECT COUNT(*)
FROM "HotelBookings"."hotelbookings";
```

Exemple :

```text
 count
--------
 119390
```

---

# 14. Afficher les premières lignes

```sql
SELECT *
FROM "HotelBookings"."hotelbookings"
LIMIT 10;
```

---

# 15. Vérifier les hôtels

```sql
SELECT
    hotel,
    COUNT(*) AS bookings
FROM "HotelBookings"."hotelbookings"
GROUP BY hotel
ORDER BY bookings DESC;
```

Exemple de résultat :

```text
hotel           | bookings
----------------+---------
City Hotel      | ...
Resort Hotel    | ...
```

---

# 16. Vérifier les annulations

```sql
SELECT
    is_cancelled,
    COUNT(*) AS bookings
FROM "HotelBookings"."hotelbookings"
GROUP BY is_cancelled;
```

---

# 17. Calculer le taux d'annulation

```sql
SELECT
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN is_cancelled = TRUE THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate
FROM "HotelBookings"."hotelbookings";
```

---

# 18. Taux d'annulation par hôtel

```sql
SELECT
    hotel,

    COUNT(*) AS total_bookings,

    SUM(
        CASE
            WHEN is_cancelled = TRUE THEN 1
            ELSE 0
        END
    ) AS cancellations,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN is_cancelled = TRUE THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate

FROM "HotelBookings"."hotelbookings"

GROUP BY hotel

ORDER BY cancellation_rate DESC;
```

---

# 19. Vérifier les valeurs manquantes

Pour une colonne :

```sql
SELECT
    COUNT(*) AS total_rows,

    COUNT(country) AS non_null_country,

    COUNT(*) - COUNT(country) AS missing_country

FROM "HotelBookings"."hotelbookings";
```

---

# 20. Vérifier les valeurs aberrantes

### Lead Time négatif

```sql
SELECT COUNT(*)
FROM "HotelBookings"."hotelbookings"
WHERE lead_time < 0;
```

### ADR négatif

```sql
SELECT COUNT(*)
FROM "HotelBookings"."hotelbookings"
WHERE adr < 0;
```

### Nombre de nuits négatif

```sql
SELECT COUNT(*)
FROM "HotelBookings"."hotelbookings"
WHERE total_nights < 0;
```

---

# 21. Exemple : importer un fichier Excel

PostgreSQL ne lit pas directement un fichier `.xlsx` avec `\copy`.

Il faut d'abord convertir Excel en CSV.

Avec Python :

```python
import pandas as pd

df = pd.read_excel(
    "hotel_bookings.xlsx"
)

df.to_csv(
    "hotel_bookings.csv",
    index=False
)
```

Puis importer le CSV :

```sql
\copy "HotelBookings"."hotelbookings"
FROM '/chemin/hotel_bookings.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);
```

---

# 22. Exemple : créer une table depuis Python

Il est également possible d'utiliser Pandas et SQLAlchemy.

Installation :

```bash
pip install sqlalchemy psycopg2-binary
```

Connexion :

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://sefdine:sefdine@localhost:5432/hotel_booking"
)
```

Puis :

```python
df.to_sql(
    "hotelbookings",
    engine,
    schema="HotelBookings",
    if_exists="append",
    index=False
)
```

### Options importantes

```text
if_exists="fail"
```

→ erreur si la table existe.

```text
if_exists="replace"
```

→ supprime et recrée la table.

```text
if_exists="append"
```

→ ajoute les nouvelles données.

Pour notre projet, `append` est intéressant si la table est déjà créée et que les types ont été contrôlés.


# 23. Connecter PostgreSQL à Apache Superset

Une fois les données dans PostgreSQL, Superset peut se connecter directement à la base.

Informations de connexion :

```text
Database:
hotel_booking

Host:
localhost

Port:
5432

Username:
sefdine

Password:
********
```

URI SQLAlchemy :

```text
postgresql+psycopg2://sefdine:sefdine@localhost:5432/hotel_booking
```

Dans Superset :

```text
Settings
   ↓
Database Connections
   ↓
+ Database
   ↓
PostgreSQL
```

Puis ajouter la connexion.


# 24. Ajouter la table dans Superset

Après la connexion :

```text
Datasets
   ↓
+ Dataset
   ↓
Database: hotel_booking
   ↓
Schema: HotelBookings
   ↓
Table: hotelbookings
```

La table devient alors disponible pour créer :

* KPI ;
* Bar Charts ;
* Line Charts ;
* Pie / Donut Charts ;
* Heatmaps ;
* Tables ;
* filtres interactifs ;
* dashboards.

# 25. Architecture du projet

L'architecture finale est :

```text
                 ┌─────────────────────┐
                 │       Kaggle        │
                 │    Dataset CSV      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Python        │
                 │      Pandas         │
                 │                     │
                 │ Data Cleaning       │
                 │ Feature Engineering │
                 │ Data Quality        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      CSV propre     │
                 └──────────┬──────────┘
                            │
                         \copy
                            │
                            ▼
              ┌──────────────────────────┐
              │       PostgreSQL         │
              │                          │
              │ Database: hotel_booking  │
              │                          │
              │ Schema: HotelBookings    │
              │                          │
              │ Table: hotelbookings     │
              └────────────┬─────────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │   Apache Superset   │
                 │                     │
                 │ Metrics             │
                 │ Charts              │
                 │ Filters             │
                 │ Dashboards          │
                 └─────────────────────┘
```

# 26. Commandes essentielles — résumé

Si la base, l'utilisateur et le schéma existent déjà, le processus d'importation peut être résumé ainsi :

### Connexion

```bash
psql -U sefdine -d hotel_booking -h localhost
```

### Vérifier la table

```sql
\d "HotelBookings"."hotelbookings"
```

### Importer

```sql
\copy "HotelBookings"."hotelbookings"
FROM '/home/sefdine/github/sefdine-portfolio/hotel-booking/outputs/cleaned/hotel_bookings_superset.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);
```

### Vérifier

```sql
SELECT COUNT(*)
FROM "HotelBookings"."hotelbookings";
```

### Aperçu

```sql
SELECT *
FROM "HotelBookings"."hotelbookings"
LIMIT 10;
```

# 27. Bonnes pratiques

### Sécurité

Ne jamais publier dans GitHub :

```text
password = ?
```

Utiliser plutôt :

```text
.env
```

et ajouter `.env` dans `.gitignore`.

---

### Qualité des données

Toujours vérifier :

* les valeurs manquantes ;
* les doublons ;
* les types ;
* les valeurs négatives ;
* les valeurs aberrantes ;
* les dates ;
* les catégories ;
* les contraintes métier.

---

### Base de données

Utiliser des types adaptés :

```text
INTEGER       → nombres entiers
NUMERIC       → montants
DATE          → dates
BOOLEAN       → vrai/faux
VARCHAR       → texte
```

---

### BI

Ne pas envoyer directement des données brutes dans le dashboard.

La chaîne recommandée est :

```text
Raw Data
   ↓
Cleaning
   ↓
Validation
   ↓
Feature Engineering
   ↓
PostgreSQL
   ↓
Superset
   ↓
Dashboard
   ↓
Business Insights
```


# 28. Résultat attendu

À la fin de cette procédure, le projet dispose de :

✅ Une base PostgreSQL `hotel_booking`

✅ Un utilisateur `sefdine`

✅ Un schéma `HotelBookings`

✅ Une table `hotelbookings`

✅ Un dataset nettoyé

✅ Des données importées depuis CSV

✅ Des requêtes SQL de contrôle

✅ Une base prête à être connectée à Apache Superset

✅ Une architecture Data Analytics complète


## Compétences démontrées

Ce workflow permet de démontrer des compétences en :

* PostgreSQL
* SQL
* Data Engineering
* Data Cleaning
* Pandas
* Feature Engineering
* Data Quality
* ETL
* Business Intelligence
* Apache Superset
* Data Visualization
