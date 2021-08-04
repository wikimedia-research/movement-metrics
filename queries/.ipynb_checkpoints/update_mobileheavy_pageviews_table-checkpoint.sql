INSERT OVERWRITE TABLE wmf_product.mh_pageviews_corrected
PARTITION (year, month, day)

SELECT CONCAT(year,'-',LPAD(month,2,'0'),'-',LPAD(day,2,'0')) AS dayy,
SUM(view_count) AS all_views,
SUM(IF (FIND_IN_SET(project,
'hi.wikipedia,bn.wikipedia,id.wikipedia,ar.wikipedia,mr.wikipedia,fa.wikipedia,sw.wikipedia,tl.wikipedia,zh.wikiquote,th.wikipedia,arz.wikipedia,ml.wikipedia,ta.wikipedia,kn.wikipedia,pt.wiktionary,az.wikipedia,gu.wikipedia,ky.wikipedia,sq.wikipedia,ms.wikipedia'
) > 0, view_count, 0)) AS mh_views,
year, month, day
FROM wmf.pageview_hourly
WHERE (year = '{metrics_year}'AND month = '{metrics_cur_month}')
AND agent_type != 'spider'
AND NOT (country_code IN ('PK', 'IR', 'AF') -- https://phabricator.wikimedia.org/T157404#3194046
AND user_agent_map['browser_family'] = 'IE') -- https://phabricator.wikimedia.org/T193578#4300284
GROUP BY year, month, day
