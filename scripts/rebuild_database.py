"""Reconstrói uma cópia do SQLite a partir dos CSVs públicos, sem alterar o banco em uso."""
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DB = OUTPUT_DIR / "customer_intelligence_rebuild.db"


def main():
    orders_path = RAW_DIR / "orders.csv"
    stores_path = RAW_DIR / "stores.csv"
    for path in (orders_path, stores_path):
        if not path.is_file():
            raise FileNotFoundError(f"Arquivo de entrada não encontrado: {path}")

    pedidos = pd.read_csv(orders_path)
    lojas = pd.read_csv(stores_path, encoding="latin-1")

    colunas_pedidos = {"order_id", "store_id", "order_status", "order_metric_cycle_time"}
    colunas_lojas = {"store_id", "store_name"}
    if not colunas_pedidos.issubset(pedidos.columns):
        raise ValueError(f"Colunas ausentes em orders.csv: {colunas_pedidos - set(pedidos.columns)}")
    if not colunas_lojas.issubset(lojas.columns):
        raise ValueError(f"Colunas ausentes em stores.csv: {colunas_lojas - set(lojas.columns)}")

    pedidos_lojas = pedidos.merge(lojas, on="store_id", how="left", validate="many_to_one")
    pedidos_lojas["cancelado"] = pedidos_lojas["order_status"] == "CANCELED"

    indicadores_lojas = (
        pedidos_lojas.groupby(["store_id", "store_name"])
        .agg(total_pedidos=("order_id", "count"), pedidos_cancelados=("cancelado", "sum"))
        .reset_index()
    )
    indicadores_lojas["taxa_cancelamento"] = (
        indicadores_lojas["pedidos_cancelados"] / indicadores_lojas["total_pedidos"] * 100
    )

    tempo_por_loja = (
        pedidos_lojas[pedidos_lojas["order_status"] == "FINISHED"]
        .groupby("store_id")
        .agg(
            tempo_mediano_ciclo=("order_metric_cycle_time", "median"),
            pedidos_com_tempo=("order_metric_cycle_time", "count"),
        )
        .reset_index()
    )
    desempenho_lojas = indicadores_lojas.merge(
        tempo_por_loja, on="store_id", how="left", validate="one_to_one"
    )

    # Os números esperados vêm da exploração original do conjunto público.
    esperado = (951, 368999, 16979)
    obtido = (
        len(desempenho_lojas),
        int(desempenho_lojas["total_pedidos"].sum()),
        int(desempenho_lojas["pedidos_cancelados"].sum()),
    )
    print(f"Indicadores reconstruídos (lojas, pedidos, cancelamentos): {obtido}")
    if obtido != esperado:
        raise ValueError(f"Indicadores diferentes do esperado {esperado}. Nenhum banco foi gravado.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if OUTPUT_DB.exists():
        raise FileExistsError(f"Arquivo de teste já existe; não será sobrescrito: {OUTPUT_DB}")

    try:
        with sqlite3.connect(OUTPUT_DB) as conexao:
            desempenho_lojas.to_sql("store_performance", conexao, if_exists="fail", index=False)
    except Exception:
        OUTPUT_DB.unlink(missing_ok=True)
        raise
    print(f"Banco de teste criado com sucesso: {OUTPUT_DB}")
    print("O banco principal customer_intelligence.db não foi alterado.")


if __name__ == "__main__":
    main()
