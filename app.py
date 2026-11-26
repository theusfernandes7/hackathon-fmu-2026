# ============================================================
# BOVINU'S AUGUSTA | PAINEL DE MIX E QUALIDADE
# Versão integrada ao banco de dados MySQL
# ============================================================

# Importamos as bibliotecas usadas pelo painel
import streamlit as st
import pandas as pd

# Importamos a função de conexão criada no arquivo conexao.py
from conexao import conectar_banco


# ============================================================
# 1. CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Bovinu'S Augusta | Gestão",
    page_icon="🍽️",
    layout="wide"
)


# ============================================================
# 2. FUNÇÕES DE ACESSO AO MYSQL
# ============================================================

def salvar_registro(data, refeicao, alimento, disponibilizado, sobras):
    """
    Salva um registro de alimento no MySQL.

    Primeiro localiza ou cadastra o alimento e a refeição.
    Depois grava as quantidades na tabela controle_refeicao.
    """

    conexao = None
    cursor = None

    try:
        # Abre a conexão com o banco bobinus_augusta
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Procura o alimento pelo nome para evitar duplicidade
        cursor.execute(
            "SELECT id_alimento FROM alimentos WHERE nome = %s",
            (alimento,)
        )
        resultado_alimento = cursor.fetchone()

        # Se o alimento ainda não existir, cadastra
        if resultado_alimento:
            id_alimento = resultado_alimento[0]
        else:
            cursor.execute(
                "INSERT INTO alimentos (nome, unidade_medida) VALUES (%s, %s)",
                (alimento, "kg")
            )
            id_alimento = cursor.lastrowid

        # Procura a refeição pelo nome
        cursor.execute(
            "SELECT id_refeicao FROM refeicoes WHERE nome = %s",
            (refeicao,)
        )
        resultado_refeicao = cursor.fetchone()

        # Se a refeição ainda não existir, cadastra
        if resultado_refeicao:
            id_refeicao = resultado_refeicao[0]
        else:
            cursor.execute(
                "INSERT INTO refeicoes (nome) VALUES (%s)",
                (refeicao,)
            )
            id_refeicao = cursor.lastrowid

        # Registra as quantidades na tabela de controle
        cursor.execute(
            """
            INSERT INTO controle_refeicao (
                id_alimento,
                id_refeicao,
                data_registro,
                quantidade_disponibilizada,
                quantidade_sobra
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_alimento, id_refeicao, data, disponibilizado, sobras)
        )

        # Confirma a gravação no banco de dados
        conexao.commit()

        return True, "Registro salvo no MySQL com sucesso!"

    except Exception as erro:
        # Desfaz alterações caso alguma etapa apresente erro
        if conexao:
            conexao.rollback()

        return False, f"Não foi possível salvar o registro: {erro}"

    finally:
        # Fecha cursor e conexão mesmo se ocorrer um erro
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


def buscar_registros():
    """
    Consulta os registros salvos no MySQL.
    O JOIN combina os dados das três tabelas do módulo.
    """

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                cr.id_registro,
                cr.data_registro AS data,
                r.nome AS refeicao,
                a.nome AS alimento,
                cr.quantidade_disponibilizada AS disponibilizado_kg,
                cr.quantidade_sobra AS sobras_kg
            FROM controle_refeicao cr
            INNER JOIN alimentos a
                ON cr.id_alimento = a.id_alimento
            INNER JOIN refeicoes r
                ON cr.id_refeicao = r.id_refeicao
            ORDER BY cr.data_registro DESC, cr.id_registro DESC
            """
        )

        registros = cursor.fetchall()

        # Converte as linhas retornadas pelo MySQL em uma tabela Pandas
        df = pd.DataFrame(registros)

        return df, None

    except Exception as erro:
        return pd.DataFrame(), str(erro)

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


# ============================================================
# 3. ESTILO VISUAL
# ============================================================

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
# 4. CABEÇALHO
# ============================================================

st.title("🍽️ Bovinu'S Augusta")
st.caption("MONITORAMENTO DE MIX E QUALIDADE ALIMENTAR")
st.write(
    "Acompanhe os alimentos disponibilizados, "
    "as sobras e os indicadores de consumo aparente."
)
st.divider()


