select 
    month,
    sum(edits) as nonbot_edits
from (
    select 
        month,
        -- Convert from BINARY to CHAR so that case-insentive regexes work
        convert(user_name using utf8) as name,
        sum(edits) as edits,
        max(bot_flag) as bot_flag
    from staging.editor_month
    where 
        month = "{metrics_month_first_day}"
    group by month, name
) global_edits
where
    -- A user is a bot if they have a matching name or have the bot flag on *any* wiki
    -- See https://meta.wikimedia.org/wiki/Research:Active_editor and https://meta.wikimedia.org/wiki/Research:Bot_user
    bot_flag = 0 and (
        name not regexp "bot\\\\b" or
        name in ("Paucabot", "Niabot", "Marbot")    
    )
group by month;