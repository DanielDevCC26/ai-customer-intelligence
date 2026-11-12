
import streamlit as st
from src.analysis import analisar_cancelamentos
from src.report import gerar_relatorio_loja
from google.genai.errors import ServerError


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


st.subheader("🏪 Lojas prioritárias")

lojas = analisar_cancelamentos(limite=10)


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


st.subheader("📊 Cancelamentos por restaurante")

dados_grafico = {
    loja["store_name"]: loja["pedidos_cancelados"]
    for loja in lojas
}



import altair as alt

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

st.subheader("🤖 Análise com inteligência artificial")

lojas_disponiveis = {
    f"{loja['store_name']} (ID: {loja['store_id']})": loja["store_id"]
    for loja in lojas
}

loja_escolhida = st.selectbox(
    "Selecione um restaurante para análise:",
    options=list(lojas_disponiveis.keys()),
)

st.caption(
    "Selecione uma das lojas prioritárias para gerar "
    "um relatório operacional com inteligência artificial."
)


if "relatorio_ia" not in st.session_state:
    st.session_state.relatorio_ia = None


if "loja_relatorio_id" not in st.session_state:
    st.session_state.loja_relatorio_id = None


if st.button("🤖 Gerar análise com IA"):
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


if (
    st.session_state.relatorio_ia
    and st.session_state.loja_relatorio_id
    == lojas_disponiveis[loja_escolhida]
):
    st.markdown(st.session_state.relatorio_ia)



