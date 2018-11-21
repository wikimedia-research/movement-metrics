select
    month,
    sum(mobile_web_edits + mobile_app_edits) as mobile_edits
from staging.editor_month
where month = "{metrics_month_first_day}"
group by month;