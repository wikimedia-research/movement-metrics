INSERT OVERWRITE TABLE cchen.pageviews_corrected
PARTITION (year, month, day)
SELECT 
    CONCAT(year,'-',LPAD(month,2,'0'),'-',LPAD(day,2,'0')) AS dayy,
    SUM(IF(access_method = 'mobile app', view_count, null)) AS apps,
    SUM(IF(access_method = 'desktop', view_count, null)) AS desktop,
    SUM(IF(access_method = 'mobile web', view_count, null)) AS mobileweb,
    SUM(view_count) as total,
    year, month, day
FROM wmf.pageview_hourly
WHERE (year = {metrics_year} AND month = {metrics_cur_month})
    AND agent_type != 'spider'
    AND NOT (country_code IN ('PK', 'IR', 'AF') -- https://phabricator.wikimedia.org/T157404#3194046
    AND user_agent_map['browser_family'] = 'IE') -- https://phabricator.wikimedia.org/T193578#4300284
GROUP BY year, month, day
--GROUP BY CONCAT(year,'-',LPAD(month,2,'0'),'-',LPAD(day,2,'0'))