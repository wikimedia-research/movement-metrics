import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re
import calendar
from datetime import date
from wikicharts import Wikichart
from wikicharts import wmf_colors


#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Content_Interactions.png"
save_file_name = "charts/" + outfile_name
yoy_note = input('YoY annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/reader_metrics.tsv', sep='\t')
corrected_df = pd.read_csv('../data/corrected_metrics.csv')

#display top rows for preview
#df.iloc[0,:] 

#---CLEAN DATA--
#print out data types
#print(df.month.dtype)
#print(df.interactions.dtype)
#print(df.interactions_corrected.dtype)

start_date = "2018-05-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#remove commas
corrected_df["interactions"] = corrected_df["interactions"].str.replace(",","")
corrected_df["interactions_corrected"] = corrected_df["interactions_corrected"].str.replace(",","")

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])
corrected_df['month'] = pd.to_datetime(corrected_df['month'])

#truncate to preferred date range
df = df[df["month"].isin(pd.date_range(start_date, end_date))]
corrected_df = corrected_df[corrected_df["month"].isin(pd.date_range(start_date, end_date))]

#convert to int
corrected_df['interactions'] = corrected_df['interactions'].astype(str).astype(float)
corrected_df['interactions_corrected'] = corrected_df['interactions_corrected'].astype(str).astype(float)

#combine datasets — add corrected values to the reader metrics dataset
df['interactions_corrected'] = df['interactions']
correction_range = pd.date_range(start='2021-05-01', end='2022-02-01', freq='MS')
for m in correction_range:
	row_index = df[df['month'] == m].index 
	correct_row = corrected_df.loc[corrected_df['month'] ==  m]
	df.loc[row_index, 'interactions_corrected'] = correct_row['interactions_corrected']

#create subsets of data for easier plotting
data_loss_df = df[df["month"].isin(pd.date_range("2021-05-01", "2022-02-01"))]

#---MAKE CHART---
chart = Wikichart(start_date,end_date,month_interest,df)
chart.init_plot()
chart.plot_data_loss('month','interactions','interactions_corrected')
chart.plot_line('month','interactions_corrected',wmf_colors['blue'])
chart.plot_monthlyscatter('month','interactions_corrected',wmf_colors['blue'])
chart.plot_yoy_highlight('month','interactions_corrected')
chart.format(title = f'Content Interactions ({month_name})',
	radjust=0.87,
	y_order=1e-9,
	y_label_format='{:1.0f}B',
	author="Hua Xi",
	data_source="https://github.com/wikimedia-research/Reader-movement-metrics")
chart.annotate(x='month',
	y='interactions_corrected',
	num_annotation=chart.calc_yoy(y='interactions_corrected'),
	legend_label='',
	xpad=0,
	ypad=0)
chart.finalize_plot(save_file_name)