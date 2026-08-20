import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SMOLamp - Sistema Integrado SMO", layout="wide")

@st.cache_data
def carregar_iluminacao():
    caminho = "/content/drive/MyDrive/Banco_de_Dados_SMO/Solicitações - Recepção.xlsx"
    df = pd.read_excel(caminho, sheet_name="Iluminação")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def carregar_processos():
    caminho = "/content/drive/MyDrive/Banco_de_Dados_SMO/001 - Controle de Fluxo de Processos.xlsm"
    df = pd.read_excel(caminho, sheet_name="Processos", skiprows=2, engine='openpyxl')
    df.columns = df.columns.str.strip()
    return df

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Brasao_Cachoeiras_de_Macacu_RJ.png/120px-Brasao_Cachoeiras_de_Macacu_RJ.png", width=100)
st.sidebar.title("SMOLamp - Navegação")
menu_selecionado = st.sidebar.radio("Ir para:", ["Dashboard Iluminação", "Entrada de Processos"])
st.sidebar.divider()

if menu_selecionado == "Dashboard Iluminação":
    st.title("💡 SMOLamp - Dashboard de Iluminação Pública")
    
    try:
        df_iluminacao = carregar_iluminacao()
    except Exception as e:
        st.error(f'Erro ao ler o arquivo. Detalhe: {e}')
        st.stop()

    st.sidebar.subheader("Filtros do Dashboard")
    lista_bairros = ["Todos"] + list(df_iluminacao['LOCALIDADE'].dropna().unique())
    bairro_selecionado = st.sidebar.selectbox("Localidade/Bairro", lista_bairros)

    lista_status = ["Todos"] + list(df_iluminacao['STATUS DO PEDIDO'].dropna().unique())
    status_selecionado = st.sidebar.selectbox("Status do Pedido", lista_status)

    df_filtrado = df_iluminacao.copy()
    if bairro_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['LOCALIDADE'] == bairro_selecionado]
    if status_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['STATUS DO PEDIDO'] == status_selecionado]

    total_solicitacoes = len(df_filtrado)
    total_executado = len(df_filtrado[df_filtrado['STATUS DO PEDIDO'].astype(str).str.upper().str.contains('FEITO', na=False)])
    total_pendente = total_solicitacoes - total_executado
    taxa_eficiencia = (total_executado / total_solicitacoes) * 100 if total_solicitacoes > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Solicitações", total_solicitacoes)
    col2.metric("Total Executado", total_executado)
    col3.metric("Total Pendente", total_pendente)
    col4.metric("Taxa de Eficiência", f"{taxa_eficiencia:.1f}%")

    st.subheader(f"Listagem - {bairro_selecionado}")
    colunas_visiveis = ['RUA', 'LOCALIDADE', 'CONTRIBUINTE', 'DATA DO PEDIDO FEITO', 'STATUS DO PEDIDO', 'PEDIDO']
    st.dataframe(df_filtrado[colunas_visiveis], use_container_width=True, hide_index=True)

elif menu_selecionado == "Entrada de Processos":
    st.title("📂 SMOLamp - Recepção de Processos")
    
    try:
        df_processos = carregar_processos()
    except Exception as e:
        st.error(f'Erro ao ler o arquivo. Detalhe: {e}')
        st.stop()
        
    with st.form("form_novo_processo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            num_processo = st.text_input("NÚMERO do Processo", required=True)
            requerente = st.text_input("REQUERENTE", required=True)
            data_recebimento = st.date_input("DATA DE RECEBIMENTO", datetime.today())
        with col2:
            assunto = st.text_input("ASSUNTO", required=True)
            orgao_remetente = st.text_input("ÓRGÃO REMETENTE", required=True)
            funcionario_setor = st.text_input("FUNCIONÁRIO/SETOR", required=True)
            
        andamento_obs = st.text_area("1.º ANDAMENTO / OBSERVAÇÃO")
        submitted = st.form_submit_button("Registrar Processo")
        
        if submitted:
            st.success(f"Processo {num_processo} registrado com sucesso!")
            
    st.divider()
    st.subheader("Últimos Processos Cadastrados (Histórico)")
    st.dataframe(df_processos.head(5), use_container_width=True, hide_index=True)
