import pandas as pd


df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

print("=== PODGLĄD DANYCH ===")
print(df.head())

print("\n=== WYMIARY ===")
print(df.shape)

print("\n=== KOLUMNY ===")
print(df.columns)


# ZADANIE ENCJE 


# Customer (CustomerID, Country)
# Product (StockCode, Description, UnitPrice)
# Invoice (InvoiceNo, InvoiceDate)
# Country (Country)

# ZADANIE MODEL 3NF

# tabela klientów

dim_customer = df[["CustomerID", "Country"]].drop_duplicates()

# tabela produktów

dim_product = df[["StockCode", "Description", "UnitPrice"]].drop_duplicates()

# tabela faktur

dim_invoice = df[["InvoiceNo", "InvoiceDate", "CustomerID"]].drop_duplicates()

# tabela krajów

dim_country = df[["Country"]].drop_duplicates()

# tabela faktów (sprzedaż)

fact_sales = df[["InvoiceNo", "StockCode", "Quantity"]]

# ZAPIS DO PLIKÓW CSV

dim_customer.to_csv("dim_customer.csv", index=False)
dim_product.to_csv("dim_product.csv", index=False)
dim_invoice.to_csv("dim_invoice.csv", index=False)
dim_country.to_csv("dim_country.csv", index=False)
fact_sales.to_csv("fact_sales.csv", index=False)

# ZADANIE ODPOWIEDŹ

# Model 3NF nie jest wygodny do OLAP, ponieważ:

# - dane są rozbite na wiele tabel
# - trzeba wykonywać dużo JOINów
# - analizy ą wolniejsze
# - trudniej robić agregacje

# Wymaga wielu joinów np.:

# fact_sales + dim_invoice + dim_customer + dim_product
print("\n=== GOTOWE ===")
print("Utworzono pliki:")
print("dim_customer.csv")
print("dim_product.csv")
print("dim_invoice.csv")
print("dim_country.csv")
print("fact_sales.csv")
