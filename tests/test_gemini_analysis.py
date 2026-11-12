from src.analysis import analisar_cancelamentos
from src.gemini_client import interpretar_loja


# Seleciona apenas uma loja prioritária
lojas = analisar_cancelamentos(limite=1)

if not lojas:
    print("Nenhuma loja prioritária encontrada.")
else:
    loja = lojas[0]

    print("Loja selecionada:", loja["store_name"])
    print("Total de pedidos:", loja["total_pedidos"])
    print("Pedidos cancelados:", loja["pedidos_cancelados"])
    print("Taxa de cancelamento:", loja["taxa_cancelamento"])

    print("\nInterpretação do Gemini:\n")

    interpretacao = interpretar_loja(loja)
    print(interpretacao)