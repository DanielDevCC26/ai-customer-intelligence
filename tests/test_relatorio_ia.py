
from unittest.mock import patch

from src.report import gerar_relatorio_loja


def test_gerar_relatorio_sem_chamar_gemini():
    resposta_simulada = "Relatório operacional gerado com sucesso."

    with patch(
        "src.report.interpretar_loja",
        return_value=resposta_simulada,
    ) as gemini_simulado:

        resultado = gerar_relatorio_loja(3)

    assert resultado == resposta_simulada

    gemini_simulado.assert_called_once()

    dados_loja = gemini_simulado.call_args.args[0]

    assert dados_loja["store_id"] == 3
    assert dados_loja["total_pedidos"] == 13
    assert dados_loja["pedidos_cancelados"] == 13


def test_relatorio_loja_inexistente():
    with patch("src.report.interpretar_loja") as gemini_simulado:
        resultado = gerar_relatorio_loja(-1)

    assert resultado == "Loja não encontrada no banco de dados."

    gemini_simulado.assert_not_called()
