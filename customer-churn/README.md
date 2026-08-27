
# 📉 Customer Churn Analytics

## 1. Présentation du projet

Ce projet consiste à analyser le phénomène de désabonnement (churn) des clients d'une entreprise de télécommunications. L'objectif est d'identifier les profils à risque, de quantifier l'impact financier et de proposer des actions de fidélisation ciblées.

Le projet combine des techniques d'analyse statistique, de segmentation et de Machine Learning.


## 2. Objectifs business

- Quel est le taux de churn actuel ?
- Quels profils de clients sont les plus susceptibles de partir ?
- Le type de contrat, la durée d'ancienneté ou le montant des factures influencent-ils le churn ?
- Quels services (internet, téléphone, streaming) sont associés à un risque plus élevé ?
- Quels clients sont à risque et représentent une perte financière potentielle ?
- Comment prédire le churn pour agir en amont ?


## 3. Dataset

**Source** : [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

Ce dataset contient des informations sur 7 043 clients, avec des variables démographiques, contractuelles, d'utilisation des services et la variable cible `Churn` (Yes/No).


## 4. Technologies

- **Python** : analyse et modélisation
- **Pandas / NumPy** : manipulation et calculs
- **Matplotlib / Seaborn** : visualisations
- **Scikit-learn** : modélisation prédictive
- **Appache Superset** : dashboard interactif


## 5. Méthodologie

### Étape 1 : Data Understanding
- Exploration des dimensions (lignes, colonnes)
- Analyse des types de variables (numériques, catégorielles)
- Examen de la variable cible `Churn` (distribution)

### Étape 2 : Data Cleaning
- Traitement des valeurs manquantes (ex : `TotalCharges` avec des espaces)
- Conversion des types (ex : `TotalCharges` en numérique)
- Encodage des variables catégorielles en indices numériques (Label Encoding ou One-Hot Encoding)
- Vérification des valeurs aberrantes

### Étape 3 : Exploratory Data Analysis (EDA)
Analyse des relations entre le churn et les variables clés :

- `Contract` (type de contrat)
- `Tenure` (ancienneté)
- `MonthlyCharges` (montant mensuel)
- `InternetService`, `PhoneService`, `StreamingTV`, etc.
- `PaymentMethod` (mode de paiement)

Des graphiques (barres, boîtes à moustaches, heatmaps) sont utilisés pour visualiser ces relations.

### Étape 4 : Customer Segmentation
Création de segments de risque :

- **Low Risk** : clients avec contrat long, ancienneté élevée, faibles mensualités
- **Medium Risk** : clients avec contrat mensuel, ancienneté moyenne, mensualités moyennes
- **High Risk** : clients avec contrat mensuel, ancienneté faible, mensualités élevées

### Étape 5 : Machine Learning
Plusieurs modèles sont entraînés pour prédire le churn :

- **Logistic Regression** (baseline)
- **Random Forest Classifier**
- **Gradient Boosting Classifier** (XGBoost ou LightGBM)

Les modèles sont évalués sur les métriques suivantes :
- **Accuracy**
- **Precision**
- **Recall**
- **F1-Score**
- **ROC-AUC**

Un modèle est sélectionné pour être déployé dans le dashboard.


## 6. KPI

| KPI | Définition |
|-----|------------|
| **Total Customers** | Nombre total de clients |
| **Churned Customers** | Nombre de clients ayant quitté le service |
| **Churn Rate** | `Churned Customers / Total Customers × 100` |
| **Monthly Revenue** | Revenu mensuel total |
| **Revenue at Risk** | Revenu mensuel des clients à risque élevé |
| **Customers at Risk** | Nombre de clients identifiés comme à risque élevé |


## 7. Dashboard

### Page 1 : Executive Overview
- Total Customers, Churn Rate, Monthly Revenue, Revenue at Risk
- Évolution du churn dans le temps (si disponible)
- Répartition des clients par segment de risque

### Page 2 : Churn Analysis
- Churn par type de contrat (barres)
- Churn par ancienneté (histogramme)
- Churn par service utilisé (barres groupées)
- Churn par mode de paiement

### Page 3 : Customer Risk
- Liste des clients à risque élevé avec leurs caractéristiques
- Estimation du revenu potentiellement perdu par segment
- Filtres par type de contrat, service, etc.


## 8. Insights

Les résultats montrent :

- Les clients avec un contrat mensuel ont un taux de churn beaucoup plus élevé que ceux avec un contrat d'un an ou de deux ans.
- Les clients avec une ancienneté inférieure à 12 mois sont les plus enclins à partir.
- Les montants mensuels élevés sont associés à un risque plus grand.
- Les clients sans services additionnels (streaming, sécurité en ligne) churnent davantage.
- Le mode de paiement par chèque électronique est corrélé à un plus fort churn.


## 9. Recommandations

- **Offres personnalisées** : proposer des remises ou des avantages aux clients à risque élevé (ex : ancienneté faible, contrat mensuel).
- **Contrats adaptés** : inciter les clients à passer à des contrats plus longs avec des avantages tarifaires.
- **Actions ciblées** : contacter proactivement les clients à haut risque pour comprendre leurs raisons et proposer des solutions.
- **Amélioration des services** : promouvoir les services complémentaires (streaming, sécurité) qui réduisent le churn.
- **Campagnes de rétention** : mettre en place des programmes de fidélisation pour les clients à ancienneté intermédiaire.


## 10. Structure du projet

```
customer-churn/
│
├── data/
│   └── telco_churn.csv
│
├── notebooks/
│   └── churn_analysis.ipynb
│
├── models/
│   └── churn_model.pkl
│
├── powerbi/
│   └── churn_dashboard.pbix
│
├── screenshots/
│   └── dashboard.png
│
├── README.md
└── requirements.txt
```


## 11. Compétences démontrées

- Analyse exploratoire et statistique
- Segmentation client
- Machine Learning (classification, évaluation de modèles)
- Feature engineering et encodage
- Power BI
- Recommandations business basées sur les données


## 12. Conclusion

Ce projet de bout en bout illustre ma capacité à traiter un problème métier complexe (la fidélisation client) en utilisant une approche data-driven. La combinaison de l'analyse descriptive, de la modélisation prédictive et de la visualisation interactive permet de fournir des outils concrets pour réduire le churn et protéger les revenus de l'entreprise.