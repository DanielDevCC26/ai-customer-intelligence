import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "customer_intelligence.db"


def conectar_banco():
    """Abre uma conexão com o banco SQLite do projeto."""
    return sqlite3.connect(DB_PATH)

def consultar_lojas_criticas(limite=10):
    """Consulta lojas com maior volume de cancelamentos."""

    conexao = conectar_banco()

    try:
        cursor = conexao.execute(
            """
            SELECT
                store_id,
                store_name,
                total_pedidos,
                pedidos_cancelados,
                ROUND(taxa_cancelamento, 2) AS taxa_cancelamento
            FROM store_performance
            WHERE total_pedidos >= 100
              AND taxa_cancelamento > 4.6
            ORDER BY pedidos_cancelados DESC
            LIMIT ?
            """,
            (limite,)
        )

        colunas = [coluna[0] for coluna in cursor.description]
        resultados = cursor.fetchall()

        return [
            dict(zip(colunas, linha))
            for linha in resultados
        ]

    finally:
        conexao.close()