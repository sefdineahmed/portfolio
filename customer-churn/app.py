import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Prédiction du Churn Client",
    
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Chargement des artefacts (avec cache pour optimiser les performances) ---
@st.cache_resource
def load_artifacts():
    model_path = Path("./models/churn_model.pkl")
    cols_path = Path("./models/feature_columns.pkl")
    
    # Vérification que les fichiers existent
    if not model_path.exists() or not cols_path.exists():
        st.error(" Modèle ou colonnes introuvables. Assurez-vous que le dossier 'models/' contient bien les fichiers générés.")
        return None, None
    
    model = joblib.load(model_path)
    feature_columns = joblib.load(cols_path)
    return model, feature_columns

model, feature_columns = load_artifacts()

# --- Titre principal ---
st.title(" Prédiction du Désabonnement Client (Churn)")
st.markdown("""
Cette application utilise un modèle **Random Forest** entraîné sur le dataset *Telco Customer Churn*.
Renseignez les caractéristiques du client ci-dessous pour estimer son risque de départ.
""")

# --- Barre latérale pour les instructions ---
with st.sidebar:
    st.header(" Comment ça marche ?")
    st.markdown("""
    1. Remplissez tous les champs du formulaire.
    2. Cliquez sur **"Prédire le Churn"**.
    3. Le modèle affichera la probabilité et le risque associé.
    """)
    st.divider()
    st.caption("Projet réalisé par Ahmed Sefdine")
    st.caption("Modèle entraîné avec un ROC-AUC ≈ 0.85")

# --- Création du formulaire (organisation en colonnes) ---
st.subheader(" Informations client")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Données démographiques**")
    gender = st.selectbox("Genre", options=["Male", "Female"])
    senior_citizen = st.checkbox("Senior Citizen (65+)")
    partner = st.selectbox("A un partenaire", options=["Yes", "No"])
    dependents = st.selectbox("A des personnes à charge", options=["Yes", "No"])
    
    st.markdown("**Contrat & Facturation**")
    contract = st.selectbox("Type de contrat", options=["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Facture dématérialisée", options=["Yes", "No"])
    payment_method = st.selectbox("Mode de paiement", options=[
        "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
    ])

with col2:
    st.markdown("**Services téléphoniques**")
    phone_service = st.selectbox("Service téléphonique", options=["Yes", "No"])
    multiple_lines = st.selectbox("Lignes multiples", options=["No", "Yes", "No phone service"])
    
    st.markdown("**Services Internet**")
    internet_service = st.selectbox("Service Internet", options=["DSL", "Fiber optic", "No"])
    
    if internet_service != "No":
        online_security = st.selectbox("Sécurité en ligne", options=["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Sauvegarde en ligne", options=["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Protection des appareils", options=["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Support technique", options=["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", options=["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Films", options=["No", "Yes", "No internet service"])
    else:
        # Si pas d'Internet, ces services sont automatiquement "No internet service"
        online_security = online_backup = device_protection = tech_support = streaming_tv = streaming_movies = "No internet service"

with col3:
    st.markdown("**Utilisation & Montants**")
    tenure = st.slider("Ancienneté (mois)", min_value=0, max_value=72, value=12, step=1)
    monthly_charges = st.number_input("Montant mensuel ($)", min_value=0.0, max_value=150.0, value=70.0, step=1.0)
    total_charges = st.number_input("Total facturé ($)", min_value=0.0, max_value=9000.0, value=500.0, step=50.0)

# --- Bouton de prédiction ---
st.divider()
predict_btn = st.button(" Prédire le Churn", type="primary", use_container_width=True)

# --- Fonction de préprocessing (identique à l'entraînement) ---
def preprocess_input(data_dict):
    """
    Transforme le dictionnaire saisi en DataFrame prêt pour la prédiction.
    Applique le One-Hot Encoding et réindexe sur les colonnes de l'entraînement.
    """
    # 1. Création du DataFrame à partir d'un seul enregistrement
    df_input = pd.DataFrame([data_dict])
    
    # 2. Conversion de SeniorCitizen en int (0/1) car dans le dataset c'est numérique
    df_input['SeniorCitizen'] = df_input['SeniorCitizen'].astype(int)
    
    # 3. Application de One-Hot Encoding (même méthode que pd.get_dummies)
    df_processed = pd.get_dummies(df_input, drop_first=True)
    
    # 4. Réindexation sur les colonnes utilisées lors de l'entraînement
    # (les colonnes manquantes sont remplies avec 0, les colonnes en trop sont supprimées)
    df_processed = df_processed.reindex(columns=feature_columns, fill_value=0)
    
    # 5. Vérification qu'il n'y a pas de colonnes NaN
    assert df_processed.isnull().sum().sum() == 0, "Des valeurs NaN sont apparues lors du preprocessing."
    
    return df_processed

# --- Logique de prédiction ---
if predict_btn:
    if model is None or feature_columns is None:
        st.error(" Le modèle n'a pas pu être chargé. Vérifiez les fichiers.")
    else:
        # Construction du dictionnaire à partir des entrées utilisateur
        input_data = {
            'gender': gender,
            'SeniorCitizen': senior_citizen,  # booléen, sera converti en int
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }
        
        # Préparation des données
        X_input = preprocess_input(input_data)
        
        # Prédiction (probabilité)
        proba_churn = model.predict_proba(X_input)[0][1]  # probabilité de la classe 1 (Yes)
        prediction = model.predict(X_input)[0]  # 0 ou 1
        
        # --- Affichage des résultats ---
        st.divider()
        st.subheader(" Résultat de la prédiction")
        
        # Métriques et style
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            st.metric("Risque de Churn", f"{proba_churn * 100:.1f} %")
        
        with col_metric2:
            statut = " À RISQUE" if prediction == 1 else "FIDÈLE"
            st.metric("Statut client", statut)
        
        with col_metric3:
            # Couleur selon le seuil (on fixe un seuil de 0.5, ajustable)
            niveau = "Élevé" if proba_churn > 0.7 else "Modéré" if proba_churn > 0.4 else "Faible"
            st.metric("Niveau de risque", niveau)
        
        # Barre de progression visuelle
        st.markdown("**Probabilité de désabonnement**")
        st.progress(proba_churn, text=f"{proba_churn*100:.0f}%")
        
        # Interprétation et suggestion
        st.divider()
        st.subheader("Recommandation")
        
        if prediction == 1:
            st.warning("""
             **Ce client présente un risque élevé de départ.**  
            **Actions suggérées :**
            - Proposer un contrat d'engagement (1 an ou 2 ans) avec une réduction.
            - Améliorer la qualité du service (suivi personnalisé).
            - Offrir des services complémentaires (sécurité, streaming) en promotion.
            """)
        else:
            st.success("""
            **Ce client a une forte probabilité de rester.**  
            **Actions suggérées :**
            - Maintenir la qualité du service.
            - Programme de fidélisation pour le récompenser.
            - Profil à surveiller périodiquement.
            """)
        
        # Détail technique (dépliable)
        with st.expander(" Voir les détails techniques de l'entrée"):
            st.write("Données encodées envoyées au modèle :")
            st.dataframe(X_input.style.highlight_max(axis=1), use_container_width=True)
            
            # Afficher les colonnes avec des valeurs non nulles
            active_features = X_input.columns[X_input.iloc[0] == 1].tolist()
            st.write(f"**Features actives (binaires) :** {len(active_features)}")
            if active_features:
                st.write(active_features[:20])  # Limite pour lisibilité