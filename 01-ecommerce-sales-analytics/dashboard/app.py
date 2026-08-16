import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path



# CONFIGURATION

st.set_page_config(
    page_title="E-commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)



# CHARGEMENT DES DONNÉES

DATA_PATH = Path("data/data.csv")

df = pd.read_csv(
    DATA_PATH,
    encoding="ISO-8859-1"
)



# NETTOYAGE


df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

df["IsCancelled"] = (
    df["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
)

# Dataset utilisé pour l'analyse commerciale

sales = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (~df["IsCancelled"])
].copy()


# FEATURE ENGINEERING

sales["Revenue"] = (
    sales["Quantity"] *
    sales["UnitPrice"]
)

sales["YearMonth"] = (
    sales["InvoiceDate"]
    .dt.to_period("M")
    .astype(str)
)

sales["Month"] = sales["InvoiceDate"].dt.month

sales["Hour"] = sales["InvoiceDate"].dt.hour



# SIDEBAR

st.sidebar.title("Filtres")

countries = sorted(
    sales["Country"]
    .dropna()
    .unique()
)

selected_country = st.sidebar.multiselect(
    "Pays",
    countries,
    default=[]
)


# APPLICATION DU FILTRE

filtered_sales = sales.copy()

if selected_country:
    filtered_sales = filtered_sales[
        filtered_sales["Country"].isin(
            selected_country
        )
    ]


# KPI

total_revenue = filtered_sales["Revenue"].sum()

total_orders = filtered_sales["InvoiceNo"].nunique()

total_customers = filtered_sales["CustomerID"].nunique()

total_quantity = filtered_sales["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# TITRE

st.title("🛒 E-commerce Sales Dashboard")

st.markdown(
    """
    **Analyse des performances commerciales**
    """
)


# KPI CARDS


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Chiffre d'affaires",
    f"{total_revenue:,.0f}"
)

col2.metric(
    "Commandes",
    f"{total_orders:,}"
)

col3.metric(
    "Clients",
    f"{total_customers:,}"
)

col4.metric(
    "Quantité vendue",
    f"{total_quantity:,}"
)

col5.metric(
    "Panier moyen",
    f"{average_order_value:,.2f}"
)


st.divider()


# CA MENSUEL

monthly_sales = (
    filtered_sales
    .groupby("YearMonth", as_index=False)
    ["Revenue"]
    .sum()
)

fig_monthly = px.line(
    monthly_sales,
    x="YearMonth",
    y="Revenue",
    markers=True,
    title="Évolution du chiffre d'affaires"
)

fig_monthly.update_layout(
    xaxis_title="Mois",
    yaxis_title="Chiffre d'affaires"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)



# ANALYSE PRODUITS

product_sales = (
    filtered_sales
    .groupby(
        ["StockCode", "Description"],
        as_index=False
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique")
    )
)


top_products = (
    product_sales
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


col1, col2 = st.columns(2)


with col1:

    fig_products = px.bar(
        top_products.sort_values("Revenue"),
        x="Revenue",
        y="Description",
        orientation="h",
        title="Top 10 produits par chiffre d'affaires"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


# PAYS

country_sales = (
    filtered_sales
    .groupby(
        "Country",
        as_index=False
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


with col2:

    fig_country = px.bar(
        country_sales.sort_values("Revenue"),
        x="Revenue",
        y="Country",
        orientation="h",
        title="Top 10 pays par chiffre d'affaires"
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )



# ANALYSE HORAIRE

hour_sales = (
    filtered_sales
    .groupby("Hour", as_index=False)
    ["Revenue"]
    .sum()
)


fig_hour = px.line(
    hour_sales,
    x="Hour",
    y="Revenue",
    markers=True,
    title="Chiffre d'affaires par heure"
)

fig_hour.update_layout(
    xaxis_title="Heure",
    yaxis_title="Chiffre d'affaires"
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)



# TOP CLIENTS

customer_sales = (
    filtered_sales
    .dropna(subset=["CustomerID"])
    .groupby(
        "CustomerID",
        as_index=False
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


st.subheader("Top 10 clients")

st.dataframe(
    customer_sales,
    use_container_width=True,
    hide_index=True
)



# TOP PRODUITS TABLE

st.subheader("Top 10 produits")

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)


# FOOTER

st.divider()

st.caption(
    "E-commerce Sales Analytics | "
    "Ahmed Sefdine"
)