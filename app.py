import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from db_sqlite import Database
from db_mongo import MongoDatabase
from geoprocessamento import calcular_distancia, locais_proximos

db_sqlite = Database("database.db")
db_mongo = MongoDatabase(db_name="meu_banco_mongo")

db_sqlite.create_table("cidades", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "nome": "TEXT NOT NULL",
    "estado": "TEXT NOT NULL"
})

st.set_page_config(page_title="Persistência Poliglota com Geo", layout="wide")
st.title("🌍 Projeto de Persistência Poliglota e Geo-Processamento")


menu = st.sidebar.radio("Menu", ["Cadastrar Cidade", "Cadastrar Local", "Consultar Locais", "Proximidade"])

if menu == "Cadastrar Cidade":
    st.subheader("Cadastrar nova cidade")

    nome = st.text_input("Nome da cidade")
    estado = st.text_input("Estado")

    if st.button("Salvar cidade"):
        if nome and estado:
            db_sqlite.insert_data("cidades", {"nome": nome, "estado": estado})
            st.success(f"Cidade {nome}/{estado} cadastrada com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

    st.subheader("Cidades cadastradas")
    cidades = db_sqlite.fetch_data("cidades")
    if cidades:
        df_cidades = pd.DataFrame(cidades, columns=["id", "nome", "estado"])
        st.dataframe(df_cidades)

elif menu == "Cadastrar Local":
    st.subheader("Cadastrar novo local de interesse")

    cidades = db_sqlite.fetch_data("cidades")
    if not cidades:
        st.warning("Cadastre uma cidade antes de registrar locais.")
    else:
        nome_local = st.text_input("Nome do local")
        cidade = st.selectbox("Cidade", [c[1] for c in cidades])
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
        descricao = st.text_area("Descrição")

        if st.button("Salvar local"):
            if nome_local and cidade and descricao and latitude != 0.0 and longitude != 0.0:
                doc = {
                    "nome_local": nome_local,
                    "cidade": cidade,
                    "coordenadas": {"latitude": latitude, "longitude": longitude},
                    "descricao": descricao
                }
                db_mongo.insert_document("locais", doc)
                st.success(f"Local {nome_local} cadastrado em {cidade}!")
            else:
                st.warning("Preencha todos os campos antes de salvar.")


elif menu == "Consultar Locais":
    st.subheader("Locais por cidade")

    cidades = db_sqlite.fetch_data("cidades")
    if not cidades:
        st.warning("Cadastre cidades para habilitar esta função.")
    else:
        cidade_sel = st.selectbox("Selecione uma cidade", [c[1] for c in cidades])
        locais = db_mongo.find_documents("locais", {"cidade": cidade_sel})

        if locais:
            df = pd.DataFrame(locais)
            st.dataframe(df[["nome_local", "cidade", "descricao"]])

            try:
                lat_ref = df['coordenadas'][0]['latitude']
                lon_ref = df['coordenadas'][0]['longitude']
                mapa = folium.Map(location=[lat_ref, lon_ref], zoom_start=12)

                for _, row in df.iterrows():
                    try:
                        folium.Marker(
                            location=[row['coordenadas']['latitude'], row['coordenadas']['longitude']],
                            popup=row['nome_local']
                        ).add_to(mapa)
                    except Exception:
                        continue

                st_folium(mapa, width=700, height=500)
            except Exception:
                st.warning("Não foi possível exibir o mapa. Verifique as coordenadas cadastradas.")
        else:
            st.info("Nenhum local encontrado para esta cidade.")


elif menu == "Proximidade":
    st.subheader("Buscar locais próximos")

    lat = st.number_input("Latitude de referência", format="%.6f")
    lon = st.number_input("Longitude de referência", format="%.6f")
    raio = st.slider("Raio em km", 1, 50, 10)

    if st.button("Buscar"):
        locais = db_mongo.find_documents("locais")
        proximos = locais_proximos(lat, lon, raio, locais)

        if proximos:
            df = pd.DataFrame(proximos)
            st.dataframe(df[["nome_local", "cidade", "descricao", "distancia_km"]])

            # Mapa
            mapa = folium.Map(location=[lat, lon], zoom_start=12)
            folium.Marker(location=[lat, lon], popup="Ponto de referência", icon=folium.Icon(color="red")).add_to(mapa)

            for _, row in df.iterrows():
                folium.Marker(
                    location=[row['coordenadas']['latitude'], row['coordenadas']['longitude']],
                    popup=f"{row['nome_local']} ({row['distancia_km']} km)"
                ).add_to(mapa)

            st_folium(mapa, width=700, height=500)
        else:
            st.info("Nenhum local encontrado nesse raio.")
