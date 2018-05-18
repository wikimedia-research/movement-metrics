select
    date_format(event_timestamp, "yyyy-MM-01") as month,
    sum(cast(
        revision_parent_id = 0 and page_namespace_historical = 6
    as int)) as uploads,
    sum(cast(
        wiki_db = "wikidatawiki" and page_namespace_historical in (0, 120)
    as int)) as data_edits
from wmf.mediawiki_history
where
    event_entity = "revision" and
    event_type = "create" and
    event_timestamp >= "{start}" and
    snapshot = "{snapshot}"
group by date_format(event_timestamp, "yyyy-MM-01")