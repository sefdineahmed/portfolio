# 🚕 NYC Taxi Data Analytics

## 1. Présentation du projet

Ce projet vise à analyser les données de trajets de taxis jaunes à New York afin d'identifier les tendances de mobilité, les périodes de forte activité et les facteurs influençant les revenus des courses.

L'accent est mis sur l'utilisation de **SQL** pour l'extraction, le nettoyage et l'analyse des données, complétée par des visualisations sous Power BI.


## 2. Objectifs business

Les questions auxquelles ce projet répond :

- Combien de courses sont effectuées chaque jour/semaine/mois ?
- Quels sont les jours et heures de pointe ?
- Quelle est la distance moyenne parcourue par course ?
- Quel est le revenu moyen par course ?
- Quelles zones de prise en charge sont les plus fréquentées ?
- Quels facteurs (distance, durée, heure) influencent le montant payé ?
- Comment les revenus évoluent-ils dans le temps ?


## 3. Dataset

**Source** : [Kaggle - NYC Yellow Taxi Trip Data](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data)

Ce dataset contient des millions d'enregistrements de trajets, avec des informations détaillées sur les lieux, les temps, les distances, les montants et les pourboires.


## 4. Technologies

- **PostgreSQL** : base de données relationnelle
- **SQL** : requêtes d'analyse et de préparation
- **Python** : chargement initial et post-traitement
- **Pandas** : manipulation complémentaire
- **Power BI** : création du dashboard final


## 5. Méthodologie

### Étape 1 : Data Loading
- Téléchargement des fichiers CSV
- Importation dans PostgreSQL via `COPY` ou `pgAdmin`
- Création des index pour optimiser les performances

### Étape 2 : Data Quality
- Contrôle des valeurs nulles dans les colonnes critiques (`pickup_datetime`, `dropoff_datetime`, `fare_amount`, etc.)
- Filtrage des distances aberrantes (ex : > 100 miles)
- Suppression des montants négatifs ou nuls
- Vérification des durées anormales (ex : > 24h)
- Élimination des enregistrements avec un nombre de passagers invalide (0 ou > 6)

### Étape 3 : Analyse avec SQL
Les requêtes SQL exploitent :

- `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`
- `JOIN` entre tables (si plusieurs fichiers)
- Common Table Expressions (`WITH`) pour des calculs intermédiaires
- Fenêtrage (`ROW_NUMBER`, `RANK`) pour les classements
- Fonctions de date (`EXTRACT`, `DATE_TRUNC`) pour l'analyse temporelle
- `CASE WHEN` pour le regroupement en catégories

Exemples de requêtes :
- Nombre de courses par heure
- Distance moyenne par jour de la semaine
- Revenu total par mois
- Top 10 des zones de prise en charge
- Corrélation entre distance et montant

### Étape 4 : Feature Engineering
Création de nouvelles colonnes dans la base ou en Python :

- `Year`, `Month`, `Day`, `Hour`
- `DayOfWeek` (1 = lundi, 7 = dimanche)
- `TripDuration` = `dropoff_datetime - pickup_datetime`
- `Speed` = `trip_distance / trip_duration` (en miles par heure)


## 6. KPI

| KPI | Définition |
|-----|------------|
| **Total Trips** | Nombre total de courses |
| **Average Trip Distance** | Distance moyenne parcourue |
| **Average Fare** | Montant moyen facturé (hors pourboire) |
| **Total Revenue** | Somme des `fare_amount` |
| **Revenue per Trip** | Revenu moyen par course |
| **Average Trip Duration** | Durée moyenne des trajets |


## 7. Dashboard

Un dashboard Power BI est conçu pour visualiser les indicateurs clés :

- **Courses par heure** (histogramme)
- **Courses par jour de la semaine** (barres)
- **Revenus par mois** (courbe)
- **Distance moyenne par mois**
- **Top 10 zones de prise en charge** (carte ou barres)
- **Revenus par zone** (carte thermique)

Des filtres permettent de segmenter par date, heure et zone.


## 8. Insights

L'analyse fait ressortir :

- Les heures de pointe (8h-10h et 17h-19h)
- Les jours les plus actifs (vendredi, samedi)
- Les zones à forte demande (aéroports, Manhattan)
- Les périodes de l'année générant le plus de revenus (décembre, septembre)
- La relation positive entre distance et montant facturé


## 9. Recommandations

- **Allocation des taxis** : renforcer la flotte aux heures et dans les zones de pointe.
- **Tarification** : envisager des majorations dynamiques aux heures de forte demande.
- **Opérations** : optimiser les itinéraires pour réduire les temps d'attente.
- **Communication** : informer les chauffeurs des zones à fort potentiel.


## 10. Structure du projet

```
03-nyc-taxi-analytics/
│
├── data/
│   └── taxi_trips.csv
│
├── sql/
│   ├── cleaning.sql
│   ├── exploration.sql
│   └── kpi.sql
│
├── notebooks/
│   └── post_processing.ipynb
│
├── powerbi/
│   └── taxi_dashboard.pbix
│
├── screenshots/
│   └── dashboard.png
│
├── README.md
└── requirements.txt
```


## 11. Compétences démontrées

- SQL avancé (PostgreSQL)
- Data cleaning et validation
- Analyse temporelle et géospatiale
- Modélisation de données
- Création de dashboards Power BI
- Synthèse et recommandations stratégiques


## 12. Conclusion

Ce projet illustre ma maîtrise de SQL pour l'analyse de gros volumes de données et ma capacité à en extraire des insights opérationnels. La combinaison avec Power BI permet de rendre ces résultats accessibles à des décideurs métier.