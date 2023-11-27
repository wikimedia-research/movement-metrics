SELECT 
    content_gap,
    category as category,
    trunc(CAST(dt AS TIMESTAMP), 'MM') AS month,
    SUM(standard_quality_count) AS standard_quality_count_value
FROM
    (
    SELECT 
        FROM_UNIXTIME(UNIX_TIMESTAMP(time_bucket, 'yyyy-MM'), 'yyyy-MM-dd') as dt,
        category,
        content_gap,
        metrics.article_created,
        metrics.pageviews_sum,
        metrics.pageviews_mean,
        metrics.standard_quality,
        metrics.standard_quality_count,
        metrics.quality_score,
        metrics.revision_count
    FROM content_gap_metrics.by_category_all_wikis
    ) AS virtual_table
WHERE 
    dt >= TIMESTAMP '2022-10-25 19:03:11.000000'
    AND (content_gap = 'gender' or content_gap = 'geography_wmf_region')
GROUP BY category,content_gap,
    trunc(CAST(dt AS TIMESTAMP), 'MM')
ORDER BY "SUM(standard_quality_count)" DESC
LIMIT 50000;
