import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Indicateurs", page_icon="chart", layout="wide")

st.title("Indicateurs techniques")

try:
    assets = requests.get(f"{API_URL}/assets/").json()
    symbols = [a["symbol"] for a in assets]
except Exception as e:
    st.error(f"Erreur API : {e}")
    st.stop()

col1, col2 = st.columns([1, 3])

with col1:
    symbol = st.selectbox("Actif", symbols)
    limit = st.slider("Nombre de jours", 50, 1000, 300)

try:
    response = requests.get(f"{API_URL}/indicators/{symbol}", params={"limit": limit})
    response.raise_for_status()
    result = response.json()
except Exception as e:
    st.error(f"Erreur : {e}")
    st.stop()

df = pd.DataFrame(result["data"])
df["observation_timestamp"] = pd.to_datetime(df["observation_timestamp"], utc=True)
df = df.sort_values("observation_timestamp")

st.subheader(f"{result['symbol']} - {result['name']}")

# Graphique 1 : Prix + Moyennes mobiles + Bollinger
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["close"], name="Close", line=dict(color="black", width=2)))
fig.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["ma20"], name="MA20", line=dict(color="blue", width=1)))
fig.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["ma50"], name="MA50", line=dict(color="orange", width=1)))
fig.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["ma200"], name="MA200", line=dict(color="red", width=1)))
fig.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["bb_upper"], name="BB Upper", line=dict(color="gray", width=1, dash="dash")))
fig.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["bb_lower"], name="BB Lower", line=dict(color="gray", width=1, dash="dash"), fill="tonexty", fillcolor="rgba(128,128,128,0.1)"))
fig.update_layout(title="Prix + Moyennes mobiles + Bandes de Bollinger", height=500, xaxis_title="Date", yaxis_title="Prix (USD)")
st.plotly_chart(fig, use_container_width=True)

# Graphique 2 : RSI
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["rsi"], name="RSI", line=dict(color="purple", width=2)))
fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sur-achat (70)")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sur-vente (30)")
fig_rsi.update_layout(title="RSI (14)", height=300, xaxis_title="Date", yaxis_title="RSI", yaxis_range=[0, 100])
st.plotly_chart(fig_rsi, use_container_width=True)

# Graphique 3 : MACD
fig_macd = go.Figure()
fig_macd.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["macd"], name="MACD", line=dict(color="blue", width=2)))
fig_macd.add_trace(go.Scatter(x=df["observation_timestamp"], y=df["macd_signal"], name="Signal", line=dict(color="orange", width=2)))
fig_macd.add_trace(go.Bar(x=df["observation_timestamp"], y=df["macd_hist"], name="Histogramme", marker_color="gray"))
fig_macd.update_layout(title="MACD", height=300, xaxis_title="Date", yaxis_title="MACD")
st.plotly_chart(fig_macd, use_container_width=True)

# Metriques
st.subheader("Dernieres valeurs")
last = df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Close", f"{last['close']:.2f} USD")
with col2:
    st.metric("RSI", f"{last['rsi']:.2f}" if last['rsi'] else "N/A")
with col3:
    st.metric("MACD", f"{last['macd']:.2f}" if last['macd'] else "N/A")
with col4:
    vol = last['volatility']
    st.metric("Volatilite", f"{vol:.4f}" if vol else "N/A")
