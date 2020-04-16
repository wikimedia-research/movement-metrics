with gs_new_editors as (
    select 
        1st_month_edits,
        2nd_month_edits
    from cchen.new_editor_retention ne
    left join wmf.editors_daily gd
    on
        ne.user_id = gd.user_fingerprint_or_id and
        ne.wiki = gd.wiki_db and
        ne.cohort = gd.month
    left join canonical_data.countries cdc
    on gd.country_code = cdc.iso_code
    where
        ne.cohort = "{retention_cohort}" and
        gd.month = "{retention_cohort}" and
        economic_region = "Global North"
    group by user_name, wiki, 1st_month_edits, 2nd_month_edits
)
select
    "{metrics_month_first_day}" as month,
    sum(cast(2nd_month_edits >= 1 as int)) / count(*) as global_north_new_editor_retention 
from gs_new_editors