SELECT 
    CONCAT(year,'-',month,'-01') AS month,
    SUM(view_count) as automated_pageviews
FROM wmf.pageview_hourly
WHERE (year = {metrics_year} AND month = {metrics_cur_month})
    AND agent_type = 'automated'
    AND NOT (country_code IN ('PK', 'IR', 'AF') -- https://phabricator.wikimedia.org/T157404#3194046
    AND user_agent_map['browser_family'] = 'IE') -- https://phabricator.wikimedia.org/T193578#4300284
GROUP BY CONCAT(year,'-',month,'-01')