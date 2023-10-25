SELECT
    day AS month,
    SUM(uniques_estimate) AS unique_devices
FROM wmf_readership.unique_devices_per_project_family_monthly
WHERE
    day = '{metrics_month_first_day}'
    AND project_family = 'wikipedia'
GROUP BY day
