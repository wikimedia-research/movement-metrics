WITH gs_editors AS (
    SELECT
        SUM(edit_count) AS edit_count,
        SUM(namespace_zero_edit_count) AS namespace_zero_edit_count,
        -- Treat the user as a bot if it matches on any wiki
        MAX(SIZE(user_is_bot_by) > 0) AS bot
    FROM wmf.editors_daily gd
    LEFT JOIN canonical_data.countries cdc
    ON gd.country_code = cdc.iso_code
    WHERE
        month = '{metrics_month}'
        AND economic_region = 'Global North'
        AND NOT user_is_anonymous
        AND gd.action_type = 0
    GROUP BY user_fingerprint_or_name
)
SELECT
    '{metrics_month_first_day}' AS month,
    SUM(edit_count) AS global_north_edits,
    SUM(IF (NOT bot, edit_count, 0)) AS global_north_nonbot_edits,
    SUM(CAST(
        namespace_zero_edit_count >= 5
        AND NOT bot
    AS INT)) AS global_north_active_editors
FROM gs_editors
