import pandas as pd
import time

print("ETAP 1 — Wczytanie i analiza danych")

start = time.time()

df = pd.read_csv("Online_Retail_sample.csv", encoding="ISO-8859-1")

end = time.time()

print(f"Czas wczytywania danych: {end - start:.4f} s")

print("\nLiczba rekordów:")
print(df.shape[0])

print("\nBrakujące wartości:")
print(df.isnull().sum())

print("\nTypy danych:")
print(df.dtypes)

print("\nZużycie pamięci przed optymalizacją:")
memory_before = df.memory_usage(deep=True).sum() / 1024**2
print(f"{memory_before:.2f} MB")


# Kopia danych przed optymalizacją
df_before = df.copy()

print("\nETAP 2 — Optymalizacja pamięci")

# Zamiana kolumn tekstowych na category
category_columns = ["Country", "CustomerID", "StockCode"]

for col in category_columns:
    if col in df.columns:
        df[col] = df[col].astype("category")

# Downcasting typów liczbowych
for col in df.select_dtypes(include=["int64"]).columns:
    df[col] = pd.to_numeric(df[col], downcast="integer")

for col in df.select_dtypes(include=["float64"]).columns:
    df[col] = pd.to_numeric(df[col], downcast="float")

print("\nTypy danych po optymalizacji:")
print(df.dtypes)

print("\nZużycie pamięci po optymalizacji:")
memory_after = df.memory_usage(deep=True).sum() / 1024**2
print(f"{memory_after:.2f} MB")

reduction = ((memory_before - memory_after) / memory_before) * 100

print(f"\nZmniejszenie pamięci: {reduction:.2f}%")

# Dodanie wartości sprzedaży
df_before["Sales"] = df_before["Quantity"] * df_before["UnitPrice"]
df["Sales"] = df["Quantity"] * df["UnitPrice"]


print("\nETAP 3 — Analiza wydajności operacji")


def measure_time(operation_name, func):
    start = time.time()
    result = func()
    end = time.time()

    execution_time = end - start

    print(f"{operation_name}: {execution_time:.6f} s")

    return result


print("\n--- PRZED OPTYMALIZACJĄ ---")

# Grupowanie — suma sprzedaży wg kraju
measure_time(
    "Suma sprzedaży wg kraju",
    lambda: df_before.groupby("Country")["Sales"].sum()
)

# Grupowanie — suma sprzedaży wg miesiąca
df_before["InvoiceDate"] = pd.to_datetime(df_before["InvoiceDate"])

measure_time(
    "Suma sprzedaży wg miesiąca",
    lambda: df_before.groupby(df_before["InvoiceDate"].dt.month)["Sales"].sum()
)

# TOP 10 klientów
measure_time(
    "TOP 10 klientów",
    lambda: df_before.groupby("CustomerID")["Sales"].sum().sort_values(ascending=False).head(10)
)

# Produkty sprzedane w Wielkiej Brytanii
measure_time(
    "Produkty sprzedane w UK",
    lambda: df_before[df_before["Country"] == "United Kingdom"]
)

# Rekordy sprzedaży > 1000
measure_time(
    "Sprzedaż > 1000",
    lambda: df_before[df_before["Sales"] > 1000]
)


print("\n--- PO OPTYMALIZACJI ---")

# Grupowanie — suma sprzedaży wg kraju
measure_time(
    "Suma sprzedaży wg kraju",
    lambda: df.groupby("Country")["Sales"].sum()
)

# Grupowanie — suma sprzedaży wg miesiąca
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

measure_time(
    "Suma sprzedaży wg miesiąca",
    lambda: df.groupby(df["InvoiceDate"].dt.month)["Sales"].sum()
)

# TOP 10 klientów
measure_time(
    "TOP 10 klientów",
    lambda: df.groupby("CustomerID")["Sales"].sum().sort_values(ascending=False).head(10)
)

# Produkty sprzedane w UK
measure_time(
    "Produkty sprzedane w UK",
    lambda: df[df["Country"] == "United Kingdom"]
)

# Rekordy sprzedaży > 1000
measure_time(
    "Sprzedaż > 1000",
    lambda: df[df["Sales"] > 1000]
)

print("\nETAP 4 — WNIOSKI")

print("""
1. Po optymalizacji zmniejszyło się zużycie pamięci DataFrame.

2. Operacje grupowania i filtrowania zwykle wykonywały się szybciej
   dzięki użyciu typu category oraz mniejszych typów liczbowych.

3. Największy wpływ na wydajność miała zmiana kolumn tekstowych
   na category.

4. Zmniejszenie pamięci nie zawsze oznacza znaczny wzrost wydajności,
   ale przy dużych zbiorach danych często poprawia szybkość operacji.
""")