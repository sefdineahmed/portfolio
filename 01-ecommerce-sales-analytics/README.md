# 🛒 E-commerce Sales Analytics

## 1. Présentation du projet

Ce projet a pour objectif d'analyser les données de ventes d'une entreprise de e-commerce afin de comprendre sa performance commerciale, d'identifier les produits et clients les plus rentables, et de dégager des tendances exploitables pour la prise de décision stratégique.

Les données transactionnelles brutes sont transformées en indicateurs clés et en recommandations opérationnelles.

## 2. Objectifs business

L'analyse répond aux questions suivantes :

- Quel est le chiffre d'affaires total et son évolution dans le temps ?
- Quels sont les produits les plus vendus et ceux qui génèrent le plus de revenus ?
- Quels clients sont les plus importants en termes de valeur ?
- Quels pays contribuent le plus au chiffre d'affaires ?
- Quel est le panier moyen et comment se distribue-t-il ?
- Existe-t-il des saisonnalités ou des tendances temporelles ?
- Quels produits affichent des performances faibles et nécessitent une attention particulière ?


## 3. Dataset

**Source** : [Kaggle - E-commerce Data](https://www.kaggle.com/datasets/carrie1/ecommerce-data)

### Variables principales

| Variable | Description |
|----------|-------------|
| `InvoiceNo` | Numéro de facture (identifiant de transaction) |
| `StockCode` | Code unique du produit |
| `Description` | Description textuelle du produit |
| `Quantity` | Quantité achetée |
| `InvoiceDate` | Date et heure de la transaction |
| `UnitPrice` | Prix unitaire du produit |
| `CustomerID` | Identifiant anonymisé du client |
| `Country` | Pays du client |


## 4. Technologies utilisées

- **Python** : langage principal
- **Pandas** : manipulation et analyse des données
- **NumPy** : calculs numériques
- **Matplotlib** : visualisations statiques
- **Seaborn** : graphiques statistiques avancés
- **Jupyter Notebook** : environnement de développement interactif


## 5. Méthodologie

### Étape 1 : Importation et exploration initiale
- Chargement du fichier CSV
- Affichage des premières lignes et des informations générales
- Identification des dimensions (lignes, colonnes) et des types de variables

### Étape 2 : Nettoyage des données
- Traitement des valeurs manquantes (suppression ou imputation)
- Suppression des doublons
- Filtrage des quantités négatives (annulations ou erreurs)
- Vérification des prix unitaires (valeurs aberrantes)
- Conversion de `InvoiceDate` en type datetime
- Nettoyage des identifiants clients invalides

### Étape 3 : Feature Engineering
Création de nouvelles variables pour enrichir l'analyse :
- `Revenue` = `Quantity × UnitPrice`
- `Year`, `Month`, `Day`, `Hour` extraits de `InvoiceDate`
- `DayOfWeek` pour analyser les tendances hebdomadaires

### Étape 4 : Analyse exploratoire (EDA)
- Calcul du chiffre d'affaires mensuel et évolution temporelle
- Répartition du CA par pays
- Top produits par quantité vendue et par CA
- Distribution des commandes et du panier moyen
- Analyse des clients : nombre de commandes, CA total, panier moyen par client


## 6. Indicateurs clés de performance (KPI)

| KPI | Définition |
|-----|------------|
| **Total Revenue** | Somme de `Revenue` sur l'ensemble des transactions |
| **Total Orders** | Nombre de factures distinctes |
| **Total Customers** | Nombre de clients uniques |
| **Average Order Value (AOV)** | `Total Revenue / Total Orders` |
| **Total Quantity Sold** | Somme des quantités vendues |
| **Revenue per Customer** | `Total Revenue / Total Customers` |
| **Revenue per Country** | CA par pays |


## 7. Visualisations

Les graphiques suivants sont réalisés pour faciliter l'interprétation :

- **Évolution du CA** (ligne temporelle par mois)
- **Top 10 produits** par CA et par quantité
- **Top 10 clients** par CA
- **Répartition géographique** du CA (carte ou barres)
- **Distribution mensuelle** des ventes
- **Histogramme du panier moyen** pour identifier les segments de clients

---

## 8. Insights

Les analyses mettent en évidence :

- Les produits les plus performants (fort volume et/ou forte marge)
- Les marchés géographiques prioritaires
- Les pics d'activité saisonniers (ex : fin d'année)
- Les clients à forte valeur ajoutée
- Les produits à faible rotation ou à marge insuffisante


## 9. Recommandations business

À partir des résultats, les actions suivantes sont proposées :

- **Gestion des produits** : renforcer l'approvisionnement des meilleurs vendeurs, envisager des promotions pour écouler les invendus.
- **Marketing** : cibler les clients à forte valeur avec des offres personnalisées ; adapter les campagnes aux périodes de forte demande.
- **Fidélisation** : mettre en place un programme de fidélité pour les clients les plus actifs.
- **Stocks** : ajuster les niveaux de stock en fonction des tendances saisonnières.
- **Marchés** : concentrer les efforts sur les pays à fort potentiel de croissance.


## 10. Structure du projet

```
01-ecommerce-sales-analytics/
│
├── data/
│   └── ecommerce.csv
│
├── notebooks/
│   └── ecommerce_analysis.ipynb
│
├── images/
│   └── charts/
│
├── README.md
└── requirements.txt
```


## 11. Conclusion

Ce projet démontre ma capacité à transformer des données transactionnelles brutes en informations stratégiques. La méthodologie rigoureuse et les livrables (KPI, visualisations, recommandations) permettent de soutenir la prise de décision opérationnelle et d'identifier des leviers de croissance concrets.


## 12. Compétences démontrées

- Nettoyage et préparation de données avec Pandas
- Analyse exploratoire et visualisation
- Construction d'indicateurs business
- Synthèse et recommandations orientées action
- Utilisation de Jupyter Notebook pour une documentation reproductible