select
    month,
    sum(edits) as total_edits,
    sum(mobile_web_edits) as mobile_web_edits,
    sum(mobile_app_edits) as mobile_app_edits
from staging.editor_month
where month >= "{start}"
group by month;