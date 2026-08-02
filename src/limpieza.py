"""
Modulo de procesamiento para el dataset Superstore Sales.
"""

import pandas as pd


def cargar_datos(ruta_csv):
    """Carga el CSV original."""
    return pd.read_csv(ruta_csv, encoding='ISO-8859-1')


def convertir_fechas(df):
    """Convierte Order Date y Ship Date a tipo datetime."""
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y', errors='coerce')
    return df


def calcular_dias_envio(df):
    """Agrega la columna 'Dias de envio' = Ship Date - Order Date."""
    df['Dias de envio'] = (df['Ship Date'] - df['Order Date']).dt.days
    return df


def agregar_columnas_temporales(df):
    """Agrega columnas de Mes y Año extraidas de Order Date."""
    df['Mes'] = df['Order Date'].dt.month
    df['Año'] = df['Order Date'].dt.year
    return df


def procesar_dataset(ruta_csv):
    """
    Ejecuta el flujo completo de procesamiento.
    """
    df = cargar_datos(ruta_csv)
    df = convertir_fechas(df)
    df = calcular_dias_envio(df)
    df = agregar_columnas_temporales(df)
    return df


if __name__ == '__main__':
    df_procesado = procesar_dataset('data/Sample_Superstore.csv')
    df_procesado.to_csv('data/superstore_procesado.csv', index=False)
    print(f'Dataset procesado guardado: {df_procesado.shape[0]} filas, {df_procesado.shape[1]} columnas')
