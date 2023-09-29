SELECT
    '{metrics_month_first_day}' AS month,
    COUNT(DISTINCT(page_id)) AS global_north_net_new_content
FROM wmf.mediawiki_history ne
LEFT JOIN wmf.editors_daily gd
ON
    ne.event_user_text = gd.user_fingerprint_or_name
    AND ne.wiki_db = gd.wiki_db
    AND gd.month = '{metrics_month}'
LEFT JOIN canonical_data.countries cdc
ON gd.country_code = cdc.iso_code
WHERE
    event_entity = 'page'
    AND event_type = 'create'
    AND event_timestamp IS NOT NULL
    AND snapshot = '{metrics_month}'
    AND event_timestamp BETWEEN '{metrics_month_first_day}' AND '{metrics_next_month_first_day}'
    AND page_namespace_is_content
    AND cdc.economic_region = 'Global North'
    AND NOT page_is_redirect
