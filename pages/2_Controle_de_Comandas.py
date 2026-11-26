# Página de controle de comandas do Bovinu'S Augusta.
# Esta página conversa com a API FastAPI do Lucas, sem alterar o código dele.

import streamlit as st
import requests
import pandas as pd

# Endereço local da API FastAPI.
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Controle de Comandas - Bovinu'S Augusta",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Controle de Comandas")
st.caption("Acompanhamento de entrada, pesagem e saída das comandas.")

# Consulta as comandas que ainda estão em andamento.
def buscar_comandas_ativas():
    try:
        resposta = requests.get(
            f"{API_URL}/api/comandas/ativas",
            timeout=5
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as erro:
        st.error(f"Não foi possível consultar a API: {erro}")
        return None

# Consulta o resumo das métricas calculadas pela API.
def buscar_metricas():
    try:
        resposta = requests.get(
            f"{API_URL}/api/metricas/resumo",
            timeout=5
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as erro:
        st.warning(f"Não foi possível carregar as métricas: {erro}")
        return None

# Envia uma etapa da comanda para a API.
def registrar_etapa(codigo, etapa):
    try:
        resposta = requests.post(
            f"{API_URL}/api/bip",
            json={"codigo": codigo, "etapa": etapa},
            timeout=10
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as erro:
        # Mostra a mensagem devolvida pela API quando houver erro HTTP.
        detalhe = ""
        if getattr(erro, "response", None) is not None:
            detalhe = erro.response.text
        st.error(f"Falha ao registrar a etapa: {erro}\n{detalhe}")
        return None

# Formulário para registrar entrada, pesagem ou saída.
st.subheader("Registrar etapa da comanda")

with st.form("form_comanda"):
    codigo = st.text_input(
        "Código da comanda",
        placeholder="Ex.: COMANDA001"
    ).strip().upper()

    etapa = st.selectbox(
        "Etapa",
        ["ENTRADA", "PESAGEM", "SAIDA"]
    )

    enviar = st.form_submit_button("Registrar etapa", type="primary")

if enviar:
    if not codigo:
        st.warning("Informe o código da comanda.")
    else:
        resultado = registrar_etapa(codigo, etapa)
        if resultado:
            st.success("Etapa registrada com sucesso!")
            st.json(resultado.get("sessao", resultado))
            st.rerun()

st.divider()

# Mostra as comandas que ainda não foram finalizadas.
st.subheader("Comandas em andamento")
ativas = buscar_comandas_ativas()

if ativas is not None:
    st.metric("Total de comandas ativas", ativas.get("total_ativas", 0))
    comandas = ativas.get("comandas", [])

    if comandas:
        st.dataframe(pd.DataFrame(comandas), use_container_width=True)
    else:
        st.info("Não há comandas em andamento no momento.")

st.divider()

# Exibe o resumo geral retornado pela API.
st.subheader("Resumo de métricas")
metricas = buscar_metricas()

if metricas is not None:
    # Exibe os dados exatamente como a API os fornece, sem inventar campos.
    st.json(metricas)

st.caption(
    "A API precisa estar em execução no endereço http://127.0.0.1:8000 "
    "para esta página funcionar."
)
