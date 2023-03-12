import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
import re
import calendar
from datetime import date
from wikicharts import Wikichart
from wikicharts import wmf_colors

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Project_Growth_Chart.png"
save_file_name = "charts/" + outfile_name
yoy_note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA---
df_wikidata = pd.read_csv('../data/wikidata_growth.csv')
df_wikipedia = pd.read_csv('../data/wikipedia_growth.csv')
df_commons = pd.read_csv('../data/commons_growth.csv')

#display top rows for preview
#df.iloc[0,:] 

#---CLEAN DATA--
#print out data types
#print(df.month.dtype)

start_date = "2014-01-01"
end_date = "2023-01-01"
month_interest = 12
month_name = calendar.month_name[month_interest]

#convert string to datetime
df_wikidata['month'] = df_wikidata['month'].apply(lambda x: x.rsplit("T")[0])
df_wikipedia['month'] = df_wikipedia['month'].apply(lambda x: x.rsplit("T")[0])
df_commons['month'] = df_commons['month'].apply(lambda x: x.rsplit("T")[0])
df_wikidata['month'] = pd.to_datetime(df_wikidata['month'])
df_wikipedia['month'] = pd.to_datetime(df_wikipedia['month'])
df_commons['month'] = pd.to_datetime(df_commons['month'])

#change column names
df_wikidata = df_wikidata.rename(columns={'total.content':'wikidata'})
df_wikipedia = df_wikipedia.rename(columns={'total.content':'wikipedia'})
df_commons = df_commons.rename(columns={'total.content':'commons'})

#drop unneeded columns
df_wikidata = df_wikidata.drop(columns=['timeRange.start', 'timeRange.end'])
df_wikipedia = df_wikipedia.drop(columns=['timeRange.start', 'timeRange.end'])
df_commons = df_commons.drop(columns=['timeRange.start', 'timeRange.end'])

#merge into one dataframe
df = pd.merge(pd.merge(df_wikidata,df_wikipedia,on='month'),df_commons,on='month')

#truncate date
df = df[df["month"].isin(pd.date_range(start_date, end_date))]

#---PREPARE TO PLOT
key = pd.DataFrame([['Wikidata',wmf_colors['pink']],
	['Wikipedia',wmf_colors['yellow']],
	['Commons',wmf_colors['orange']]],
	index=['wikidata','wikipedia','commons'],
	columns=['labelname','color'])

#---PLOT---
chart = Wikichart(start_date,end_date,month_interest,df)
chart.init_plot(width=12)
chart.plot_line('month','wikidata',key.loc['wikidata','color'],linewidth=4)
chart.plot_line('month','wikipedia',key.loc['wikipedia','color'])
chart.plot_line('month','commons',key.loc['commons','color'])
chart.format(title = f'Growth of Wikimedia Projects: Content Items',
	y_order=1e-6,
	y_label_format='{:1.0f}M',
	radjust=0.75,
	author="Hua Xi",
	data_source="https://stats.wikimedia.org")

chart.multi_yoy_annotate(['wikidata','wikipedia','commons'],key,chart.calc_finalcount)

chart.finalize_plot(save_file_name)