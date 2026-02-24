import matplotlib
matplotlib.use("Agg")
import pandas as pd

# Wczytanie danych
df = pd.read_csv("sales_raw.csv")

print(" Pierwsze 5 rekordów ")
print(df.head()) 
print(f"\nRozmiar ramki danych: {df.shape}") 
print(f"Typy danych:\n{df.dtypes}\n") 

#  Transformacje (ETL) 

# 1. Konwersja daty 
df["order_date"] = pd.to_datetime(df["order_date"], errors='coerce')

# 2. Tworzenie miary sprzedaży (total_value = quantity * unit_price) 
df["total_value"] = df["quantity"] * df["unit_price"]

# 3. Przygotowanie atrybutu  do agregacji 
df["year"] = df["order_date"].dt.year

print("--- Dane po transformacji ---")
print(df[["order_id", "total_value", "year"]].head())

# Agregacje (OLAP)

# Suma całkowita (miara globalna) 
total_sales = df["total_value"].sum()

# Sprzedaż per kraj (wymiar lokalizacji) 
sales_by_country = df.groupby("country")["total_value"].sum()

# Sprzedaż per rok (wymiar czasu) 
sales_by_year = df.groupby("year")["total_value"].sum()

print(f"\nCałkowita sprzedaż: {total_sales}")
print(f"\nSprzedaż według krajów:\n{sales_by_country}")
print(f"\nSprzedaż według lat:\n{sales_by_year}")

# Eksport danych analitycznych 

# Tworzenie nowej tabeli zagregowanej 
df_agg = df.groupby(["country", "year"])["total_value"].sum().reset_index()

# Zapis do pliku wynikowego 
df_agg.to_csv("sales_aggregated.csv", index=False)

print("\nSukces: Plik sales_aggregated.csv został wygenerowany.")