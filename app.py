
import altair as alt
import streamlit as st

from google.genai.errors import ServerError

from src.analysis import analisar_cancelamentos
from src.database import consultar_todas_lojas
from src.report import gerar_relatorio_loja


# Configuração inicial da aplicação
st.set_page_config(
    page_title="AI Customer Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Customer Intelligence")
st.subheader("Inteligência operacional para delivery")

st.write(
    "Plataforma de análise de desempenho de restaurantes, "
    "com indicadores operacionais e recomendações "
    "geradas por inteligência artificial."
)

st.divider()


# Consulta dos dados no SQLite
lojas = analisar_cancelamentos(limite=10)
todas_lojas = consultar_todas_lojas()


# ==================================================
# VISÃO GERAL DA PLATAFORMA
# ==================================================

st.subheader("📈 Visão geral da plataforma")

total_pedidos = sum(
    loja["total_pedidos"] for loja in todas_lojas
)

total_cancelamentos = sum(
    loja["pedidos_cancelados"] for loja in todas_lojas
)

taxa_geral = (
    total_cancelamentos / total_pedidos * 100
    if total_pedidos > 0 else 0
)

geral1, geral2, geral3, geral4 = st.columns(4)

geral1.metric(
    "Restaurantes",
    len(todas_lojas),
)

geral2.metric(
    "Total de pedidos",
    f"{total_pedidos:,}".replace(",", "."),
)

geral3.metric(
    "Cancelamentos",
    f"{total_cancelamentos:,}".replace(",", "."),
)

geral4.metric(
    "Taxa geral",
    f"{taxa_geral:.2f}%".replace(".", ","),
)

st.divider()


# ==================================================
# RANKING DE LOJAS PRIORITÁRIAS
# ==================================================

st.subheader("🏪 Lojas prioritárias")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Lojas prioritárias",
    len(lojas),
)

col2.metric(
    "Pedidos analisados",
    f"{sum(loja['total_pedidos'] for loja in lojas):,}".replace(",", "."),
)

col3.metric(
    "Pedidos cancelados",
    f"{sum(loja['pedidos_cancelados'] for loja in lojas):,}".replace(",", "."),
)

st.divider()

st.write(
    "Restaurantes com taxa de cancelamento acima de 4,6%, "
    "pelo menos 100 pedidos e priorização pelo volume "
    "absoluto de cancelamentos."
)

st.dataframe(
    lojas,
    column_order=[
        "store_id",
        "store_name",
        "total_pedidos",
        "pedidos_cancelados",
        "taxa_cancelamento",
    ],
    column_config={
        "store_id": "ID",
        "store_name": "Restaurante",
        "total_pedidos": "Total de pedidos",
        "pedidos_cancelados": "Cancelamentos",
        "taxa_cancelamento": st.column_config.NumberColumn(
            "Taxa de cancelamento (%)",
            format="%.2f",
        ),
    },
    width="stretch",
    hide_index=True,
)


# ==================================================
# GRÁFICO DE CANCELAMENTOS
# ==================================================

st.subheader("📊 Cancelamentos por restaurante")

dados = [
    {
        "Restaurante": loja["store_name"],
        "Cancelamentos": loja["pedidos_cancelados"],
    }
    for loja in lojas
]

grafico = (
    alt.Chart(alt.Data(values=dados))
    .mark_bar()
    .encode(
        x=alt.X("Restaurante:N", sort="-y"),
        y=alt.Y("Cancelamentos:Q"),
        tooltip=["Restaurante:N", "Cancelamentos:Q"],
    )
    .properties(height=350)
)

st.altair_chart(grafico, width="stretch")

st.divider()


# ==================================================
# ANÁLISE COM INTELIGÊNCIA ARTIFICIAL
# ==================================================

st.subheader("🤖 Análise com inteligência artificial")


pesquisa_loja = st.text_input(
    "🔎 Pesquisar restaurante",
    placeholder="Digite o nome ou ID da loja...",
)

lojas_filtradas = [
    loja for loja in todas_lojas
    if pesquisa_loja.lower() in loja["store_name"].lower()
    or pesquisa_loja in str(loja["store_id"])
]



lojas_disponiveis = {
    f"{loja['store_name']} (ID: {loja['store_id']})": loja["store_id"]
    for loja in lojas_filtradas
}



loja_escolhida = st.selectbox(
    "Selecione um restaurante para análise:",
    options=list(lojas_disponiveis.keys()),
    placeholder="Nenhum restaurante encontrado",
)

if not lojas_disponiveis:
    st.warning(
        "Nenhum restaurante corresponde à pesquisa. "
        "Tente outro nome ou ID."
    )


st.caption(
    "Selecione qualquer uma das 951 lojas cadastradas "
    "para consultar sua análise operacional."
)


# Armazena o relatório durante a sessão
if "relatorio_ia" not in st.session_state:
    st.session_state.relatorio_ia = None

if "loja_relatorio_id" not in st.session_state:
    st.session_state.loja_relatorio_id = None


# Geração do relatório sob demanda

if st.button(
    "🤖 Gerar análise com IA",
    disabled=not lojas_disponiveis,
):

    store_id = lojas_disponiveis[loja_escolhida]

    try:
        with st.spinner("Analisando os dados do restaurante..."):
            relatorio = gerar_relatorio_loja(store_id)

        st.session_state.relatorio_ia = relatorio
        st.session_state.loja_relatorio_id = store_id

    except ServerError as erro:
        if erro.code == 503:
            st.warning(
                "O Gemini está com alta demanda no momento. "
                "Aguarde alguns minutos antes de tentar novamente."
            )
        else:
            st.error(
                "O serviço de IA apresentou um erro temporário. "
                "Tente novamente mais tarde."
            )

    except Exception:
        st.error(
            "Não foi possível gerar o relatório neste momento. "
            "O serviço de inteligência artificial pode estar "
            "temporariamente indisponível. Tente novamente mais tarde."
        )


# Exibe apenas o relatório da loja selecionada

if (
    loja_escolhida is not None
    and st.session_state.relatorio_ia
    and st.session_state.loja_relatorio_id
    == lojas_disponiveis[loja_escolhida]
):
    st.markdown(st.session_state.relatorio_ia)

