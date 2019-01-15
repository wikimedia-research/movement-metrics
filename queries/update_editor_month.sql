insert into staging.editor_month
select
    database() as wiki,
    str_to_date(concat(month, "01"), "%Y%m%d") as month,
    local_user_id,
    ifnull(user_name, "") as user_name,
    count(*) as edits,
    ifnull(sum(page_namespace = 0 or cn.namespace is not null), 0) as content_edits,
    ifnull(sum(deleted), 0) as deleted_edits,
    ifnull(sum(platform = "web"), 0) as mobile_web_edits,
    ifnull(sum(platform = "app"), 0) as mobile_app_edits,
    ifnull(sum(interface = "ve"), 0) as visual_edits,
    ifnull(sum(interface = "ve source"), 0) as ve_source_edits,
    if(ug_group = "bot" or ufg_group = "bot", 1, 0) as bot_flag,
    str_to_date(user_registration, "%Y%m%d%H%i%S") as user_registration
from ( 
    select
        left(rev_timestamp, 6) as month,
        rev_user as local_user_id,
        page_namespace,
        case 
            when sum(ctd_name = "mobile app edit") = 1
                then "app"
            when sum(ctd_name = "mobile web edit" or ctd_name = "mobile_edit") = 1
                then "web"
            else null
        end as platform,
        case
            when sum(ctd_name = "visualeditor-wikitext") = 1
                then "ve source"
            -- we want to catch "visualeditor-switched" in addition to "visual-editor"
            when sum(ctd_name like "visualeditor%") >= 1
                then "ve"
            else null
        end as interface,
        0 as deleted
    from revision
    left join page on rev_page = page_id
    left join change_tag on ct_rev_id = rev_id
    left join change_tag_def on ct_tag_id = ctd_id
    where
        rev_timestamp between "{start}" and "{end}"
    group by rev_id
    
    union all
    
    select
        left(ar_timestamp, 6) as month,
        ar_user as local_user_id,
        ar_namespace as page_namespace,
        case 
            when sum(ctd_name = "mobile app edit") = 1
                then "app"
            when sum(ctd_name = "mobile web edit" or ctd_name = "mobile_edit") = 1
                then "web"
            else null
        end as platform,
        case
            when sum(ctd_name = "visualeditor-wikitext") = 1
                then "ve source"
            when sum(ctd_name like "visualeditor%") >= 1
                then "ve"
            else null
        end as interface,
        1 as deleted
    from archive
    left join change_tag on ct_rev_id = ar_rev_id
    left join change_tag_def on ct_tag_id = ctd_id
    where
        ar_timestamp between "{start}" and "{end}"
    group by ar_rev_id
) tagged_revs
left join user on local_user_id = user_id
left join staging.content_namespaces cn on database() = wiki and tagged_revs.page_namespace = cn.namespace
left join user_groups on local_user_id = ug_user and ug_group = "bot"
left join user_former_groups on local_user_id = ufg_user and ufg_group = "bot"
group by month, local_user_id;