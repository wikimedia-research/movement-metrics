import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import re
import calendar
from datetime import date
from wikicharts import Wikichart
from wikicharts import wmf_colors

#to do
#programmatize yorder and ylabelformatter
#remove repetitive yoy_highlight dataframe making

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Net_New.png"
save_file_name = "charts/" + outfile_name
yoy_note = input('YoY annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/editor_metrics.tsv', sep='\t')

#display top rows for preview
#df.head()
#df.iloc[0,:]

#---CLEAN DATA--
#print out data types
#print(df.month.dtype)
#print(df.net_new_Commons_content_pages.dtype)
#print(df.net_new_Wikidata_entities.dtype)
#print(df.net_new_Wikipedia_articles.dtype)
#print(df.net_new_content_pages.dtype)

start_date = "2018-05-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#truncate to preferred date range
df = df[df["month"].isin(pd.date_range(start_date, end_date))]

#---PREPARE TO PLOT
key = pd.DataFrame([['Commons',wmf_colors['pink']],
	['Wikidata',wmf_colors['brightgreen']],
	['Wikipedia',wmf_colors['purple']]],
	index=['net_new_Commons_content_pages','net_new_Wikidata_entities','net_new_Wikipedia_articles'],
	columns=['labelname','color'])

#---MAKE CHART---
chart = Wikichart(start_date,end_date,month_interest,df)
chart.init_plot(width=12)
chart.plot_line('month','net_new_Commons_content_pages',key.loc['net_new_Commons_content_pages','color'])
chart.plot_line('month','net_new_Wikidata_entities',key.loc['net_new_Wikidata_entities','color'])
chart.plot_line('month','net_new_Wikipedia_articles',key.loc['net_new_Wikipedia_articles','color'])

chart.plot_monthlyscatter('month','net_new_Commons_content_pages',key.loc['net_new_Commons_content_pages','color'])
chart.plot_monthlyscatter('month','net_new_Wikidata_entities',key.loc['net_new_Wikidata_entities','color'])
chart.plot_monthlyscatter('month','net_new_Wikipedia_articles',key.loc['net_new_Wikipedia_articles','color'])

chart.format(title = f'Net New Content ({month_name})',
	y_order=1e-6,
	y_label_format='{:1.1f}M',
	radjust=0.75,
	author="Hua Xi",
	data_source="https://github.com/wikimedia-research/Editing-movement-metrics")

chart.multi_yoy_annotate(['net_new_Commons_content_pages','net_new_Wikidata_entities','net_new_Wikipedia_articles'],key)

chart.finalize_plot(save_file_name)