# ============================================================
# 5. MENU LATERAL
# ============================================================

with st.sidebar:
    st.title("🍽️ Bovinu'S")
    st.caption("Mix e Qualidade")
    st.divider()

    # O filtro permite visualizar todas as refeições ou apenas uma
    filtro_refeicao = st.selectbox(
        "Filtrar refeição",
        ["Todas", "Almoço", "Jantar"]
    )

    # Indica que o painel já utiliza o banco de dados
    st.success("Conectado ao MySQL")


# ============================================================
# 6. CADASTRO DE ALIMENTOS
# ============================================================

st.header("📝 Registro de alimentos")
col_cadastro, col_info = st.columns([2, 1])

with col_cadastro:
    with st.form("cadastro_alimento"):

        # Campo para selecionar a data do registro
        data = st.date_input("Data do registro")

        # Campo para selecionar a refeição
        refeicao = st.selectbox(
            "Refeição",
            ["Almoço", "Jantar"]
        )

        # Campo para informar o alimento
        alimento = st.text_input(
            "Nome do alimento",
            placeholder="Ex.: Picanha"
        )

        # Campo para informar o peso disponibilizado
        disponibilizado = st.number_input(
            "Quantidade disponibilizada (kg)",
            min_value=0.0,
            step=0.5
        )

        # Campo para informar o peso das sobras
        sobras = st.number_input(
            "Quantidade de sobras (kg)",
            min_value=0.0,
            step=0.5
        )

        # Botão que envia os dados do formulário
        enviar = st.form_submit_button(
            "➕ Registrar alimento",
            use_container_width=True
        )

with col_info:
    st.markdown("### ℹ️ Como registrar")
    st.write("1. Selecione a data e a refeição.")
    st.write("2. Informe o nome e o peso disponibilizado.")
    st.write("3. Registre o peso das sobras.")
    st.write(
        "Os registros serão armazenados no banco de dados "
        "e continuarão disponíveis após fechar o painel."
    )


# ============================================================
# 7. VALIDAR E SALVAR NO MYSQL
# ============================================================

if enviar:

    # Verifica se o nome do alimento foi preenchido
    if not alimento.strip():
        st.error("Informe o nome do alimento.")

    # Verifica se a quantidade disponibilizada é válida
    elif disponibilizado <= 0:
        st.error("A quantidade disponibilizada deve ser maior que zero.")

    # Verifica se as sobras não ultrapassam o peso disponibilizado
    elif sobras > disponibilizado:
        st.error("As sobras não podem superar o disponibilizado.")

    else:
        # Chama a função que grava os dados no MySQL
        sucesso, mensagem = salvar_registro(
            data,
            refeicao,
            alimento.strip(),
            disponibilizado,
            sobras
        )

        if sucesso:
            st.success(mensagem)
        else:
            st.error(mensagem)


# ============================================================
# 8. BUSCAR E PREPARAR OS DADOS DO MYSQL
# ============================================================

# Busca novamente os registros sempre que o Streamlit atualiza a tela
df, erro_consulta = buscar_registros()

if erro_consulta:
    st.error(f"Erro ao consultar o MySQL: {erro_consulta}")

# Garante que a tabela tenha as colunas esperadas mesmo quando estiver vazia
colunas_esperadas = [
    "id_registro",
    "data",
    "refeicao",
    "alimento",
    "disponibilizado_kg",
    "sobras_kg"
]

for coluna in colunas_esperadas:
    if coluna not in df.columns:
        df[coluna] = pd.Series(dtype="object")

# Converte as quantidades para números para fazer os cálculos
if not df.empty:
    df["disponibilizado_kg"] = pd.to_numeric(
        df["disponibilizado_kg"]
    )
    df["sobras_kg"] = pd.to_numeric(df["sobras_kg"])

    # Calcula o consumo aparente de cada registro
    df["consumo_aparente_kg"] = (
        df["disponibilizado_kg"] - df["sobras_kg"]
    )

    # Calcula o percentual de sobras de cada registro
    df["percentual_sobra"] = (
        df["sobras_kg"] / df["disponibilizado_kg"]
    ) * 100

    # Arredonda os percentuais para duas casas decimais
    df["percentual_sobra"] = df["percentual_sobra"].round(2)

