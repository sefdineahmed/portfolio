# Fiche mémo : PostgreSQL, CSV et Superset

## 1. PostgreSQL fonctionne avec des bases, schémas et tables

La hiérarchie est :

```text
PostgreSQL
│
├── Base de données : superstore_bi2
│   │
│   └── Schéma : SalesAnalytics
│       │
│       └── Table : salesanalytics
│
└── Autres bases...
```

Un **schéma appartient à une base de données**.
On ne peut pas utiliser directement le même schéma entre deux bases.


## 2. Créer une base

Depuis le **terminal Linux** :

```bash
sudo -u postgres createdb superstore_bi2
```

`postgres` est généralement l'utilisateur administrateur PostgreSQL.

Si la base existe déjà :

```text
database "superstore_bi2" already exists
```

➡️ Il ne faut pas la recréer.

## 3. Donner la propriété d'une base

Si `sefdine` doit travailler directement sur la base :

```bash
sudo -u postgres psql -c "ALTER DATABASE superstore_bi2 OWNER TO sefdine;"
```

À retenir :

```text
sudo -u postgres
```

➡️ exécute la commande avec l'utilisateur PostgreSQL `postgres`.


## 4. Se connecter à une base

Depuis le terminal :

```bash
psql -d superstore_bi2
```

Avec un utilisateur précis :

```bash
psql -h localhost -p 5432 -U sefdine -d superstore_bi2
```

Une fois connecté, tu vois :

```text
superstore_bi2=>
```

À partir de là, tu es **dans PostgreSQL**.


# 5. Différence entre Linux et PostgreSQL

C'est l'un des points les plus importants.

### Terminal Linux

```text
(base) sefdine@sefdine:~$
```

Ici tu peux faire :

```bash
sudo ...
psql ...
ls ...
docker ...
```

### PostgreSQL

```text
superstore_bi2=>
```

Ici tu peux faire :

```sql
SELECT ...
CREATE TABLE ...
CREATE SCHEMA ...
GRANT ...
```

Et les commandes `psql` :

```sql
\copy
\dt
\dn
\d
\q
```

### Exemple

❌ Ne pas faire :

```text
superstore_bi2=> sudo -u postgres ...
```

Parce que `sudo` est une commande Linux.

Il faut d'abord :

```sql
\q
```

puis exécuter `sudo` dans le terminal.


# 6. Créer un schéma

```sql
CREATE SCHEMA IF NOT EXISTS "SalesAnalytics";
```

`IF NOT EXISTS` signifie :

> Créer le schéma seulement s'il n'existe pas déjà.

Les guillemets sont importants ici parce que tu utilises :

```text
SalesAnalytics
```

avec des majuscules.


# 7. Créer une table

Ta table est :

```sql
CREATE TABLE "SalesAnalytics"."salesanalytics" (
    "InvoiceNo" VARCHAR(20),
    "StockCode" VARCHAR(30),
    "Description" TEXT,
    "Quantity" INTEGER,
    "InvoiceDate" TIMESTAMP,
    "UnitPrice" NUMERIC(12,4),
    "CustomerID" INTEGER,
    "Country" VARCHAR(100)
);
```

À retenir :

| Type            | Utilisation                  |
| --------------- | ---------------------------- |
| `VARCHAR(n)`    | Texte avec longueur maximale |
| `TEXT`          | Texte libre                  |
| `INTEGER`       | Nombre entier                |
| `NUMERIC(12,4)` | Nombre décimal précis        |
| `TIMESTAMP`     | Date + heure                 |


# 8. `COPY` vs `\copy`

C'est **très important**.

### `COPY`

```sql
COPY "SalesAnalytics"."salesanalytics"
FROM '/chemin/data.csv';
```

`COPY` demande au **serveur PostgreSQL** de lire le fichier.

Donc PostgreSQL doit avoir accès au fichier.

C'est pourquoi tu avais :

```text
permission denied
```

### `\copy`

```sql
\copy "SalesAnalytics"."salesanalytics"
FROM '/chemin/data.csv'
WITH (...);
```

`\copy` est une commande de **psql**.

Elle permet au **client qui exécute psql** de lire le fichier local.

👉 Pour importer un CSV présent sur ton ordinateur avec `psql`, pense généralement à :

```text
\copy
```

---

# 9. Importer un CSV

Dans ton cas :

```sql
\copy "SalesAnalytics"."salesanalytics"
FROM '/home/sefdine/github/sefdine-analytics-portfolio/01-ecommerce-sales-analytics/data/data.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);
```

### Les paramètres importants

```text
FORMAT CSV
```

➡️ Le fichier est au format CSV.

```text
HEADER TRUE
```

➡️ La première ligne contient les noms des colonnes.

```text
DELIMITER ','
```

➡️ Les colonnes sont séparées par une virgule.

