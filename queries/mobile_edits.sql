select
    month,
    sum(mobile_web_edits + mobile_app_edits) as mobile_edits
from staging.editor_month
where month >= "{start}"
group by month;