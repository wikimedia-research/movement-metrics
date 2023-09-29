WITH edits AS (
    SELECT
        event_timestamp,
        (
            ARRAY_CONTAINS(revision_tags, 'mobile edit')
            OR ARRAY_CONTAINS(revision_tags, 'mobile app edit')
            OR ARRAY_CONTAINS(revision_tags, 'mobile web edit')
        ) AS mobile_edit,
        SIZE (event_user_is_bot_by) = 0
            AND SIZE (event_user_is_bot_by_historical) = 0 AS nonbot_edit,
        (
            wiki_db = 'wikidatawiki'
            AND page_namespace_historical IN (0, 120)
        ) AS data_edit,
        revision_is_identity_reverted AS reverted,
        event_user_is_anonymous AS anonymous,
        (
            revision_parent_id = 0
            AND page_namespace_historical = 6
        ) AS upload
    FROM wmf.mediawiki_history
    WHERE
        event_entity = 'revision'
        AND event_type = 'create'
        AND event_timestamp BETWEEN '{metrics_month_start}' AND '{metrics_month_end}'
        AND snapshot = '{mediawiki_history_snapshot}'
)
SELECT
    DATE_FORMAT(event_timestamp, 'yyyy-MM-01') AS month,
    COUNT(*) AS total_edits,
    SUM(CAST(upload AS INT)) AS uploads,
    SUM(CAST(mobile_edit AS INT)) AS mobile_edits,
    SUM(CAST(data_edit AS INT)) AS wikidata_edits,
    SUM(CAST(
        nonbot_edit
        AND NOT data_edit
        AND NOT upload
        AND NOT mobile_edit
    AS INT)) AS other_nonbot_edits,
    SUM(CAST(anonymous AS INT)) AS anonymous_edits,
    SUM(CAST(NOT anonymous AS INT)) AS non_anonymous_edits,
    SUM(CAST(reverted AS INT)) / SUM(CAST(nonbot_edit AS INT)) AS revert_rate
FROM edits
GROUP BY DATE_FORMAT(event_timestamp, 'yyyy-MM-01')
