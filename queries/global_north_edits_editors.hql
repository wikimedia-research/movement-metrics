with gs_editors as (
    select 
        sum(edit_count) as edit_count,
        sum(namespace_zero_edit_count) as namespace_zero_edit_count,
        -- Treat the user as a bot if it matches on any wiki
        --max(size(is_bot_by) > 0 or size(is_bot_by_historical) > 0) as bot
        max(size(user_is_bot_by) > 0) as bot
    from wmf.editors_daily gd
    left join canonical_data.countries cdc
    on gd.country_code = cdc.iso_code
    --left join wmf.mediawiki_user_history muh
    --on
    --    gd.wiki_db = muh.wiki_db and
    --    gd.user_fingerprint_or_id = muh.user_id and
    --    muh.snapshot = "{mediawiki_history_snapshot}" and
    --    muh.end_timestamp is null
    where
        month = "{metrics_month}" and
        economic_region = "Global North" and
        not user_is_anonymous and 
        gd.action_type = 0
    group by user_fingerprint_or_id
)
select
    "{metrics_month_first_day}" as month,
    sum(edit_count) as global_north_edits,
    sum(if(not bot, edit_count, 0)) as global_north_nonbot_edits,
    sum(cast(namespace_zero_edit_count >= 5 as int)) as global_north_active_editors
from gs_editors