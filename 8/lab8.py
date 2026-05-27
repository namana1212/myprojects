import pandas as pd
import time

# Wczytanie danych
df = pd.read_csv("Online_Retail_sample.csv", encoding="ISO-8859-1")

print("Liczba rekordów przed czyszczeniem:", len(df))

# Usunięcie brakujących CustomerID
df = df.dropna(subset=['CustomerID'])

# Usunięcie Quantity <= 0
df = df[df['Quantity'] > 0]

print("Liczba rekordów po czyszczeniu:", len(df))

# Utworzenie kolumny Total Price
df['Total Price'] = df['Quantity'] * df['UnitPrice']

# Konwersja daty
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Utworzenie kolumny Month
df['Month'] = df['InvoiceDate'].dt.to_period('M')

print("\nPrzygotowanie danych zakończone.\n")

def measure_time(function, description):

    start = time.perf_counter()

    result = function()

    end = time.perf_counter()

    execution_time = end - start

    print(f"{description}: {execution_time:.6f} sekundy")

    return result, execution_time

print("===================================")
print("ETAP 2 — AGREGACJE")
print("===================================\n")


print("1. SPRZEDAŻ WG KRAJU\n")


# groupby()
def sales_country_groupby():
    return df.groupby('Country')['Total Price'].sum()


result1, time1 = measure_time(
    sales_country_groupby,
    "groupby()"
)

print(result1.head(), "\n")


# pivot_table()
def sales_country_pivot():
    return pd.pivot_table(
        df,
        values='Total Price',
        index='Country',
        aggfunc='sum'
    )


result2, time2 = measure_time(
    sales_country_pivot,
    "pivot_table()"
)

print(result2.head(), "\n")


# set_index()
def sales_country_setindex():

    df2 = df.set_index('Country')

    return df2.groupby(level=0)['Total Price'].sum()


result3, time3 = measure_time(
    sales_country_setindex,
    "set_index()"
)

print(result3.head(), "\n")


print("2. SPRZEDAŻ WG MIESIĄCA\n")


# groupby()
def sales_month_groupby():
    return df.groupby('Month')['Total Price'].sum()


result4, time4 = measure_time(
    sales_month_groupby,
    "groupby()"
)

print(result4.head(), "\n")


# pivot_table()
def sales_month_pivot():
    return pd.pivot_table(
        df,
        values='Total Price',
        index='Month',
        aggfunc='sum'
    )


result5, time5 = measure_time(
    sales_month_pivot,
    "pivot_table()"
)

print(result5.head(), "\n")


# set_index()
def sales_month_setindex():

    df2 = df.set_index('Month')

    return df2.groupby(level=0)['Total Price'].sum()


result6, time6 = measure_time(
    sales_month_setindex,
    "set_index()"
)

print(result6.head(), "\n")


print("3. LICZBA TRANSAKCJI WG KLIENTA\n")


# groupby()
def transactions_customer_groupby():
    return df.groupby('CustomerID')['InvoiceNo'].count()


result7, time7 = measure_time(
    transactions_customer_groupby,
    "groupby()"
)

print(result7.head(), "\n")


# pivot_table()
def transactions_customer_pivot():
    return pd.pivot_table(
        df,
        values='InvoiceNo',
        index='CustomerID',
        aggfunc='count'
    )


result8, time8 = measure_time(
    transactions_customer_pivot,
    "pivot_table()"
)

print(result8.head(), "\n")


# set_index()
def transactions_customer_setindex():

    df2 = df.set_index('CustomerID')

    return df2.groupby(level=0)['InvoiceNo'].count()


result9, time9 = measure_time(
    transactions_customer_setindex,
    "set_index()"
)

print(result9.head(), "\n")

print("===================================")
print("ETAP 3 — DUŻA HURTOWNIA")
print("===================================\n")


# Powiększenie danych
large_df = pd.concat([df] * 10, ignore_index=True)

print("Liczba rekordów po powiększeniu:", len(large_df))
print()


print("SPRZEDAŻ WG KRAJU — DUŻY ZBIÓR\n")


# groupby()
def large_groupby():
    return large_df.groupby('Country')['Total Price'].sum()


_, lg1 = measure_time(
    large_groupby,
    "groupby()"
)


# pivot_table()
def large_pivot():
    return pd.pivot_table(
        large_df,
        values='Total Price',
        index='Country',
        aggfunc='sum'
    )


_, lg2 = measure_time(
    large_pivot,
    "pivot_table()"
)


# set_index()
def large_setindex():

    df2 = large_df.set_index('Country')

    return df2.groupby(level=0)['Total Price'].sum()


_, lg3 = measure_time(
    large_setindex,
    "set_index()"
)

print("\n===================================")
print("ETAP 4 — RAPORT")
print("===================================\n")

times = {
    "groupby()": lg1,
    "pivot_table()": lg2,
    "set_index()": lg3
}

fastest = min(times, key=times.get)

print(f"Najszybsza metoda: {fastest}")

print("\nNajbardziej czytelna metoda:")
print("groupby() — ponieważ jest najprostsza i najbardziej intuicyjna.")

print("\nProblemy przy bardzo dużych hurtowniach danych:")
print("- duże zużycie pamięci RAM")
print("- wolniejsze operacje agregacji")
print("- długi czas przetwarzania")
print("- możliwe problemy z optymalizacją indeksów")
print("- konieczność stosowania technologii Big Data")