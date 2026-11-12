
from src.analysis import analisar_cancelamentos
from src.gemini_client import interpretar_loja


def gerar_relatorio_loja(store_id):
    """Gera um relatório de IA para uma loja prioritária."""

    lojas = analisar_cancelamentos(limite=951)

    loja_selecionada = next(
        (loja for loja in lojas if loja["store_id"] == store_id),
        None,
    )

    if loja_selecionada is None:
        return "Loja não encontrada entre as lojas prioritárias."

    return interpretar_loja(loja_selecionada)
