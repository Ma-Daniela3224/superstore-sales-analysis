import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from limpieza import (
    convertir_fechas,
    calcular_dias_envio,
    agregar_columnas_temporales,
)


def test_convertir_fechas():
    """Las fechas deben convertirse a tipo datetime."""
    df = pd.DataFrame({
        "Order Date": [
            "01/15/2017",
            "02/20/2018"
        ],
        "Ship Date": [
            "01/18/2017",
            "02/25/2018"
        ]
    })

    resultado = convertir_fechas(df)

    assert pd.api.types.is_datetime64_any_dtype(
        resultado["Order Date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        resultado["Ship Date"]
    )


def test_calcular_dias_envio():
    """Debe calcular correctamente la diferencia en dias entre Ship Date y Order Date."""
    df = pd.DataFrame({
        "Order Date": pd.to_datetime([
            "2017-01-01",
            "2017-02-01"
        ]),
        "Ship Date": pd.to_datetime([
            "2017-01-04",
            "2017-02-08"
        ])
    })

    resultado = calcular_dias_envio(df)

    assert resultado["Dias de envio"].tolist() == [3, 7]


def test_agregar_columnas_temporales():
    """Debe extraer correctamente Mes y Año de Order Date."""
    df = pd.DataFrame({
        "Order Date": pd.to_datetime([
            "2017-05-15",
            "2018-11-20"
        ])
    })

    resultado = agregar_columnas_temporales(df)

    assert resultado["Mes"].tolist() == [5, 11]

    assert resultado["Año"].tolist() == [2017, 2018]