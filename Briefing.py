import streamlit as st

pg = st.navigation([
    st.Page("slit.py", title="Solicitar Peças"),
    st.Page("consultas.py", title="Consultar Status")
])
pg.run()
