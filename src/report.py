
from src.database import consultar_todas_lojas
from src.gemini_client import interpretar_loja


def gerar_relatorio_loja(store_id):
    """Gera um relatório de IA para qualquer loja cadastrada."""

    lojas = consultar_todas_lojas()

    loja_selecionada = next(
        (loja for loja in lojas if loja["store_id"] == store_id),
        None,
    )

    if loja_selecionada is None:
        return "Loja não encontrada no banco de dados."

    return interpretar_loja(loja_selecionada)
