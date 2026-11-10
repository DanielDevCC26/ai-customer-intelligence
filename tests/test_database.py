from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.database import conectar_banco


conexao = conectar_banco()

resultado = conexao.execute(
    "SELECT COUNT(*) FROM store_performance"
).fetchone()

conexao.close()

print(f"Estabelecimentos encontrados: {resultado[0]}")

from src.database import consultar_lojas_criticas

print("\nLojas prioritárias para análise:")

lojas = consultar_lojas_criticas(limite=5)

for loja in lojas:
    print(loja)