import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread

# Configuração automática do acesso seguro usando os segredos que você salvou
creds_dict = st.secrets["gcp"]
creds = service_account.Credentials.from_service_account_info(creds_dict)
gc = gspread.authorize(creds)

# ID da sua planilha (peguei o ID que aparece no link da sua imagem)
FILE_ID = "1DTCP3Gs_FjumfUO-QAAGAue8_2-b8cIB"

# Carrega os dados direto da aba "Iluminação"
sh = gc.open_by_key(FILE_ID)
worksheet = sh.worksheet("Iluminação")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Exibe no site
st.title("SMOLamp - Dashboard de Iluminação Pública")
st.dataframe(df)
