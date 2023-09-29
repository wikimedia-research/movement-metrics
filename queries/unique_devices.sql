WITH a AS (
    SELECT
        year,
        month,
        uniques_estimate AS unique_devices
    FROM wmf.unique_devices_per_project_family_monthly
    WHERE
        year >= 2014
        AND project_family = 'wikipedia'
) a
SELECT
    CONCAT(year, '-', LPAD(month, 2, '0'), '-01') AS month,
    SUM(unique_devices) AS unique_devices
FROM a
WHERE
    year = {metrics_year}
    AND month = {metrics_cur_month}
GROUP BY CONCAT(year, '-', LPAD(month, 2, '0'), '-01')
LIMIT 1000
