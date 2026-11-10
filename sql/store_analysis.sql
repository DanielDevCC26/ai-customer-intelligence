-- Total de estabelecimentos cadastrados
SELECT COUNT(*) AS total_lojas
FROM store_performance;


-- Dez estabelecimentos com maiores taxas de cancelamento
-- Considerando pelo menos 100 pedidos
SELECT
    store_id,
    store_name,
    total_pedidos,
    pedidos_cancelados,
    ROUND(taxa_cancelamento, 2) AS taxa_cancelamento_pct
FROM store_performance
WHERE total_pedidos >= 100
ORDER BY taxa_cancelamento DESC
LIMIT 10;


-- Estabelecimentos com cancelamento acima da referência geral
-- Ordenados pela quantidade absoluta de pedidos cancelados
SELECT
    store_id,
    store_name,
    total_pedidos,
    pedidos_cancelados,
    ROUND(taxa_cancelamento, 2) AS taxa_cancelamento_pct,
    ROUND(tempo_mediano_ciclo, 2) AS tempo_mediano_min
FROM store_performance
WHERE total_pedidos >= 100
  AND taxa_cancelamento > 4.6
ORDER BY pedidos_cancelados DESC;