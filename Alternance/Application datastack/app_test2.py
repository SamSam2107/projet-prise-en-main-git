import streamlit as st
import pandas as pd
import requests

# Charger Bootstrap
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
""", unsafe_allow_html=True)

# Configuration de Streamlit
st.set_page_config(page_title="DataStack - Data Engineering", layout="wide")

# === Navbar HTML ===
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
          <a class="nav-link" href="?tab=home">🏠 Accueil</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="?tab=load">📂 Chargement des Données</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="?tab=etl">⚙️ ETL</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="?tab=analyze">📊 Analyse</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
""", unsafe_allow_html=True)

# === Gestion des Onglets ===
query_params = st.experimental_get_query_params()
tab = query_params.get("tab", ["home"])[0]  # Déterminer l'onglet actif, par défaut "home"

# === Contenu Dynamique Basé sur l'Onglet Actif ===
if tab == "home":
    st.title("🏠 Accueil")
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

elif tab == "load":
    st.title("📂 Chargement des Données")

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
        api_url = st.text_input("URL de l'API")
        token = st.text_input("Token de l'API", type="password")
        params = st.text_area("Paramètres (JSON)", '{"param1": "value1", "param2": "value2"}')
        if st.button("Charger depuis l'API"):
            try:
                headers = {"Authorization": f"Bearer {token}"}
                params = eval(params)
                response = requests.get(api_url, headers=headers, params=params)
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
        db_connection = st.text_input("Chaîne de connexion (SQLAlchemy)")
        db_query = st.text_area("Requête SQL", "SELECT * FROM your_table")
        if st.button("Charger depuis la base de données"):
            from sqlalchemy import create_engine
            try:
                engine = create_engine(db_connection)
                with engine.connect() as conn:
                    data = pd.read_sql(db_query, conn)
                st.success("Données chargées avec succès.")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"Erreur de connexion à la base de données : {e}")

elif tab == "etl":
    st.title("⚙️ Pipeline ETL")
    st.write("Ajoutez ici votre processus d'extraction, transformation et chargement.")

elif tab == "analyze":
    st.title("📊 Analyse des Données")
    st.write("Ajoutez ici vos visualisations ou analyses des données.")

st.sidebar.info("Application évolutive - Ajoutez vos propres modules pour enrichir cette plateforme.")
