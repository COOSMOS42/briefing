import streamlit as st
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from gspread_pandas import Spread, Client
from gspread_dataframe import set_with_dataframe

# Definir escopos para Google Sheets e Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carregar as credenciais de acesso do arquivo JSON
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes= scope)
# Autenticar com o Google Sheets (conectar as credencias)
client = Client(scope=scope, creds=creds)
spreadsheetname = "controlador"
spread = Spread(spreadsheetname, client = client)
#link com a planilha do google sheets
sheet = client.open(spreadsheetname).sheet1

val = sheet.get_all_values()
# fr é a variavel da planilha do google sheets
fr = pd.DataFrame(val)
#separa a primeira linha da planilha google sheets
cab = fr.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr = fr[1:]
#seta as colunas
fr.columns = cab


if 'jsoninput' not in st.session_state:
    st.session_state.jsoninput = None

def adicionar_entrega(A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P):
    entrega = {
        'A': A,
        'B': B,
        'C': C,
        'D': D,
        'E' : E,
        'F': F,
        'G': G,
        'H': H,
        'I': I,
        'J': J,
        'K': K,
        'L': L,
        'M': M,
        'N': N,
        'O': O,
        'P': P
    }

    st.session_state.jsoninput = pd.concat(
        [st.session_state.jsoninput,
         pd.DataFrame(entrega, index=[0])],
        ignore_index=True)

    return st.session_state.jsoninput


with st.form('Preencha os dados', clear_on_submit=True, border=True):
    st.subheader('Contato')
    a = st.text_input('Coloque aqui o seu E-mail para contato:')

    st.subheader('Briefing')
    b = st.text_input('Qual a área de atuação da empresa?')

    c = st.text_input('Descreva sua empresa.')

    d = st.text_input('Descreva seu produto ou serviço.')

    e = st.text_input('Qual o público-alvo? Quem é o seu cliente?')

    f = st.text_input('Qual mensagem sua maraca deve transmitir para os seus clientes?')

    g = st.text_input('Quais são os adjetivos que melhor descreveriam sua identidade?')

    h = st.text_input('Qual texto (exato) você quer que apareça no seu logo?')

    i = st.text_input('Existe algum slogan?')

    j = st.text_input('Existem algum(s) logo(s) que você acha interessante e que o perfil dele se encaixe com o seu? Se sim, deixe o link e explique o porquê.')

    k = st.text_input('Espaço para upload do logo que acha interessante.')

    l = st.text_input('Existe alguma cor que NÃO deve ser utilizada? Se sim, por quê?')

    m = st.text_input('Existe alguma cor que precisa ter?')

    n = st.text_input('Onde o seu logo será utilizado?')

    o = st.text_input('Tem algo que não deve ser incluído de maneira nenhuma no seu logo?')

    p = st.text_input('Fique a vontade para colocar alguma observação extra!')

    if st.form_submit_button('Salvar'):
        st.session_state.jsoninput = adicionar_entrega(
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p)
        st.success('Informações salvas com sucesso!')