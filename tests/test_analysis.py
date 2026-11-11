from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.analysis import analisar_cancelamentos


analises = analisar_cancelamentos(limite=3)

for analise in analises:
    print(f"\nLoja: {analise['store_name']}")
    print(f"ID: {analise['store_id']}")
    print(f"Pedidos: {analise['total_pedidos']}")
    print(f"Cancelamentos: {analise['pedidos_cancelados']}")
    print(f"Taxa: {analise['taxa_cancelamento']}%")
    print(f"Motivo: {analise['motivo_priorizacao']}")
    print(f"Ação sugerida: {analise['acao_sugerida']}")