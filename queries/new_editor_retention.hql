select 
    concat(cohort, "-01") as month,
    sum(cast(2nd_month_edits >= 1 as int)) / sum(cast(1st_month_edits >= 1 as int)) as new_editor_retention
from neilpquinn.new_editors
where cohort >= "{start}"
group by cohort
order by cohort asc
limit 1000