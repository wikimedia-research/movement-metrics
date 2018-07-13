select
    date_format(event_timestamp, "yyyy-MM-01") as month,
    count(*) as total_edits,
    sum(cast(upload as int)) as uploads,
    sum(cast(data_edit as int)) as data_edits,
    sum(cast(nonbot_edit and not data_edit and not upload as int)) as nonbot_nondata_nonupload_edits,
    sum(cast(reverted as int)) / sum(cast(nonbot_edit as int)) as revert_rate
from (
    select
        event_timestamp,
        not (event_user_is_bot_by_name or array_contains(event_user_groups, "bot")) as nonbot_edit,
        (wiki_db = "wikidatawiki" and page_namespace_historical in (0, 120)) as data_edit,
        revision_is_identity_reverted as reverted,
        (revision_parent_id = 0 and page_namespace_historical = 6) as upload
    from wmf.mediawiki_history
    where
        event_entity = "revision" and
        event_type = "create" and
        event_timestamp >= "{start}" and
        snapshot = "{snapshot}"
) edits
group by date_format(event_timestamp, "yyyy-MM-01")
