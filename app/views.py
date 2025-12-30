from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.offline import plot

def index(request):
    # Download ETF data
    data_etf = yf.download(
        # passes the ticker
        tickers=['SPY', 'QQQ', 'DIA', 'IWM', 'VTI', 'VXX',                                    # <- US ETFs
                'FEZ', 'IEUR', 'EWG', 'EWQ', 'EWU', 'EWL',                                    # <- European ETFs
                'EWJ', 'MCHI', 'FXI', 'INDA', 'EEMA', 'AAXJ',                                 # <- Asian ETFs
                'BTC-USD', 'XRP-USD', 'USDT-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD',            # <- Crypto Currencies
                'TLT', 'IEF', 'SHY', 'LQD', 'HYG', 'TIP',                                     # <- Rates/Fixed Income ETFs
                'USO', 'GLD', 'DBA', 'UNG', 'SLV', 'CORN',                                    # <- Commodity ETFs               
                'EURUSD=X', 'JPY=X', 'GBP=X', 'AUD=X', 'CAD=X', 'MXN=X'],                     # <- Forex ETFs
        group_by = 'ticker',
        threads=True, # Set thread value to true
        # used for access data[ticker]
        period='1d', 
        interval='1m' 
    )

    def make_candle_chart(df, ticker):
        if df.empty:
            return None

        fig = go.Figure(
            data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=ticker
            )]
        )

        fig.update_layout(
            paper_bgcolor="#14151b",
            plot_bgcolor="#14151b",
            font_color="white",
            xaxis_rangeslider_visible=False,
            height=250,
            margin=dict(l=5, r=5, t=20, b=5)
        )
        return plot(fig, auto_open=False, output_type='div')

    ETF_REGIONS = {
        "US": ['SPY','QQQ','DIA','IWM','VTI','VXX'],
        "EUROPE": ['FEZ','IEUR','EWG','EWQ','EWU','EWL'],
        "ASIA": ['EWJ','MCHI','FXI','INDA','EEMA','AAXJ'],
        "CRYPTO": ['BTC-USD','XRP-USD','USDT-USD','ETH-USD','BNB-USD','SOL-USD'],
        "RATES_FIXED_INCOME": ['TLT','IEF','SHY','LQD','HYG','TIP'],
        "COMMODITIES": ['USO','GLD','DBA','UNG','SLV','CORN'],
        "FOREX": ['EURUSD=X', 'JPY=X', 'GBP=X', 'AUD=X', 'CAD=X', 'MXN=X']
    }

    plots = {}

    for region, tickers in ETF_REGIONS.items():
        plots[region] = {}
        for ticker in tickers:
            df = data_etf[ticker].dropna()
            plots[region][ticker] = make_candle_chart(df, ticker)

    return render(request, 'index.html', {
        'plots': plots
    })


