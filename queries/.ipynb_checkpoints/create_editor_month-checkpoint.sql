CREATE TABLE IF NOT EXISTS neilpquinn.editor_month (
  `month` TIMESTAMP, -- Hive 1.1 does not support the DATE type
  `wiki` STRING,
  `user_id` BIGINT,
  `user_name` STRING,
  `edits` BIGINT,
  `content_edits` BIGINT,
  `mobile_web_edits` BIGINT,
  `mobile_app_edits` BIGINT,
  `visual_edits` BIGINT,
  `2017_wikitext_edits` BIGINT,
  `bot_by_group` BOOLEAN, -- This should just be `bot` since this field is based on both group and name
  `user_registration` TIMESTAMP
) 
STORED AS PARQUET
