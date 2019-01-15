insert into staging.editor_month
select
  database() as wiki,
  str_to_date(concat(rev_month, "01"), "%Y%m%d") as month,
  local_user_id,
  ifnull(user_name, "") as user_name,
  ifnull(sum(edits), 0) as edits,
  ifnull(sum(content_edits), 0) as content_edits,
  ifnull(sum(edits * deleted), 0) as deleted_edits,
  ifnull(sum(mobile_web_edits), 0) as mobile_web_edits,
  ifnull(sum(mobile_app_edits), 0) as mobile_app_edits,
  ifnull(sum(visual_edits), 0) as visual_edits,
  ifnull(sum(ve_source_edits), 0) as ve_source_edits,
  if(ug_group = "bot" or ufg_group = "bot", 1, 0) as bot_flag,
  str_to_date(user_registration, "%Y%m%d%H%i%S") as user_registration
from
(
select
  left(rev_timestamp, 6) as `rev_month`,
  rev_user as `local_user_id`,
  count(*) as `edits`,
  sum(page_namespace = 0 or cn.namespace is not null) as content_edits,
  sum(
    ts_tags like "%mobile edit%" and
    (ts_tags like "%mobile web edit%" or ts_tags not like "%mobile app edit%")
  ) as mobile_web_edits,
  sum(ts_tags like "%mobile app edit%") as mobile_app_edits,
  sum(ts_tags like "%visualeditor%" and ts_tags not like "%visualeditor-wikitext%") as visual_edits,
  sum(ts_tags like "%visualeditor-wikitext%") as ve_source_edits,
  0 as `deleted`
from revision
left join page on rev_page = page_id
left join (
    select
        ct_rev_id as ts_rev_id,
        group_concat(ctd_name) as ts_tags
    from change_tag
    left join change_tag_def
    on ct_tag_id = ctd_id
    group by ts_rev_id
) tag_summary on rev_id = ts_rev_id
left join staging.content_namespaces cn on database() = wiki and page_namespace = namespace
where rev_timestamp between "{start}" and "{end}"
group by left(rev_timestamp, 6), rev_user

union all

select
  left(ar_timestamp, 6) as `rev_month`,
  ar_user as `local_user_id`,
  count(*) as `edits`,
  sum(ar_namespace = 0 or cn.namespace is not null) as content_edits,
  sum(
    ts_tags like "%mobile edit%" and
    (ts_tags like "%mobile web edit%" or ts_tags not like "%mobile app edit%")
  ) as mobile_web_edits,
  sum(ts_tags like "%mobile app edit%") as mobile_app_edits,
  sum(ts_tags like "%visualeditor%" and ts_tags not like "%visualeditor-wikitext%") as visual_edits,
  sum(ts_tags like "%visualeditor-wikitext%") as ve_source_edits,
  1 as `deleted`
from archive
left join (
    select
        ct_rev_id as ts_rev_id,
        group_concat(ctd_name) as ts_tags
    from change_tag
    left join change_tag_def
    on ct_tag_id = ctd_id
    group by ts_rev_id
) tag_summary on ar_rev_id = ts_rev_id
left join staging.content_namespaces cn on database() = wiki and ar_namespace = namespace
where ar_timestamp between "{start}" and "{end}"
group by left(ar_timestamp, 6), ar_user
) revs
left join user on local_user_id = user_id
left join user_groups on local_user_id = ug_user and ug_group = "bot"
left join user_former_groups on local_user_id = ufg_user and ufg_group = "bot"
group by month, local_user_id;