# Aplica o filtro de refeição selecionado no menu lateral
if filtro_refeicao != "Todas":
    df_filtrado = df[df["refeicao"] == filtro_refeicao].copy()
else:
    df_filtrado = df.copy()


# ============================================================
# 9. INDICADORES
# ============================================================

st.header("📊 Indicadores")

if not df_filtrado.empty:

    # Soma o peso total disponibilizado
    total_disponibilizado = df_filtrado["disponibilizado_kg"].sum()

    # Soma o peso total das sobras
    total_sobras = df_filtrado["sobras_kg"].sum()

    # Soma o consumo aparente
    total_consumo = df_filtrado["consumo_aparente_kg"].sum()

    # Calcula o percentual geral de sobras
    percentual_sobra = (
        total_sobras / total_disponibilizado
    ) * 100

    # Organiza os quatro indicadores em colunas
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Disponibilizado",
        f"{total_disponibilizado:.2f} kg"
    )
    col2.metric(
        "Sobras",
        f"{total_sobras:.2f} kg"
    )
    col3.metric(
        "Consumo aparente",
        f"{total_consumo:.2f} kg"
    )
    col4.metric(
        "Percentual de sobras",
        f"{percentual_sobra:.2f}%"
    )

else:
    st.info("Ainda não existem registros para essa seleção.")


# ============================================================
# 10. RELATÓRIOS
# ============================================================

st.divider()
st.header("📈 Relatórios")

aba_historico, aba_resumo = st.tabs(
    ["📋 Histórico", "🥩 Resumo por alimento"]
)


# ============================================================
# 11. ABA HISTÓRICO
# ============================================================

with aba_historico:

    if not df_filtrado.empty:

        # Exibe o histórico sem a coluna interna de identificação
        st.dataframe(
            df_filtrado.drop(columns=["id_registro"], errors="ignore"),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Cadastre alimentos para visualizar o histórico.")


# ============================================================
# 12. ABA RESUMO POR ALIMENTO
# ============================================================

with aba_resumo:

    if not df_filtrado.empty:

        # Agrupa os registros por alimento e soma as quantidades
        resumo = df_filtrado.groupby("alimento").agg(
            total_disponibilizado_kg=("disponibilizado_kg", "sum"),
            total_sobras_kg=("sobras_kg", "sum"),
            total_consumo_aparente_kg=("consumo_aparente_kg", "sum")
        )

        # Calcula o percentual consolidado de sobras por alimento
        resumo["percentual_sobra"] = (
            resumo["total_sobras_kg"] /
            resumo["total_disponibilizado_kg"]
        ) * 100

        # Arredonda o percentual para duas casas decimais
        resumo["percentual_sobra"] = resumo["percentual_sobra"].round(2)

        # Exibe a tabela consolidada
        st.dataframe(
            resumo,
            use_container_width=True
        )

        # Exibe o gráfico de consumo aparente por alimento
        st.subheader("Consumo aparente por alimento")
        st.bar_chart(resumo["total_consumo_aparente_kg"])

    else:
        st.info("Cadastre alimentos para gerar o resumo.")


# ============================================================
# 13. EXPORTAÇÃO
# ============================================================

st.divider()
st.header("📥 Exportação de dados")

if not df_filtrado.empty:

    # Converte os dados filtrados para CSV
    arquivo_csv = df_filtrado.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    # Disponibiliza o arquivo para download
    st.download_button(
        label="Baixar registros CSV",
        data=arquivo_csv,
        file_name="bovinus_registros.csv",
        mime="text/csv"
    )

else:
    st.info("Nenhum registro disponível para exportação.")


# ============================================================
# 14. RODAPÉ
# ============================================================

st.divider()
st.caption(
    "Bovinu'S Augusta | Hackathon Tech FMU | "
    "Painel de Mix e Qualidade conectado ao MySQL"
)
