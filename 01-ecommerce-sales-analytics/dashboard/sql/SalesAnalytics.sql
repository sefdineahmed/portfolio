-- E-COMMERCE SALES ANALYTICS
-- Database : superset_bi
-- Schema   : SalesAnalytics


-- 1. CREATION DU SCHEMA

CREATE SCHEMA IF NOT EXISTS "SalesAnalytics";


-- 2. TABLE DE STAGING
-- Cette table reçoit les données brutes du CSV via Talend


DROP TABLE IF EXISTS "SalesAnalytics"."stg_ecommerce";

CREATE TABLE "SalesAnalytics"."stg_ecommerce" (

    staging_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    "InvoiceNo" VARCHAR(20),

    "StockCode" VARCHAR(30),

    "Description" TEXT,

    "Quantity" INTEGER,

    "InvoiceDate" TIMESTAMP,

    "UnitPrice" NUMERIC(12,4),

    "CustomerID" INTEGER,

    "Country" VARCHAR(100)

);


-- 3. DIMENSION CLIENT


DROP TABLE IF EXISTS "SalesAnalytics"."dim_customer";

CREATE TABLE "SalesAnalytics"."dim_customer" (

    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id INTEGER UNIQUE,

    customer_status VARCHAR(20) DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- 4. DIMENSION PRODUIT


DROP TABLE IF EXISTS "SalesAnalytics"."dim_product";

CREATE TABLE "SalesAnalytics"."dim_product" (

    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    stock_code VARCHAR(30) UNIQUE NOT NULL,

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- 5. DIMENSION PAYS


DROP TABLE IF EXISTS "SalesAnalytics"."dim_country";

CREATE TABLE "SalesAnalytics"."dim_country" (

    country_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    country_name VARCHAR(100) UNIQUE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- 6. DIMENSION DATE

DROP TABLE IF EXISTS "SalesAnalytics"."dim_date";

CREATE TABLE "SalesAnalytics"."dim_date" (

    date_key INTEGER PRIMARY KEY,

    full_date DATE UNIQUE NOT NULL,

    year INTEGER NOT NULL,

    quarter INTEGER NOT NULL,

    month INTEGER NOT NULL,

    month_name VARCHAR(20) NOT NULL,

    week INTEGER NOT NULL,

    day INTEGER NOT NULL,

    day_name VARCHAR(20) NOT NULL,

    is_weekend BOOLEAN NOT NULL

);


-- 7. TABLE DE FAITS
-- Grain = une ligne de transaction / ligne de facture


DROP TABLE IF EXISTS "SalesAnalytics"."fact_sales";

CREATE TABLE "SalesAnalytics"."fact_sales" (

    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    invoice_no VARCHAR(20) NOT NULL,

    product_key BIGINT NOT NULL,

    customer_key BIGINT,

    country_key BIGINT NOT NULL,

    date_key INTEGER NOT NULL,

    invoice_datetime TIMESTAMP NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(12,4) NOT NULL,

    revenue NUMERIC(14,4) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    
    -- CONTRAINTES


    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_key)
        REFERENCES "SalesAnalytics"."dim_product"(product_key),

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES "SalesAnalytics"."dim_customer"(customer_key),

    CONSTRAINT fk_sales_country
        FOREIGN KEY (country_key)
        REFERENCES "SalesAnalytics"."dim_country"(country_key),

    CONSTRAINT fk_sales_date
        FOREIGN KEY (date_key)
        REFERENCES "SalesAnalytics"."dim_date"(date_key),

    CONSTRAINT chk_quantity_positive
        CHECK (quantity > 0),

    CONSTRAINT chk_unit_price_positive
        CHECK (unit_price >= 0),

    CONSTRAINT chk_revenue_positive
        CHECK (revenue >= 0)

);



-- 8. INDEX
-- Optimisation pour Superset et les requêtes SQL


CREATE INDEX idx_fact_sales_invoice
ON "SalesAnalytics"."fact_sales"(invoice_no);


CREATE INDEX idx_fact_sales_date
ON "SalesAnalytics"."fact_sales"(date_key);


CREATE INDEX idx_fact_sales_product
ON "SalesAnalytics"."fact_sales"(product_key);


CREATE INDEX idx_fact_sales_customer
ON "SalesAnalytics"."fact_sales"(customer_key);


CREATE INDEX idx_fact_sales_country
ON "SalesAnalytics"."fact_sales"(country_key);


CREATE INDEX idx_fact_sales_datetime
ON "SalesAnalytics"."fact_sales"(invoice_datetime);


CREATE INDEX idx_product_stock
ON "SalesAnalytics"."dim_product"(stock_code);


CREATE INDEX idx_customer_id
ON "SalesAnalytics"."dim_customer"(customer_id);


CREATE INDEX idx_country_name
ON "SalesAnalytics"."dim_country"(country_name);



-- 9. VUE POUR SUPerset
-- Vue analytique principale


CREATE OR REPLACE VIEW "SalesAnalytics"."vw_sales_analytics" AS

SELECT

    f.sales_key,

    f.invoice_no,

    f.invoice_datetime,

    f.quantity,

    f.unit_price,

    f.revenue,

    p.stock_code,

    p.description AS product_description,

    c.customer_id,

    co.country_name,

    d.full_date,

    d.year,

    d.quarter,

    d.month,

    d.month_name,

    d.week,

    d.day,

    d.day_name,

    d.is_weekend

FROM "SalesAnalytics"."fact_sales" f

LEFT JOIN "SalesAnalytics"."dim_product" p
    ON f.product_key = p.product_key

LEFT JOIN "SalesAnalytics"."dim_customer" c
    ON f.customer_key = c.customer_key

LEFT JOIN "SalesAnalytics"."dim_country" co
    ON f.country_key = co.country_key

LEFT JOIN "SalesAnalytics"."dim_date" d
    ON f.date_key = d.date_key;