-- E-COMMERCE SALES ANALYTICS
-- Database : superset_bi
-- Schema   : SalesAnalytics


-- 1. CREATION DU SCHEMA

CREATE SCHEMA IF NOT EXISTS "SalesAnalytics";


-- 2. TABLE DE STAGING
-- Cette table reçoit les données brutes du CSV via Talend


DROP TABLE IF EXISTS "SalesAnalytics"."salesanalytics";

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
