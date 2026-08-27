# Superstore Business Intelligence Dashboard

## 1. Présentation du projet

Ce projet consiste à développer une solution de Business Intelligence complète pour permettre à la direction d'une entreprise de suivre en temps réel la performance commerciale, la rentabilité et les tendances de ses ventes.

L'objectif est de construire un modèle de données robuste, de définir des indicateurs avec DAX et de livrer un dashboard interactif sous Power BI.


## 2. Objectifs business

Le dashboard doit répondre aux questions stratégiques suivantes :

- Quel est le chiffre d'affaires global et le bénéfice net ?
- Quelle est la marge bénéficiaire par produit, catégorie et région ?
- Quelles régions sont les plus performantes ?
- Quels produits génèrent le plus de bénéfices et lesquels sont déficitaires ?
- Quels clients sont les plus rentables ?
- Comment les ventes et les bénéfices évoluent-ils dans le temps ?


## 3. Dataset

**Source** : [Kaggle - Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

Le jeu de données contient les ventes d'une grande surface américaine sur plusieurs années, avec des informations détaillées sur les commandes, les produits, les clients et les régions.

---

## 4. Technologies

- **Appache Superset** : création du dashboard interactif
- ~~**Power Query** : préparation et nettoyage des données~~
- ~~**DAX** : création de mesures et de KPI~~
- **Excel** : exploration initiale
- ~~**Data Modeling** : conception du modèle en étoile~~


## 5. Méthodologie

### Étape 1 : Data Preparation
- Importation des données depuis un fichier Excel
- Nettoyage des valeurs manquantes (suppression ou remplacement)
- Vérification et correction des types de données
- Suppression des doublons éventuels
- Création de colonnes calculées (ex : `Year`, `Month`)

### Étape 2 : Data Modeling
Création d'un modèle en étoile avec les tables suivantes :

```
                Dim_Date
                    |
                    |
Dim_Product --- Fact_Sales --- Dim_Customer
                    |
                    |
                Dim_Region
```

- **Fact_Sales** : table des faits contenant les montants, quantités, etc.
- **Dim_Date** : dimensions temporelles (date, année, mois, trimestre)
- **Dim_Product** : dimensions produit (catégorie, sous-catégorie, nom)
- **Dim_Customer** : dimensions client (nom, segment)
- **Dim_Region** : dimensions géographiques (région, état, ville)

Les relations sont définies selon un schéma en étoile pour optimiser les performances et la clarté du modèle.

### Étape 3 : Création des KPI 

Exemples de mesures:

```DAX
Total Sales = SUM(Sales[Sales])

Total Profit = SUM(Sales[Profit])

Total Orders = DISTINCTCOUNT(Sales[Order ID])

Profit Margin = DIVIDE([Total Profit], [Total Sales])
```

D'autres mesures sont créées pour l'analyse par catégorie, par client, par région, etc.


## 6. Dashboard

### Page 1 : Executive Overview
- **KPI** : Total Sales, Total Profit, Total Orders, Profit Margin
- **Visualisations** :
  - Évolution des ventes et du profit (graphique en courbes)
  - Ventes par région (carte ou barres)
  - Ventes par catégorie (graphique en anneau)
  - Top 5 produits par profit

### Page 2 : Product Analysis
- Top 10 des produits par profit
- Bottom 10 des produits par profit (produits déficitaires)
- Ventes par catégorie et sous-catégorie
- Matrice de rentabilité (profit vs volume)

### Page 3 : Customer Analysis
- Top 10 clients par revenu et par profit
- Nombre de commandes par client
- Répartition géographique des clients
- Analyse de la valeur client (RFM simplifié)


## 7. Business Insights

Les analyses permettent d'identifier :

- Les régions les plus rentables (ex : Est, Ouest)
- Les catégories de produits à forte marge (ex : technologies, mobilier)
- Les sous-catégories déficitaires (ex : tables, fournitures)
- Les clients à forte valeur ajoutée (segment "Consumer" souvent en tête)
- Les tendances saisonnières (pics en fin d'année)


## 8. Recommandations

- **Produits** : renforcer les gammes les plus rentables, envisager des ajustements de prix ou des arrêts pour les produits déficitaires.
- **Régions** : investir davantage dans les régions à fort potentiel de croissance.
- **Clients** : développer des programmes de fidélisation pour les meilleurs clients.
- **Politique commerciale** : ajuster les remises pour améliorer la marge globale.
- **Gestion des stocks** : aligner les niveaux de stock sur les pics saisonniers.


## 9. Structure du projet

```
superstore-bi/
│
├── data/
│   └── superstore.xlsx
│
├── powerbi/
│   └── superstore_dashboard.pbix
│
├── screenshots/
│   ├── overview.png
│   ├── product.png
│   └── customer.png
│
├── README.md
└── documentation/
    └── data_dictionary.md
```


## 10. Compétences démontrées

- création de dashboards interactifs
- ETL
- mesures et KPI
- Analyse business et traduction en indicateurs
- Data storytelling


## 11. Conclusion

Ce projet illustre ma capacité à concevoir une solution BI complète, depuis la préparation des données jusqu'à la livraison d'un tableau de bord opérationnel. Il démontre une maîtrise des outils Microsoft et une compréhension approfondie des besoins métier en matière de pilotage de la performance.