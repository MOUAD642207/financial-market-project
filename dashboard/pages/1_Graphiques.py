import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_assets, get_prices

st.set_page_config(page_title="Graphiques", page_icon="chart", layout="wide")

st.title("Graphiques des cours")

assets = get_assets()
symbols = [a["symbol"] for a in assets]

col1, col2 = st.columns([1, 3])

with col1:
    symbol = st.selectbox("Actif", symbols)
    limit = st.slider("Nombre de jours", 10, 1000, 100)

with col2:
    prices = get_prices(symbol, limit=limit)

    if not prices:
        st.warning("Aucune donnee disponible")
    else:
        df = pd.DataFrame(prices)
        df["observation_timestamp"] = pd.to_datetime(df["observation_timestamp"], utc=True)
        df = df.sort_values("observation_timestamp")

        fig = go.Figure(data=[go.Candlestick(
            x=df["observation_timestamp"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name=symbol,
        )])

        fig.update_layout(
            title=f"{symbol} - Chandeliers japonais",
            xaxis_title="Date",
            yaxis_title="Prix (USD)",
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df["observation_timestamp"],
            y=df["close"],
            mode="lines",
            name="Close",
            line=dict(color="blue", width=2),
        ))
        fig2.update_layout(
            title=f"{symbol} - Evolution du cours",
            xaxis_title="Date",
            yaxis_title="Prix (USD)",
            height=400,
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Volume")
        fig3 = go.Figure(data=[go.Bar(
            x=df["observation_timestamp"],
            y=df["volume"],
            name="Volume",
            marker_color="orange",
        )])
        fig3.update_layout(height=300, xaxis_title="Date", yaxis_title="Volume")
        st.plotly_chart(fig3, use_container_width=True)
