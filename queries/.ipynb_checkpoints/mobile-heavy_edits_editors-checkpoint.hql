with mh_editors as (
    select
        count(*) as edits,
        sum(cast(page_namespace_is_content_historical as int)) as content_edits,
        max(size(event_user_is_bot_by) > 0 or size(event_user_is_bot_by_historical) > 0) as bot
    from wmf.mediawiki_history mh
    inner join canonical_data.mobile_heavy_wikis mhw
    on mh.wiki_db = mhw.database_code
    where
        event_timestamp between "{metrics_month_start}" and "{metrics_month_end}" and
        not event_user_is_anonymous and
        snapshot = "{mediawiki_history_snapshot}" and
        event_entity = "revision" and
        event_type = "create"
    group by event_user_text
)
select
    "{metrics_month_first_day}" as month,
    sum(edits) as `mobile-heavy_wiki_edits`,
    sum(if(not bot, edits, 0)) as `mobile-heavy_wiki_nonbot_edits`,
    sum(cast(content_edits >= 5 as int)) as `mobile-heavy_wiki_active_editors`
from mh_editors