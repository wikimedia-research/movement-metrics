import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re
import calendar
from datetime import date
import wikicharts
from wikicharts import Wikichart
from wikicharts import wmf_colors

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Active_Editors.png"
save_file_name = "charts/" + outfile_name
yoy_note = input('YoY annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/editor_metrics.tsv', sep='\t')

#display top rows for preview
#df.iloc[0,:] 

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

start_date = "2019-01-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#truncate data to period of interst
df = df[df["month"].isin(pd.date_range(start_date, end_date))]

#---MAKE CHART---
chart = Wikichart(start_date,end_date,month_interest,df)
chart.init_plot()
chart.plot_line('month','active_editors',wmf_colors['blue'])
chart.plot_monthlyscatter('month','active_editors',wmf_colors['blue'])
chart.plot_yoy_highlight('month','active_editors',wmf_colors['yellow'])
chart.format(title = f'Active Editors ({month_name})',
	y_order=1e-3,
	y_label_format='{:1.0f}K',
	author="Hua Xi",
	data_source="https://github.com/wikimedia-research/Editing-movement-metrics")
chart.annotate(x='month',
	y='active_editors',
	num_annotation=chart.calc_yoy(y='active_editors',yoy_note=yoy_note),
	legend_label='',
	xpad=0, 
	ypad=0)
chart.finalize_plot(save_file_name)