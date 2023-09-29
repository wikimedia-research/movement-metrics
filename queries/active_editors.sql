SELECT
    month,
    COUNT(*) AS active_editors,
    SUM(CAST(registration_month = month AS INT)) AS new_active_editors,
    COUNT(*) - SUM(CAST(registration_month = month AS INT)) AS returning_active_editors
FROM
    (
        SELECT
            CAST(month AS DATE) AS month,
            user_name,
            SUM(content_edits) AS content_edits,
            MAX(bot_by_group) AS bot_by_group,
            CAST(TRUNC(MIN(user_registration), 'MONTH') AS DATE) AS registration_month
        FROM wmf_product.editor_month
        WHERE
            MONTH = '{metrics_month_first_day}'
            AND user_id != 0
        GROUP BY
            month,
            user_name
    ) global_edits
WHERE
    content_edits >= 5
    AND NOT bot_by_group
    AND user_name NOT REGEXP 'bot\\b'
GROUP BY month
