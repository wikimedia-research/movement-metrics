WITH global_user_registration AS (
    SELECT
        user_name,
        MIN(CAST(TRUNC(user_registration, 'MONTH') AS DATE)) AS global_registration_month
    FROM wmf_product.editor_month
    WHERE
        user_id != 0
        AND NOT bot_by_group
        AND user_name NOT REGEXP 'bot\\b'
    GROUP BY
        user_name
),
aggregated_edits AS (
    SELECT
        e.month,
        e.user_name,
        SUM(e.content_edits) AS content_edits,
        g.global_registration_month
    FROM wmf_product.editor_month e
    INNER JOIN global_user_registration g ON e.user_name = g.user_name
    WHERE
        e.MONTH = '{metrics_month_first_day}'
        AND e.user_id != 0
        AND NOT e.bot_by_group
        AND e.user_name NOT REGEXP 'bot\\b'
    GROUP BY
        e.month,
        e.user_name,
        g.global_registration_month
)
SELECT
    month,
    COUNT(*) AS active_editors,
    SUM(CAST(global_registration_month = CAST(month AS DATE) AS INT)) AS new_active_editors,
    COUNT(*) - SUM(CAST(global_registration_month = CAST(month AS DATE) AS INT)) AS returning_active_editors
FROM
    aggregated_edits
WHERE
    content_edits >= 5
    AND global_registration_month  = '{metrics_month_first_day}'
GROUP BY month


