--SELECT
--    DATE_FORMAT(date, 'YYYY-MM-01') AS month,
--    SUM(pageviews) AS gs_pageviews
--FROM cchen.gs_pageviews_corrected
--WHERE
--     (year = {metrics_year} AND month = {metrics_cur_month})
--     AND region = 'Global South'
--GROUP BY DATE_FORMAT(date, 'YYYY-MM-01')


SELECT
    CONCAT(year,'-',month,'-01') AS month,
    SUM(pageviews) AS gs_pageviews
FROM cchen.gs_pageviews_corrected
WHERE  (year = {metrics_year} AND month = {metrics_cur_month})
    AND region = 'Global South'
GROUP BY CONCAT(year,'-',month,'-01')