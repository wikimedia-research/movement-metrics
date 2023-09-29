SELECT
    '{metrics_month_first_day}' AS month,
    SUM(CAST(2nd_month_edits >= 1 AS INT))
        / SUM(CAST(1st_month_edits >= 1 AS INT)) AS new_editor_retention
FROM wmf_product.new_editors
WHERE cohort = '{retention_cohort}'
