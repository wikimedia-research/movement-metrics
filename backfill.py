import pandas as pd
import datetime
from wmfdata import charting, hive, spark

#hive.run(
#"""
#CREATE EXTERNAL TABLE IF NOT EXISTS florez.test_1_new_editors ( 
#    `user_name` string, 
#    `wiki` string, 
#    `user_id` bigint, 
#    `1st_month_edits` bigint, 
#    `2nd_month_edits` bigint  
#) 
#PARTITIONED BY (`cohort` string) 
#STORED AS PARQUET
#"""
#)

#add --INSERT INTO TABLE florez.test_1_new_editors
#overwrite

NED = '''
    INSERT OVERWRITE TABLE wmf_product.new_editors
    PARTITION(cohort= '{cohort}')

    SELECT user_name, wiki, user_id, 1st_month_edits, 2nd_month_edits
    FROM cchen.new_editors
    WHERE cohort = '{cohort}'
'''

# one year of data
for n in range(1, 13):
    dtime = datetime.datetime(2016, n, 1)
    METRICS_MONTH_TEXT = dtime.strftime("%Y-%m") 
    spark.run(NED.format(cohort = METRICS_MONTH_TEXT))