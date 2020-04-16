select 
    '{metrics_month_first_day}' as month,
    count(distinct(page_id)) as global_south_wikidata_entities
from wmf.mediawiki_history ne
left join wmf.editors_daily gd
    on
        ne.event_user_id = gd.user_fingerprint_or_id and
        ne.wiki_db = gd.wiki_db and
        gd.month = '{metrics_month}'
    left join canonical_data.countries cdc
    on gd.country_code = cdc.iso_code
where 
    event_entity = 'page' AND
    event_type = 'create' AND
    event_timestamp IS NOT NULL AND 
    snapshot =  '{metrics_month}' AND 
    event_timestamp between '{metrics_month_first_day}' and '{metrics_next_month_first_day}' AND
    page_namespace_is_content AND
    cdc.economic_region = 'Global South' AND
    gd.wiki_db = "wikidatawiki" AND
    page_namespace_historical in (0, 120) AND
    NOT page_is_redirect 
