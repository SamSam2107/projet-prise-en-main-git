import streamlit as st
from streamlit.logger import get_logger

import pandas as pd
import requests

LOGGER = get_logger(__name__)



# Charger Bootstrap
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
""", unsafe_allow_html=True)

# Navbar HTML
st.markdown("""
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">DataStack</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" href="#tab1">🏠 Accueil</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#tab2">📂 Chargement des Données</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#tab3">⚙️ ETL</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#tab4">📊 Analyse</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
""", unsafe_allow_html=True)

# Gestion des onglets avec Streamlit
st.sidebar.header("Navigation")
tab = st.sidebar.selectbox(
    "Choisissez un onglet",
    options=["🏠 Accueil", "📂 Chargement des Données", "⚙️ ETL", "📊 Analyse"]
)

# === Contenu des Onglets ===
if tab == "🏠 Accueil":
    st.markdown("""
    <div class="container mt-4">
        <h1 class="display-4 text-center">Bienvenue sur DataStack</h1>
        <p class="lead text-center">
            Une plateforme intuitive pour charger, nettoyer et analyser vos données.
        </p>
        <hr>
        <p class="text-center">Utilisez les options du menu pour explorer les fonctionnalités.</p>
    </div>
    """, unsafe_allow_html=True)

elif tab == "📂 Chargement des Données":
    st.header("📂 Chargement des Données")

    # Sélection de la source
    source_type = st.radio(
        "Choisissez la source de données",
        options=["Fichier local", "Base de données", "API"]
    )

    # Chargement depuis un fichier local
    if source_type == "Fichier local":
        uploaded_file = st.file_uploader("Téléversez votre fichier", type=["csv", "xlsx"])
        delimiter = st.text_input("Délimiteur (par défaut : ';')", value=";")
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    data = pd.read_csv(uploaded_file, delimiter=delimiter)
                elif uploaded_file.name.endswith(".xlsx"):
                    data = pd.read_excel(uploaded_file)
                st.success("Données chargées avec succès.")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier : {e}")

    # Chargement depuis une API
    elif source_type == "API":
        st.text_input("URL de l'API", key="api_url")
        st.text_input("Token API", key="api_token", type="password")
        st.text_area("Paramètres (JSON)", '{"param1": "value1", "param2": "value2"}', key="api_params")
        if st.button("Charger depuis l'API"):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.api_token}"}
                params = eval(st.session_state.api_params)
                response = requests.get(st.session_state.api_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, dict):
                    data = pd.DataFrame(data['data']) if 'data' in data else pd.DataFrame([data])
                elif isinstance(data, list):
                    data = pd.DataFrame(data)
                st.success("Données chargées avec succès.")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"Erreur lors de la connexion à l'API : {e}")

    # Chargement depuis une base de données
    elif source_type == "Base de données":
        st.text_input("Chaîne de connexion (SQLAlchemy)", key="db_connection")
        st.text_area("Requête SQL", "SELECT * FROM your_table", key="db_query")
        if st.button("Charger depuis la base de données"):
            from sqlalchemy import create_engine
            try:
                engine = create_engine(st.session_state.db_connection)
                with engine.connect() as conn:
                    data = pd.read_sql(st.session_state.db_query, conn)
                st.success("Données chargées avec succès.")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"Erreur de connexion à la base de données : {e}")

elif tab == "⚙️ ETL":
    st.header("⚙️ Pipeline ETL")
    st.write("Ajoutez ici votre processus d'extraction, transformation et chargement.")

elif tab == "📊 Analyse":
    st.header("📊 Analyse des Données")
    st.write("Ajoutez ici vos visualisations ou analyses des données.")

st.sidebar.info("Application évolutive - Ajoutez vos propres modules pour enrichir cette plateforme.")



if __name__ == "__main__":
    run()

