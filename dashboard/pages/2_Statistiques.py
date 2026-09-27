import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_assets, get_stats

st.set_page_config(page_title="Statistiques", page_icon="📊", layout="wide")

st.title("📊 Statistiques des actifs")

assets = get_assets()
symbols = [a["symbol"] for a in assets]

symbol = st.selectbox("Choisir un actif", symbols)

stats = get_stats(symbol)

if stats is None:
    st.warning(f"Aucune statistique disponible pour {symbol}")
else:
    st.subheader(f"Statistiques de {stats['symbol']} - {stats['name']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nombre d'observations", stats["nb_observations"])
    with col2:
        st.metric("Periode", f"{stats['date_min']} -> {stats['date_max']}")
    with col3:
        st.metric("Volume total", f"{stats['volume_total']:,}")

    st.subheader("Prix")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prix moyen", f"{stats['prix_moyen']:.2f} USD")
    with col2:
        st.metric("Prix maximum", f"{stats['prix_max']:.2f} USD")
    with col3:
        st.metric("Prix minimum", f"{stats['prix_min']:.2f} USD")
