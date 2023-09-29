WITH mh_editors AS (
    SELECT
        COUNT(*) AS edits,
        SUM(CAST(page_namespace_is_content_historical AS INT)) AS content_edits,
        MAX(
            SIZE (event_user_is_bot_by) > 0
            OR SIZE (event_user_is_bot_by_historical) > 0
        ) AS bot
    FROM wmf.mediawiki_history mh
    INNER JOIN canonical_data.mobile_heavy_wikis mhw
    ON mh.wiki_db = mhw.database_code
    WHERE
        event_timestamp BETWEEN '{metrics_month_start}' AND '{metrics_month_end}'
        AND NOT event_user_is_anonymous
        AND snapshot = '{mediawiki_history_snapshot}'
        AND event_entity = 'revision'
        AND event_type = 'create'
    GROUP BY event_user_text
)
SELECT
    '{metrics_month_first_day}' AS month,
    SUM(edits) AS `mobile-heavy_wiki_edits`,
    SUM(IF(NOT bot, edits, 0)) AS `mobile-heavy_wiki_nonbot_edits`,
    SUM(CAST(content_edits >= 5 AS INT)) AS `mobile-heavy_wiki_active_editors`
FROM mh_editors
