select
    month,
    count(*) as active_editors,
    sum(cast(registration_month = month as int)) as new_active_editors,
    count(*) - sum(cast(registration_month = month as int)) as returning_active_editors
from (
    select
        cast(month as date) as month,
        user_name,
        sum(content_edits) as content_edits,
        max(bot_by_group) as bot_by_group,
        cast(trunc(min(user_registration), "MONTH") as date) as registration_month
    from wmf_product.editor_month
    where
        month = "{metrics_month_first_day}" and
        user_id != 0
    group by month, user_name
) global_edits
where
    content_edits >= 5 and
    not bot_by_group and
    user_name not regexp "bot\\b"
group by month
                              
