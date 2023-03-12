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
outfile_name = input('Outfile_name:\n') or "New_Returning.png"
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

start_date = "2019-01-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#truncate to preferred date range
df = df[df["month"].isin(pd.date_range(start_date, end_date))]

#---PREPARE TO PLOT
key = pd.DataFrame([['Returning',wmf_colors['blue']],
	['New',wmf_colors['green50']]],
	index=['returning_active_editors','new_active_editors'],
	columns=['labelname','color'])

#---MAKE CHART---
chart = Wikichart(start_date,end_date,month_interest,df)
chart.init_plot(width=12)
chart.plot_line('month','returning_active_editors',key.loc['returning_active_editors','color'])
chart.plot_line('month','new_active_editors',key.loc['new_active_editors','color'])
chart.plot_monthlyscatter('month','returning_active_editors',key.loc['returning_active_editors','color'])
chart.plot_monthlyscatter('month','new_active_editors',key.loc['new_active_editors','color'])
chart.format(title = f'New and Returning Editors ({month_name})',
	y_order=1e-3,
	y_label_format='{:1.0f}K',
	radjust=0.75,
	author="Hua Xi",
	data_source="https://github.com/wikimedia-research/Editing-movement-metrics")

chart.multi_yoy_annotate(['returning_active_editors','new_active_editors'],key)

chart.finalize_plot(save_file_name)