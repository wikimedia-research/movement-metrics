WITH bydatecountry AS (
    SELECT
        year,
        month,
        day,
        CONCAT(
            year,
            '-',
            LPAD(month, 2, '0'),
            '-',
            LPAD(day, 2, '0')
        ) AS DATE,
        country_code,
        SUM(view_count) AS previews_seen_country
    FROM wmf.virtualpageview_hourly
    WHERE year >= 2019
    GROUP BY
        year,
        month,
        day,
        country_code
)
SELECT
    CONCAT(year, '-', month, '-01') AS month,
    SUM(previews_seen_country) AS gs_previews
FROM bydatecountry
JOIN canonical_data.countries countries
ON bydatecountry.country_code = countries.iso_code
WHERE
    countries.economic_region = 'Global South'
    AND year = {metrics_year}
    AND month = {metrics_cur_month}
GROUP BY CONCAT(year, '-', month, '-01')
LIMIT 10000
