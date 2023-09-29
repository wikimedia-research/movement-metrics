SELECT
    CONCAT(year, '-', month, '-01') AS month,
    SUM(desktop) AS desktop,
    SUM(mobileweb) AS mobileweb,
    SUM(total) AS total_pageview
FROM wmf_product.pageviews_corrected
WHERE
    year = {metrics_year}
    AND month = {metrics_cur_month}
GROUP BY CONCAT(year, '-', month, '-01')
