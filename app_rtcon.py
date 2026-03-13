import streamlit as st
import pandas as pd
# Importa a função do arquivo backend_rtcon.py
# O arquivo backend_rtcon.py DEVE estar na mesma pasta deste arquivo
from backend_rtcon import processar_dados

# --- CONFIGURAÇÃO DA PÁGINA ---
# Deve ser sempre o primeiro comando do Streamlit
st.set_page_config(page_title="Portal RTCON", page_icon="☢️", layout="wide")

# --- FRONTEND ---
st.title("☢️ Portal RTCON - IBCC")

# Menu Lateral
opcao = st.sidebar.radio("Navegação", ["Início", "Controle de Vencimentos"])

if opcao == "Início":
    st.info("Bem-vindo ao sistema.")

elif opcao == "Controle de Vencimentos":
    st.header("Controle de Prazos")
    
    col1, col2 = st.columns(2)
    
    acao = None
    if col1.button("🔍 Verificar"):
        acao = "verificar"
    if col2.button("🚀 Enviar E-mails", type="primary"):
        acao = "enviar"
        
    if acao:
        with st.spinner('Processando dados...'):
            # Chama a função que está no outro arquivo
            resultado = processar_dados(disparar=(acao == "enviar"))
        
        # Verifica se o retorno é um erro (string) ou dados (DataFrame)
        if isinstance(resultado, str):
            st.error(f"Ocorreu um erro no backend: {resultado}")
        else:
            # Exibe a tabela formatada
            st.dataframe(resultado, use_container_width=True, hide_index=True)
            
            if acao == "enviar":
                st.success("Processo de envio finalizado.")