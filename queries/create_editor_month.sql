CREATE TABLE IF NOT EXISTS neilpquinn.editor_month (
  `month` TIMESTAMP, -- Hive 1.1 does not support the DATE type
  `wiki_db` STRING,
  `local_user_id` BIGINT,
  `user_name` STRING,
  `edits` BIGINT,
  `content_edits` BIGINT,
  `mobile_web_edits` BIGINT,
  `mobile_app_edits` BIGINT,
  `visual_edits` BIGINT,
  `ve_source_edits` BIGINT,
  `bot` BOOLEAN,
  `user_registration` TIMESTAMP
) 
STORED AS PARQUET