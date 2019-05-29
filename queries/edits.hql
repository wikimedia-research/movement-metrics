select
    date_format(event_timestamp, "yyyy-MM-01") as month,
    count(*) as total_edits,
    sum(cast(upload as int)) as uploads,
    sum(cast(mobile_edit as int)) as mobile_edits,
    sum(cast(data_edit as int)) as data_edits,
    sum(cast(nonbot_edit and not data_edit and not upload and not mobile_edit as int)) as other_nonbot_edits,
    sum(cast(reverted as int)) / sum(cast(nonbot_edit as int)) as revert_rate
from (
    select
        event_timestamp,
        (
            array_contains(revision_tags, "mobile edit") or
            array_contains(revision_tags, "mobile app edit") or 
            array_contains(revision_tags, "mobile web edit")
        ) as mobile_edit,
        size(event_user_is_bot_by) = 0 and size(event_user_is_bot_by_historical) = 0 as nonbot_edit,
        (wiki_db = "wikidatawiki" and page_namespace_historical in (0, 120)) as data_edit,
        revision_is_identity_reverted as reverted,
        (revision_parent_id = 0 and page_namespace_historical = 6) as upload
    from wmf.mediawiki_history
    where
        event_entity = "revision" and
        event_type = "create" and
        event_timestamp between "{metrics_month_start}" and "{metrics_month_end}" and
        snapshot = "{mediawiki_history_snapshot}"
) edits
group by date_format(event_timestamp, "yyyy-MM-01")
