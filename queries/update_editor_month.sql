insert into neilpquinn.editor_month
select
    trunc(event_timestamp, "MONTH") as month,
    wiki_db,
    event_user_id as local_user_id,
    max(event_user_text) as user_name, -- Some rows incorrectly have a null `event_user_text`
    count(*) as edits,
    coalesce(
        sum(cast(page_namespace_is_content_historical as int)),
        0
    ) as content_edits,
    NULL as mobile_web_edits,
    NULL as mobile_app_edits,
    NULL as visual_edits,
    NULL as ve_source_edits,
    (
        max(event_user_is_bot_by_name) or 
        max(array_contains(event_user_groups, "bot")) or
        max(array_contains(event_user_groups_historical, "bot"))
    ) as bot,
    min(event_user_creation_timestamp) as user_registration
from wmf.mediawiki_history
where
    event_timestamp between "{start}" and "{end}" and
    event_entity = "revision" and
    event_type = "create" and
    snapshot = "{mwh_snapshot}"
group by
    trunc(event_timestamp, "MONTH"),
    wiki_db,
    event_user_id