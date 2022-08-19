with gs_new_editors as (
    select 
        1st_month_edits,
        2nd_month_edits
    from wmf_product.new_editors ne
    left join wmf.editors_daily gd
    on
        ne.user_id = gd.user_fingerprint_or_name and
        ne.wiki = gd.wiki_db and
        ne.cohort = gd.month
    left join canonical_data.countries cdc
    on gd.country_code = cdc.iso_code
    where
        ne.cohort = "{retention_cohort}" and
        gd.month = "{retention_cohort}" and
        economic_region = "Global South"
    group by user_name, wiki, 1st_month_edits, 2nd_month_edits
)
select
    "{metrics_month_first_day}" as month,
    sum(cast(2nd_month_edits >= 1 as int)) / count(*) as global_south_new_editor_retention 
from gs_new_editors