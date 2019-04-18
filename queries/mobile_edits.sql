select
    month,
    sum(mobile_web_edits + mobile_app_edits) as mobile_edits
from neilpquinn.editor_month
where month = "{metrics_month}"
group by month;