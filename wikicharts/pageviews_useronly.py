import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re
from datetime import date
from matplotlib.patches import Ellipse
import matplotlib.dates as mdates
import calendar
from wikicharts import Wikichart
from wikicharts import wmf_colors


#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Monthly_User_Pageviews_Wikipedia.png"
save_file_name = "charts/" + outfile_name
note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/monthly_pageviews.csv')

#display top rows for preview
#df.head()

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

start_date = "2020-07-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by='timestamp')

#truncate to preferred date range
df = df[df["timestamp"].isin(pd.date_range(start_date, end_date))]


#---PLOT---
chart = Wikichart(start_date,end_date,month_interest,df)
chart.init_plot(width=12)
chart.plot_line('timestamp','pageviews_corrected',wmf_colors['blue'])
chart.plot_monthlyscatter('timestamp','pageviews_corrected',wmf_colors['blue'])
chart.plot_yoy_highlight('timestamp','pageviews_corrected')
chart.format(title = f'Monthly User Pageviews to Wikipedia ({month_name})',
	y_order=1e-9,
	y_label_format='{:1.1f}B',
	radjust=0.825,
	tadjust=0.85,
	badjust=0.15,
	author="Hua Xi",
	data_source="https://docs.google.com/spreadsheets/d/1YfKmAe6ViAIjnPejYEq6yCkuYa8QK8-h6VxsAlbnNGA")
chart.annotate(x='timestamp',
	y='sum_view_count',
	num_annotation=chart.calc_yoy(y='pageviews_corrected'),
	legend_label='',
	xpad=0, 
	ypad=0)
chart.finalize_plot(save_file_name)