SELECT
   -- DATE_FORMAT(date, 'YYYY-MM-01') AS month,
    CONCAT(year,'-',month,'-01') AS month,
    SUM(previews_seen) AS previews_seen
FROM
(
    SELECT year, month, day,
      CONCAT(year,'-',LPAD(month,2,'0'),'-',LPAD(day,2,'0')) AS date,
      SUM(view_count) AS previews_seen
    FROM wmf.virtualpageview_hourly 
    WHERE year >= 2019
    GROUP BY year, month, day

) a
--WHERE DATE_FORMAT(date, 'YYYY-MM-01') = 
--GROUP BY DATE_FORMAT(date, 'YYYY-MM-01')
WHERE  (year = {metrics_year} AND month = {metrics_cur_month})
GROUP BY CONCAT(year,'-',month,'-01')
ORDER BY month
LIMIT 10000