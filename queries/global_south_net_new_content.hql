select 
    '{metrics_month_first_day}' as month,
    count(distinct(page_id)) as global_south_net_new_content
from wmf.mediawiki_history ne
left join wmf.editors_daily gd
    on
        ne.event_user_text = gd.user_fingerprint_or_name and
        ne.wiki_db = gd.wiki_db and
        gd.month = '{metrics_month}'
    left join canonical_data.countries cdc
    on gd.country_code = cdc.iso_code
where 
    event_entity = 'revision' AND
    event_type = 'create' AND
    revision_parent_id == 0 AND
    event_timestamp IS NOT NULL AND 
    snapshot =  '{metrics_month}' AND 
    event_timestamp between '{metrics_month_first_day}' and '{metrics_next_month_first_day}' AND
    page_namespace_is_content AND
    cdc.economic_region = 'Global South' AND
    NOT page_is_redirect 
