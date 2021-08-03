INSERT INTO wmf_product.editor_month
select
    trunc(event_timestamp, "MONTH") as month,
    wiki_db as wiki,
    event_user_id as user_id,
    max(event_user_text) as user_name, -- Some rows incorrectly have a null `event_user_text` (T218463)
    count(*) as edits,
    coalesce(sum(ns_map.namespace_is_content), 0) as content_edits,
    SUM(CAST(ARRAY_CONTAINS(revision_tags, "mobile web edit") AS INT)) AS mobile_web_edits,
    SUM(CAST(ARRAY_CONTAINS(revision_tags, "mobile app edit") AS INT)) AS mobile_app_edits,
    SUM(CAST(ARRAY_CONTAINS(revision_tags, "visualeditor") AS INT))  AS visual_edits,
    SUM(CASE WHEN wiki_db = "wikidatawiki" AND page_namespace_historical in (0, 120) THEN 1 END) AS data_edits,
    NULL as `2017_wikitext_edits`,
    max(size(event_user_is_bot_by) > 0 or size(event_user_is_bot_by_historical) > 0) as bot_by_group,
    min(event_user_creation_timestamp) as user_registration
from wmf.mediawiki_history mwh
inner join canonical_data.wikis 
on
    wiki_db = database_code and
    database_group in (
        "commons", "incubator", "foundation", "mediawiki", "meta", "sources", 
        "species","wikibooks", "wikidata", "wikinews", "wikipedia", "wikiquote",
        "wikisource", "wikiversity", "wikivoyage", "wiktionary"
    )
left join wmf_raw.mediawiki_project_namespace_map ns_map -- Avoid `page_namespace_is_content` to work around T221338
on
    wiki_db = dbname and
    coalesce(page_namespace_historical, page_namespace) = namespace and
    ns_map.snapshot = "{mwh_snapshot}" and
    mwh.snapshot = "{mwh_snapshot}"

where
    event_timestamp between "{start}" and "{end}" and
    event_entity = "revision" and
    event_type = "create" and
    mwh.snapshot = "{mwh_snapshot}"
group by
    trunc(event_timestamp, "MONTH"),
    wiki_db,
    event_user_id