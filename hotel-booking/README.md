# 🏨 Hotel Booking Analytics

## 1. Présentation du projet

Ce projet analyse les données de réservations hôtelières pour comprendre le comportement des clients, les taux d'annulation et les performances commerciales des deux hôtels (Resort Hotel et City Hotel). L'objectif est d'identifier les leviers pour réduire les annulations et optimiser la gestion des capacités.

## 2. Objectifs business

Les principales questions :

- Quel est le taux d'annulation global et par type d'hôtel ?
- Quels mois enregistrent le plus de réservations et d'annulations ?
- Quels segments de clients annulent le plus ?
- Quel est le délai moyen entre la réservation et l'arrivée (lead time) ?
- Quels canaux de distribution génèrent le plus de réservations ?
- Quelle est la durée moyenne des séjours ?
- Quels segments sont les plus rentables ?

---

## 3. Dataset

**Source** : [Kaggle - Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)

Ce jeu de données contient des informations sur les réservations de deux hôtels, avec des variables telles que les dates, le nombre d'adultes/enfants, les annulations, les canaux de distribution, etc.


## 4. Technologies

- **Python** : analyse exploratoire et préparation
- **Pandas** : manipulation des données
- **NumPy** : calculs numériques
- **Matplotlib / Seaborn** : visualisations
- **Appache Superset** : dashboard interactif


## 5. Méthodologie

### Étape 1 : Data Understanding
- Exploration des variables (types, distributions, valeurs manquantes)
- Analyse des valeurs aberrantes et des incohérences

### Étape 2 : Data Cleaning
- Traitement des valeurs manquantes (ex : `children` remplacé par 0)
- Nettoyage des dates (conversion en datetime)
- Standardisation des variables catégorielles (ex : `meal`, `market_segment`)
- Suppression des doublons éventuels

### Étape 3 : Feature Engineering
Création de nouvelles variables :
- `Total Guests` = `adults + children + babies`
- `Total Nights` = `stays_in_weekend_nights + stays_in_week_nights`
- `Booking Month`, `Booking Year`
- `Lead Time Category` (ex : "0-30 jours", "31-90 jours", ">90 jours")
- `Is Cancelled` (booléen)

### Étape 4 : Analyse exploratoire
- Répartition des réservations par mois et par type d'hôtel
- Taux d'annulation par segment, par mois, par canal
- Durée moyenne des séjours par type d'hôtel
- Relation entre lead time et annulation
- Canaux de distribution les plus utilisés


## 6. KPI

| KPI | Définition |
|-----|------------|
| **Total Bookings** | Nombre total de réservations |
| **Cancellation Rate** | (Réservations annulées / Total réservations) × 100 |
| **Average Stay** | Nombre moyen de nuits par réservation |
| **Average Lead Time** | Délai moyen entre réservation et arrivée |
| **Bookings by Channel** | Répartition par canal de distribution |
| **Bookings by Customer Type** | Répartition par type de client |


## 7. Dashboard

### Page 1 : Vue d'ensemble
- Total des réservations, taux d'annulation, séjour moyen, lead time moyen
- Évolution mensuelle des réservations et annulations
- Répartition par type d'hôtel

### Page 2 : Analyse client
- Taux d'annulation par type de client (`Transient`, `Group`, etc.)
- Taux d'annulation par canal de distribution
- Durée de séjour moyenne par type de client
- Distribution des lead times

### Page 3 : Analyse temporelle et géographique
- Saisonnalité des réservations
- Annulations par mois
- Carte des pays d'origine des clients (si disponible)


## 8. Insights

Les analyses révèlent :

- Un taux d'annulation plus élevé pour le City Hotel que pour le Resort Hotel.
- Les mois d'été (juillet, août) concentrent le plus de réservations.
- Les clients de type `Transient` annulent davantage que les groupes.
- Les canaux en ligne (OTA) génèrent plus d'annulations que les canaux directs.
- Un lead time élevé est corrélé à un risque d'annulation plus important.


## 9. Recommandations

- **Politique d'annulation** : renforcer les pénalités pour les annulations tardives, surtout pour le City Hotel.
- **Gestion des réservations** : proposer des offres flexibles pour réduire les annulations en haute saison.
- **Marketing** : cibler les canaux directs pour fidéliser les clients et réduire les annulations.
- **Fidélisation** : récompenser les clients à faible taux d'annulation.
- **Capacité** : ajuster les surréservations en fonction des tendances d'annulation.


## 10. Structure du projet

```
hotel-booking/
│
├── data/
│   └── hotel_bookings.csv
│
├── notebooks/
│   └── hotel_booking_analysis.ipynb
│
├── powerbi/
│   └── hotel_dashboard.pbix
│
├── screenshots/
│   └── dashboard.png
│
├── README.md
└── requirements.txt
```


## 11. Compétences démontrées

- Python (Pandas, Seaborn)
- Analyse exploratoire approfondie
- Feature engineering
- KPI et mesure de performance
- Appache Superset
- Recommandations orientées métier


## 12. Conclusion

Ce projet montre ma capacité à analyser un secteur spécifique (hôtellerie) et à fournir des recommandations concrètes pour réduire les annulations et optimiser la gestion des réservations. La démarche est reproductible et s'appuie sur des données réelles.