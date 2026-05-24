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
spreadsheetname = "trainee"
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

st.set_page_config(page_title='Briefing para construção de logotipos',
                   layout='wide')

if 'jsoninput' not in st.session_state:
    st.session_state.jsoninput = None

def adicionar_entrega(B, C, D, E, F, G, H):
    entrega = {
        'B': B,
        'C': C,
        'D': D,
        'E' : E,
        'F': F,
        'G': G,
        'H': H
    }

    st.session_state.jsoninput = pd.concat(
        [st.session_state.jsoninput,
         pd.DataFrame(entrega, index=[0])],
        ignore_index=True)

    return st.session_state.jsoninput


with st.form('Preencha os dados', clear_on_submit=False, border=True):

    st.subheader('Lançamento')
    b = st.date_input(label='Selecione uma data',format='DD/MM/YYYY')

    c = desc = st.text_input('Descriçao do lançamento')


    lista_cr = ['Suspençao e Dinamica Veicular', 'Aerodinamica', 'Drivetrain', 'Powertrain', 'Eletronica e Controle', 'Estrutura', 'Freio', 'Gestao de Pessoas', 'Marketin', 'Comercial', 'Patrimonio']
    d = st.selectbox('Selecione o centro de responsabilidade',(lista_cr))

    e = st.text_input('Valor referente ao lançameto')

    f = st.selectbox('Natureza', ("Faturamentio",'Custo'))
    
    g = st.selectbox('Status', ("Concluido",'Pendente'))

    h = st.date_input(label='Selecione uma data',format='DD/MM/YYYY')


    st.write('Salve as informaçõs antes do envio')
    if st.form_submit_button('Salvar'):
        st.session_state.jsoninput = adicionar_entrega(
            b, c, d, e, f, g, h)
        st.success('Informações salvas com sucesso!')


if st.button('Enviar dados 📨'):
    set_with_dataframe(sheet,
                       st.session_state.jsoninput,
                       row=len(sheet.col_values(1)) + 1,
                       include_column_header=False)
    st.success('Dados enviados com sucesso!')



