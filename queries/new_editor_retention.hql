select 
    "{metrics_month_first_day}" as month,
    sum(cast(2nd_month_edits >= 1 as int)) / sum(cast(1st_month_edits >= 1 as int)) as new_editor_retention
from cchen.new_editor_retention
where cohort = "{retention_cohort}"