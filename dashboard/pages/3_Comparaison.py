import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_assets, get_prices

st.set_page_config(page_title="Comparaison", page_icon="search", layout="wide")

st.title("Comparaison d'actifs")

assets = get_assets()
symbols = [a["symbol"] for a in assets]

selected = st.multiselect(
    "Selectionnez 2 a 5 actifs",
    options=symbols,
    default=symbols[:2] if len(symbols) >= 2 else symbols,
)

limit = st.slider("Nombre de jours", 10, 1000, 100)

if len(selected) < 2:
    st.info("Selectionnez au moins 2 actifs pour comparer")
elif len(selected) > 5:
    st.warning("Maximum 5 actifs")
else:
    fig = go.Figure()

    for symbol in selected:
        prices = get_prices(symbol, limit=limit)
        if not prices:
            continue

        df = pd.DataFrame(prices)
        df["observation_timestamp"] = pd.to_datetime(df["observation_timestamp"], utc=True)
        df = df.sort_values("observation_timestamp")

        first_close = df["close"].iloc[0]
        df["normalized"] = (df["close"] / first_close) * 100

        fig.add_trace(go.Scatter(
            x=df["observation_timestamp"],
            y=df["normalized"],
            mode="lines",
            name=symbol,
        ))

    fig.update_layout(
        title="Comparaison (base 100 = premier jour)",
        xaxis_title="Date",
        yaxis_title="Valeur normalisee",
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)
