select 
    month, 
    count(*) as active_editors,
    sum(extract(year_month from reg) not in (
        extract(year_month from month),
        extract(year_month from date_sub(month, interval 1 month))
    )) as existing_active_editors,
    sum(extract(year_month from reg) = extract(year_month from month)) as new_active_editors,
    sum(extract(year_month from reg) = extract(year_month from date_sub(month, interval 1 month))) as second_month_active_editors
from (
    select
        month,
        -- Convert from BINARY to CHAR so that case-insentive regexes work
        convert(user_name using utf8) as name,
        sum(content_edits) as content_edits,
        max(bot_flag) as bot_flag,
        min(user_registration) as reg
    from staging.editor_month
    where 
        month = "{metrics_month_first_day}" and
        local_user_id != 0
    group by month, name
) global_edits
where
    content_edits >= 5 and
    -- A user is a bot if they have a matching name or have the bot flag on *any* wiki
    -- See https://meta.wikimedia.org/wiki/Research:Active_editor and https://meta.wikimedia.org/wiki/Research:Bot_user
    bot_flag = 0 and (
        name not regexp "bot\\\\b" or
        name in ("Paucabot", "Niabot", "Marbot")    
    )
group by month;