Si le fichier utilise `;` :

```text
DELIMITER ';'
```


# 10. Problème de format des dates

Ton CSV contenait :

```text
12/13/2010 9:02
```

C'est le format :

```text
MM/DD/YYYY HH:MI
```

PostgreSQL interprétait mal la date.

La solution utilisée :

```sql
SET datestyle = 'ISO, MDY';
```

À retenir :

```text
MDY = Month / Day / Year
```

Donc :

```text
12/13/2010
```

signifie :

```text
Décembre 13, 2010
```


# 11. Problème d'encodage

Tu as ensuite rencontré :

```text
invalid byte sequence for encoding "UTF8"
```

Cela signifie que le CSV n'était probablement pas encodé en UTF-8.

On peut indiquer l'encodage dans `COPY` :

```sql
ENCODING 'WIN1252'
```

Par exemple :

```sql
\copy "SalesAnalytics"."salesanalytics"
FROM '/chemin/data.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    ENCODING 'WIN1252'
);
```

On peut aussi vérifier l'encodage du fichier avec Linux :

```bash
file -bi /chemin/data.csv
```


# 12. Vérifier les données

Après l'import :

### Compter les lignes

```sql
SELECT COUNT(*)
FROM "SalesAnalytics"."salesanalytics";
```

### Voir quelques lignes

```sql
SELECT *
FROM "SalesAnalytics"."salesanalytics"
LIMIT 10;
```

### Voir la structure

Dans `psql` :

```sql
\d "SalesAnalytics"."salesanalytics"
```

Ou avec SQL :

```sql
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'SalesAnalytics'
  AND table_name = 'salesanalytics'
ORDER BY ordinal_position;
```

# 13. Vérifier PostgreSQL

Pour vérifier que PostgreSQL fonctionne :

```bash
sudo systemctl status postgresql
```

Tu avais :

```text
Active: active
```

➡️ PostgreSQL fonctionne.


# 14. Vérifier le port PostgreSQL

Tu as utilisé :

```bash
sudo ss -lntp | grep 5432
```

Et obtenu :

```text
127.0.0.1:5432
```

À retenir :

```text
5432
```

➡️ Port PostgreSQL par défaut.

```text
127.0.0.1
```

➡️ PostgreSQL écoute sur la machine locale.

# 15. Tester une connexion PostgreSQL

Tu as testé :

```bash
psql -h localhost -p 5432 -U sefdine -d superstore_bi2
```

Et obtenu :

```text
superstore_bi2=>
```

Cela confirme que :

* PostgreSQL fonctionne ;
* le port `5432` fonctionne ;
* la base `superstore_bi2` existe ;
* l'utilisateur `sefdine` peut se connecter ;
* l'authentification fonctionne.


# 16. Connexion PostgreSQL → Superset

Dans Superset, les informations importantes sont :

```text
Host
Port
Database name
Username
Password
```

Dans une installation **directe sur la même machine**, tu utiliserais généralement :

```text
Host       : 127.0.0.1
Port       : 5432
Database   : superstore_bi2
Username   : sefdine
Password   : ton mot de passe PostgreSQL
```

⚠️ Mais si Superset tourne dans **Docker**, `127.0.0.1` désigne le conteneur Superset et non nécessairement ta machine Ubuntu.

C'est donc un point essentiel à vérifier.



# 17. Les commandes que tu dois vraiment mémoriser

Si tu fais régulièrement des projets **PostgreSQL + CSV + Superset**, retiens surtout celles-ci :

### Connexion

```bash
psql -d superstore_bi2
```

### Quitter PostgreSQL

```sql
\q
```

### Voir les bases

```sql
\l
```

### Voir les schémas

```sql
\dn
```

### Voir les tables

```sql
\dt
```

### Voir la structure d'une table

```sql
\d "SalesAnalytics"."salesanalytics"
```

### Compter les lignes

```sql
SELECT COUNT(*)
FROM "SalesAnalytics"."salesanalytics";
```

### Importer un CSV local

```sql
\copy "SalesAnalytics"."salesanalytics"
FROM '/chemin/data.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);
```

### Voir l'utilisateur connecté

```sql
SELECT current_user;
```

### Voir la base courante

```sql
SELECT current_database();
```

## Le workflow à retenir

Pour un projet Data Analytics comme ton projet **E-commerce Sales Analytics**, tu peux retenir ce workflow :

```text
CSV
 │
 ▼
Vérifier le fichier
 │
 ▼
Créer la base PostgreSQL
 │
 ▼
Créer le schéma
 │
 ▼
Créer la table
 │
 ▼
Importer avec \copy
 │
 ▼
Vérifier COUNT(*) + SELECT
 │
 ▼
Connecter PostgreSQL à Superset
 │
 ▼
Créer les datasets / dashboards
```