import streamlit as st
from api_client import check_health, get_assets

st.set_page_config(
    page_title="Financial Market Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Financial Market Dashboard")
st.markdown("Bienvenue sur le dashboard de donnees boursieres")

st.sidebar.header("Navigation")
st.sidebar.info("Utilisez le menu ci-dessus pour naviguer entre les pages")

st.header("Etat du systeme")

health = check_health()

col1, col2 = st.columns(2)

with col1:
    if health.get("status") == "ok":
        st.success("API : operationnelle")
    else:
        st.error("API : non accessible")

with col2:
    if health.get("database") == "connected":
        st.success("Base de donnees : connectee")
    else:
        st.error(f"Base de donnees : {health.get('database', 'inconnue')}")

st.header("Actifs disponibles")

try:
    assets = get_assets()
    st.dataframe(assets, use_container_width=True)
    st.metric("Nombre d'actifs", len(assets))
except Exception as e:
    st.error(f"Erreur lors du chargement des actifs : {e}")
