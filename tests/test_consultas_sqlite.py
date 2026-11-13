
from src.database import consultar_todas_lojas


def test_consulta_retorna_lojas():
    lojas = consultar_todas_lojas()

    assert len(lojas) > 0


def test_consulta_retorna_951_lojas():
    lojas = consultar_todas_lojas()

    assert len(lojas) == 951


def test_lojas_possuem_campos_esperados():
    lojas = consultar_todas_lojas()

    campos_esperados = {
        "store_id",
        "store_name",
        "total_pedidos",
        "pedidos_cancelados",
        "taxa_cancelamento",
        "tempo_mediano_ciclo",
        "pedidos_com_tempo",
    }

    assert campos_esperados.issubset(lojas[0].keys())


def test_integridade_dos_pedidos():
    lojas = consultar_todas_lojas()

    for loja in lojas:
        assert loja["total_pedidos"] >= 0
        assert loja["pedidos_cancelados"] >= 0
        assert loja["pedidos_cancelados"] <= loja["total_pedidos"]
        assert 0 <= loja["taxa_cancelamento"] <= 100
