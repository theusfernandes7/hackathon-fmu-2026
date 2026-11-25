
# ============================================================
# BOVINU'S AUGUSTA | PAINEL DE MIX E QUALIDADE
# ============================================================

# Importamos o Streamlit para construir a interface
import streamlit as st

# Importamos Pandas para organizar, filtrar e calcular os dados
import pandas as pd

# ============================================================
# 1. CONFIGURAÇÃO
# ============================================================

# Definimos o título, ícone e layout do aplicativo
st.set_page_config(
    page_title="Bovinu'S Augusta | Gestão",
    page_icon="🍽️",
    layout="wide"
)

# ============================================================
# 2. ESTILO VISUAL
# ============================================================

# Aplicamos algumas configurações visuais ao painel
st.markdown("""
<style>

    /* Ajustamos a largura e o espaço interno da página */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Estilizamos os indicadores */
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. CABEÇALHO
# ============================================================

# Criamos o título do sistema
st.title("🍽️ Bovinu'S Augusta")

# Apresentamos o módulo
st.caption("MONITORAMENTO DE MIX E QUALIDADE ALIMENTAR")

# Apresentamos a finalidade do painel
st.write(
    "Acompanhe os alimentos disponibilizados, "
    "as sobras e os indicadores de consumo aparente."
)

# Criamos uma divisão visual
st.divider()

# ============================================================
# 4. ARMAZENAMENTO DOS REGISTROS
# ============================================================

# Inicializamos a lista de registros na memória da sessão
# Os registros serão mantidos durante a sessão atual
if "registros" not in st.session_state:
    st.session_state.registros = []

# ============================================================
# 5. MENU LATERAL
# ============================================================

# Criamos um menu lateral para organizar o sistema
with st.sidebar:

    # Apresentamos o nome do sistema no menu
    st.title("🍽️ Bovinu'S")

    # Apresentamos o nome do módulo
    st.caption("Mix e Qualidade")

    # Criamos uma divisão
    st.divider()

    # Criamos uma seleção de refeição para filtro
    filtro_refeicao = st.selectbox(
        "Filtrar refeição",
        ["Todas", "Almoço", "Jantar"]
    )

    # Criamos uma informação sobre o protótipo
    st.info(
        "Protótipo de demonstração. "
        "Os dados ainda não estão conectados ao MySQL."
    )

# ============================================================
# 6. CADASTRO DE ALIMENTOS
# ============================================================

# Criamos o título da área de cadastro
st.header("📝 Registro de alimentos")

# Criamos duas colunas para organizar o conteúdo
col_cadastro, col_info = st.columns([2, 1])

# Colocamos o formulário na primeira coluna
with col_cadastro:

    # Criamos um formulário de cadastro
    with st.form("cadastro_alimento"):

        # Campo de data
        data = st.date_input("Data do registro")

        # Campo de refeição
        refeicao = st.selectbox(
            "Refeição",
            ["Almoço", "Jantar"]
        )

        # Campo para nome do alimento
        alimento = st.text_input(
            "Nome do alimento",
            placeholder="Ex.: Picanha"
        )

        # Campo para quantidade disponibilizada
        disponibilizado = st.number_input(
            "Quantidade disponibilizada (kg)",
            min_value=0.0,
            step=0.5
        )

        # Campo para quantidade de sobras
        sobras = st.number_input(
            "Quantidade de sobras (kg)",
            min_value=0.0,
            step=0.5
        )

        # Botão para enviar o formulário
        enviar = st.form_submit_button(
            "➕ Registrar alimento",
            use_container_width=True
        )

# Colocamos informações explicativas na segunda coluna
with col_info:

    # Apresentamos uma explicação sobre o registro
    st.markdown("### ℹ️ Como registrar")

    # Explicamos a primeira etapa
    st.write(
        "1. Selecione a data e a refeição."
    )

    # Explicamos a segunda etapa
    st.write(
        "2. Informe o nome e o peso disponibilizado."
    )

    # Explicamos a terceira etapa
    st.write(
        "3. Registre o peso das sobras."
    )

    # Explicamos o objetivo do indicador
    st.write(
        "Os indicadores serão atualizados "
        "conforme os registros forem cadastrados."
    )

# ============================================================
# 7. VALIDAR E CADASTRAR
# ============================================================

# Verificamos se o formulário foi enviado
if enviar:

    # Verificamos se o nome do alimento está vazio
    if not alimento.strip():

        # Exibimos uma mensagem de erro
        st.error("Informe o nome do alimento.")

    # Verificamos se o peso disponibilizado é válido
    elif disponibilizado <= 0:

        # Exibimos uma mensagem de erro
        st.error("A quantidade disponibilizada deve ser maior que zero.")

    # Verificamos se as sobras são maiores que o disponibilizado
    elif sobras > disponibilizado:

        # Exibimos uma mensagem de erro
        st.error("As sobras não podem superar o disponibilizado.")

    # Se os dados forem válidos, realizamos o cadastro
    else:

        # Criamos um dicionário com os dados do registro
        novo_registro = {
            "data": str(data),
            "refeicao": refeicao,
            "alimento": alimento.strip(),
            "disponibilizado_kg": disponibilizado,
            "sobras_kg": sobras
        }

        # Adicionamos o registro à lista da sessão
        st.session_state.registros.append(novo_registro)

        # Exibimos uma mensagem de sucesso
        st.success("Registro cadastrado com sucesso!")

# ============================================================
# 8. PREPARAÇÃO DOS DADOS
# ============================================================

# Verificamos se existem registros
if st.session_state.registros:

    # Transformamos os registros em uma tabela
    df = pd.DataFrame(st.session_state.registros)

    # Calculamos o consumo aparente de cada registro
    df["consumo_aparente_kg"] = (
        df["disponibilizado_kg"] - df["sobras_kg"]
    )

    # Calculamos o percentual de sobras de cada registro
    df["percentual_sobra"] = (
        df["sobras_kg"] / df["disponibilizado_kg"]
    ) * 100

    # Arredondamos os percentuais
    df["percentual_sobra"] = df["percentual_sobra"].round(2)

    # ========================================================
    # 9. FILTRAR OS REGISTROS
    # ========================================================

    # Aplicamos o filtro de refeição escolhido no menu lateral
    if filtro_refeicao != "Todas":

        # Selecionamos apenas os registros da refeição escolhida
        df_filtrado = df[
            df["refeicao"] == filtro_refeicao
        ].copy()

    # Caso todas as refeições estejam selecionadas
    else:

        # Utilizamos todos os registros
        df_filtrado = df.copy()

    # ========================================================
    # 10. INDICADORES
    # ========================================================

    # Criamos o título dos indicadores
    st.header("📊 Indicadores")

    # Verificamos se há dados após o filtro
    if not df_filtrado.empty:

        # Somamos os pesos disponibilizados
        total_disponibilizado = (
            df_filtrado["disponibilizado_kg"].sum()
        )

        # Somamos as sobras
        total_sobras = df_filtrado["sobras_kg"].sum()

        # Somamos o consumo aparente
        total_consumo = (
            df_filtrado["consumo_aparente_kg"].sum()
        )

        # Calculamos o percentual geral de sobras
        percentual_sobra = (
            total_sobras / total_disponibilizado
        ) * 100

        # Criamos quatro colunas para os indicadores
        col1, col2, col3, col4 = st.columns(4)

        # Exibimos o disponibilizado
        col1.metric(
            "Disponibilizado",
            f"{total_disponibilizado:.2f} kg"
        )

        # Exibimos as sobras
        col2.metric(
            "Sobras",
            f"{total_sobras:.2f} kg"
        )

        # Exibimos o consumo aparente
        col3.metric(
            "Consumo aparente",
            f"{total_consumo:.2f} kg"
        )

        # Exibimos o percentual de sobras
        col4.metric(
            "Percentual de sobras",
            f"{percentual_sobra:.2f}%"
        )

    # Se o filtro não encontrar registros
    else:

        # Informamos que não há registros para o filtro
        st.info("Não existem registros para essa refeição.")

# ============================================================
# 11. RELATÓRIOS
# ============================================================

# Criamos uma divisão visual
st.divider()

# Criamos o título da seção de relatórios
st.header("📈 Relatórios")

# Criamos duas abas para organizar os relatórios
aba_historico, aba_resumo = st.tabs(
    ["📋 Histórico", "🥩 Resumo por alimento"]
)

# ============================================================
# 12. ABA HISTÓRICO
# ============================================================

# Organizamos o histórico na primeira aba
with aba_historico:

    # Verificamos se existem registros
    if st.session_state.registros:

        # Verificamos se existem dados após o filtro
        if not df_filtrado.empty:

            # Exibimos o histórico de registros
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )

        # Caso o filtro não encontre registros
        else:

            # Informamos que o histórico está vazio para esse filtro
            st.info("Nenhum registro encontrado para o filtro.")

    # Caso não exista nenhum registro
    else:

        # Informamos que o histórico está vazio
        st.info("Cadastre alimentos para visualizar o histórico.")

# ============================================================
# 13. ABA RESUMO POR ALIMENTO
# ============================================================

# Organizamos o relatório consolidado na segunda aba
with aba_resumo:

    # Verificamos se existem registros
    if st.session_state.registros:

        # Verificamos se existem dados após o filtro
        if not df_filtrado.empty:

            # Agrupamos os registros por alimento
            resumo = df_filtrado.groupby("alimento").agg(
                total_disponibilizado_kg=("disponibilizado_kg", "sum"),
                total_sobras_kg=("sobras_kg", "sum"),
                total_consumo_aparente_kg=("consumo_aparente_kg", "sum")
            )

            # Calculamos o percentual consolidado de sobras
            resumo["percentual_sobra"] = (
                resumo["total_sobras_kg"] /
                resumo["total_disponibilizado_kg"]
            ) * 100

            # Arredondamos os percentuais
            resumo["percentual_sobra"] = (
                resumo["percentual_sobra"].round(2)
            )

            # Exibimos a tabela consolidada
            st.dataframe(
                resumo,
                use_container_width=True
            )

            # Criamos um título para o gráfico
            st.subheader("Consumo aparente por alimento")

            # Criamos um gráfico de barras
            st.bar_chart(
                resumo["total_consumo_aparente_kg"]
            )

        # Caso não existam dados para o filtro
        else:

            # Informamos que não existem dados
            st.info("Não existem dados para gerar o resumo.")

    # Caso não existam registros
    else:

        # Informamos que é necessário cadastrar alimentos
        st.info("Cadastre alimentos para gerar o resumo.")

# ============================================================
# 14. EXPORTAÇÃO
# ============================================================

# Criamos uma divisão visual
st.divider()

# Criamos o título da área de exportação
st.header("📥 Exportação de dados")

# Verificamos se existem registros
if st.session_state.registros:

    # Verificamos se existem registros no filtro
    if not df_filtrado.empty:

        # Transformamos os dados filtrados em CSV
        arquivo_csv = df_filtrado.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        # Criamos o botão para baixar o CSV
        st.download_button(
            label="Baixar registros CSV",
            data=arquivo_csv,
            file_name="bovinus_registros.csv",
            mime="text/csv"
        )

    # Caso o filtro esteja vazio
    else:

        # Informamos que não existem dados para exportar
        st.info("Não existem registros para exportar.")

# Caso não existam registros
else:

    # Informamos que o sistema ainda não possui registros
    st.info("Nenhum registro disponível para exportação.")

# ============================================================
# 15. RODAPÉ
# ============================================================

# Criamos uma divisão visual
st.divider()

# Apresentamos a identificação do módulo
st.caption(
    "Bovinu'S Augusta | Hackathon Tech FMU | "
    "Protótipo de Mix e Qualidade"
)
