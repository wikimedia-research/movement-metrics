WITH gs_new_editors AS (
    SELECT
        1st_month_edits,
        2nd_month_edits
    FROM wmf_product.new_editors ne
    LEFT JOIN wmf.editors_daily gd
    ON
        ne.user_id = gd.user_fingerprint_or_name
        AND ne.wiki = gd.wiki_db
        AND ne.cohort = gd.month
    LEFT JOIN canonical_data.countries cdc
    ON gd.country_code = cdc.iso_code
    WHERE
        ne.cohort = '{retention_cohort}'
        AND gd.month = '{retention_cohort}'
        AND economic_region = 'Global North'
    GROUP BY
        user_name,
        wiki,
        1st_month_edits,
        2nd_month_edits
)
SELECT
    '{metrics_month_first_day}' AS month,
    SUM(CAST(2nd_month_edits >= 1 AS INT)) / COUNT(*) AS global_north_new_editor_retention
FROM
    gs_new_editors
