SELECT 
    CONCAT(year,'-',month,'-01')AS month,
    SUM(mh_views) AS mh_previews
FROM
(
    SELECT 
        year, 
        month,  
        day, 
        CONCAT(year,'-',LPAD(month,2,'0'),'-',LPAD(day,2,'0')) AS date,
      SUM(view_count) AS all,
      SUM(IF (FIND_IN_SET(project,   'hi.wikipedia,bn.wikipedia,id.wikipedia,ar.wikipedia,mr.wikipedia,fa.wikipedia,sw.wikipedia,tl.wikipedia,zh.wikiquote,th.wikipedia,arz.wikipedia,ml.wikipedia,ta.wikipedia,kn.wikipedia,pt.wiktionary,az.wikipedia,gu.wikipedia,ky.wikipedia,sq.wikipedia,ms.wikipedia'
    ) > 0, view_count, 0)) AS mh_views
    FROM wmf.virtualpageview_hourly 
    WHERE year >= 2019
    GROUP BY year, month, day
) a
WHERE  (year = {metrics_year} AND month = {metrics_cur_month})
GROUP BY CONCAT(year,'-',month,'-01')
ORDER BY month
LIMIT 100000