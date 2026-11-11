from src.database import consultar_lojas_criticas


def analisar_cancelamentos(limite=10):
    """Analisa lojas prioritárias com base nos cancelamentos."""

    lojas = consultar_lojas_criticas(limite=limite)

    analises = []

    for loja in lojas:
        analise = {
            "store_id": loja["store_id"],
            "store_name": loja["store_name"].strip(),
            "total_pedidos": loja["total_pedidos"],
            "pedidos_cancelados": loja["pedidos_cancelados"],
            "taxa_cancelamento": loja["taxa_cancelamento"],
            "motivo_priorizacao": (
                "Taxa de cancelamento acima da referência "
                "geral de 4,6%, com pelo menos 100 pedidos. "
                "Ordenação pelo volume absoluto de cancelamentos."
            ),
            "acao_sugerida": (
                "Investigar os motivos dos cancelamentos "
                "antes de definir ações corretivas."
            )
        }

        analises.append(analise)

    return analises