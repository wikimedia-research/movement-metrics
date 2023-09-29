SELECT
    CONCAT(year, '-', month, '-01') AS month,
    SUM(mh_views) AS mh_pageviews
FROM wmf_product.mh_pageviews_corrected
WHERE
    year = {metrics_year}
    AND month = {metrics_cur_month}
GROUP BY CONCAT(year, '-', month, '-01')
