import krakenex  # conectar al servidor de kraken
from pykrakenapi import KrakenAPI  # conectar a la base de datos
import time  # tiempo para parar el codigo
import plotly.graph_objects as go
import ta


def cotizacion(moneda):  # DESCARGAR COLUMNA NOMBRE DE VARIABLES y decir por que las escogimos
    # ohlc DataFrame
    try:
        api = krakenex.API()
        k = KrakenAPI(api)

        df, last = k.get_ohlc_data(moneda,
                                   interval=1440)  # 60 min *24  horas. last es el ultimo valor de la columna time
        df = df.reset_index()
        df = indicadores(df)
        df['name'] = moneda
        time.sleep(.9)  # api pide esperar 0.8 seconds

        return df
    except Exception as e:
        print(e)


def indicadores(df):
    try:
        # Calculando la media móvil:
        df['MA5'] = df.close.rolling(5).mean()
        df['MA20'] = df.close.rolling(20).mean()

        # Cálculo de RSI
        df["rsi"] = ta.momentum.rsi(df["close"], window=14, fillna=False)
        return df
    except Exception as e:
        print(e)


def algoritmo(df1, df2, df3):
    try:

        coins = [cotizacion(df1), cotizacion(df2), cotizacion(df3)]
        fig = go.Figure()
        for coin in coins:
            name = coin['name'][0]
            fig.add_trace(
                go.Candlestick(x=coin['dtime'],
                               # Funcion que permite ver grafico de vela a partir del HIGH, LOW, OPEN y CLOSE
                               open=coin['open'],
                               high=coin['high'],
                               low=coin['low'],
                               close=coin['close'],
                               name=name)  # name para que aparezca en la leyenda el nombre de la moneda
            )
            fig.add_trace(
                go.Scatter(x=coin['dtime'],  # FUNCION QUE GRAFICA DE FORMA CONTINUA LOS VALORES DE LA MEDIA
                           y=coin['MA5'],
                           line=dict(color='orange', width=1), name=f"MA5({name})"))
            fig.add_trace(
                go.Scatter(x=coin['dtime'],  # FUNCION QUE GRAFICA DE FORMA CONTINUA LOS VALORES DE LA MEDIA
                           y=coin['MA20'],
                           line=dict(color='green', width=1), name=f"MA20({name})"))
            fig.add_trace(
                go.Scatter(x=coin["dtime"],  # FUNCION QUE GRAFICA DE FORMA CONTINUA LOS VALORES DE RDI
                           y=coin["rsi"],
                           mode="markers+lines", name=f"RSI({name})"))

        fig.update_layout(  # FUNCION PARA EDITAR LA VISTA DE LOS GRAFICOS
            updatemenus=[go.layout.Updatemenu(
                active=0,
                buttons=list(
                    [dict(label='All',
                          method='update',
                          args=[{'visible': [True, True, True]},
                                {'title': 'All',
                                 'showlegend': True}]),
                     dict(label='BCHUSD',
                          method='update',
                          args=[
                              {'visible': [True, True, True, True, False, False, False, False, False, False, False, False]},
                              # the index of True aligns with the indices of plot traces
                              {'title': 'ZRXUSD',
                               'showlegend': True}]),
                     dict(label='ZRXUSD',
                          method='update',
                          args=[
                              {'visible': [False, False, False, False, True, True, True, True, False, False, False, False]},
                              {'title': 'BCHUSD',
                               'showlegend': True}]),
                     dict(label='XZECZUSD',
                          method='update',
                          args=[
                              {'visible': [False, False, False, False, False, False, False, False, True, True, True, True]},
                              {'title': 'XZECZUSD',
                               'showlegend': True}]),
                     ])
            )
            ])

        fig.show()
    except Exception as e:
        print(e)


algoritmo("BCHUSD", "ZRXUSD", "XZECZUSD")
