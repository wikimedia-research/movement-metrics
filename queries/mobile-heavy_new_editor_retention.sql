SELECT
    '{metrics_month_first_day}' AS month,
    SUM(CAST(2nd_month_edits >= 1 AS INT))
        / SUM(CAST(1st_month_edits >= 1 AS INT)) AS `mobile-heavy_wiki_new_editor_retention`
FROM wmf_product.new_editors
INNER JOIN canonical_data.mobile_heavy_wikis
ON wiki = database_code
WHERE cohort = '{retention_cohort}'
