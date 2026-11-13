
from src.analysis import classificar_restaurante


def test_amostra_limitada():
    loja = {
        "total_pedidos": 13,
        "taxa_cancelamento": 100.0,
    }

    resultado = classificar_restaurante(loja, 4.6)

    assert resultado == "Amostra limitada"


def test_restaurante_em_atencao():
    loja = {
        "total_pedidos": 4470,
        "taxa_cancelamento": 25.82,
    }

    resultado = classificar_restaurante(loja, 4.6)

    assert resultado == "Atenção"


def test_restaurante_dentro_da_referencia():
    loja = {
        "total_pedidos": 3739,
        "taxa_cancelamento": 2.35,
    }

    resultado = classificar_restaurante(loja, 4.6)

    assert resultado == "Dentro da referência"


def test_limite_minimo_de_pedidos():
    loja = {
        "total_pedidos": 100,
        "taxa_cancelamento": 5.0,
    }

    resultado = classificar_restaurante(loja, 4.6)

    assert resultado == "Atenção"


def test_taxa_igual_a_referencia():
    loja = {
        "total_pedidos": 500,
        "taxa_cancelamento": 4.6,
    }

    resultado = classificar_restaurante(loja, 4.6)

    assert resultado == "Dentro da referência"
