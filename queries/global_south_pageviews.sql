SELECT
    CONCAT(year, '-', month, '-01') AS month,
    SUM(pageviews) AS gs_pageviews
FROM wmf_product.global_markets_pageviews
WHERE
    year = {metrics_year}
    AND month = {metrics_cur_month}
    AND region = 'Global South'
GROUP BY CONCAT(year, '-', month, '-01')
