import pandas as pd
import datetime
from math import ceil
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
import path
import getopt
import sys
import os
from os.path import dirname
sys.path.append('../')
from wikicharts import Wikichart
from wikicharts import wmf_colors
from wikicharts import split_df_by_col
from wikicharts import gen_keys

def main(argv):
	print("Generating Regional Unique Devices chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Regional_Unique_Devices"
	yoy_note = " "
	display_flag = True
	if len(opts) > 0:
		for opt in opts[0]:
			if opt == '-p':
				outfile_name = input('Outfile_name:\n')
				yoy_note = input('YoY annotation note (default is blank):\n')
			elif opt == '-i':
				display_flag = False
	save_file_name1 = dirname(script_directory) + "/charts/" + outfile_name + "_1.jpeg"
	save_file_name2 = dirname(script_directory) + "/charts/" + outfile_name + "_2.jpeg"

	#---CLEAN DATA--
	data_directory = dirname(dirname(script_directory))
	df = pd.read_csv(data_directory + '/data/regional_reader_metrics.csv')

	#note start and end dates may be different depending on chart_type
	start_date = "2018-01-01"
	end_date = datetime.datetime.today()
	block_off_start = datetime.datetime.strptime("2021-01-01", '%Y-%m-%d')
	block_off_end = datetime.datetime.strptime("2022-07-01", '%Y-%m-%d')

	#convert string to datetime
	df['month'] = pd.to_datetime(df['month'])

	#truncate data to period of interst
	df = df[df["month"].isin(pd.date_range(start_date, end_date))]

	#get max and min for setting subplot yaxis limits
	'''
	data_min = df["unique_devices"].min()
	data_max = df["unique_devices"].max()
	ymin = data_min
	ymax = data_max
	#ymin = data_min - (data_max - data_min / 4)
	#ymax = data_max + (data_max - data_min / 4)
	'''

	#pivot to make regions separate columns
	df = df.pivot(index='month', columns='region', values='unique_devices').reset_index()

	#sort columns by total
	#add a Totals row at bottom
	df.loc['Total'] = df.iloc[:, :-1].sum()
	#sort columns left to right for highest to lowest totals
	df = df.sort_values('Total', axis=1, ascending=False)
	#print Totals row (sorted)
	#delete Totals row
	df = df.iloc[:-1]
	df = df.rename(columns={np.nan: "Unknown",'UNCLASSED':"Unclassed"})
	print(df.columns)

	#divide into sets of four
	dfs = split_df_by_col(df)

	#generate keys that correspond each region to a diff color
	key_colors = [wmf_colors['red'], wmf_colors['orange'], wmf_colors['yellow'], wmf_colors['green'], wmf_colors['purple'], wmf_colors['blue'], wmf_colors['pink'], wmf_colors['black50'], wmf_colors['brightblue'],wmf_colors['red']]
	keys = gen_keys(dfs, key_colors)

	#---MAKE CHART---
	#annotation to explain boxes
	annotation_text = "     Data unreliable [February 2021 - June 2022] (period not shown)" #or use /// instead of rectangle patch
	#make charts
	total_num_charts = len(df.columns) - 1
	charts_per_figure = 4
	num_figures = ceil(total_num_charts / charts_per_figure)
	charts = [None]*num_figures
	#max range across figures
	maxranges = [None]*num_figures 
	num_ticks = [None]*num_figures
	#initialize each figure
	for f in range(num_figures):
		figure_num_charts = len(dfs[f].columns) - 1
		charts[f] = Wikichart(start_date,end_date,dfs[f])
		charts[f].init_plot(width=12,subplotsx=2,subplotsy=2,fignum=f)
		charts[f].plot_subplots_lines('month', keys[f], num_charts=figure_num_charts)
		maxranges[f], num_ticks[f] = charts[f].get_maxyrange()
	#calculate the largest range between the two figures and 8 subplots
	maxrange = max(maxranges)
	maxrange_index = maxranges.index(maxrange)
	maxrange_numticks = num_ticks[maxrange_index]
	#format and display each figure
	for f in range(num_figures):
		plt.figure(f)
		figure_num_charts = len(dfs[f].columns) - 1
		#charts[f].standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=figure_num_charts)
		charts[f].block_off_multi(block_off_start,block_off_end)
		charts[f].add_block_legend()
		charts[f].format_subplots(title = 'Regional Unique Devices',
			key = keys[f],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			tadjust=0.8, badjust=0.1,
			num_charts=figure_num_charts)
		charts[f].top_annotation(annotation_text = annotation_text)
		#save chart1 but set display to False because plt.show() will show all figures at once
		save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_0" + str(f) + ".jpeg"
		charts[f].finalize_plot(save_file_name,display=False)
	#plt.show()

	#---GENERATE INDIVIDUAL CHARTS---
	individual_charts = [None]*total_num_charts
	columns = list(df.columns)
	columns.remove('month')
	for c in range(len(columns)):
		current_fignum = num_figures + c + 1
		current_col = columns[c]
		current_df = df[['month', current_col]]
		current_savefile = dirname(script_directory) + "/charts/individual_" + outfile_name + "_" + str(c) + ".jpeg"
		individual_charts[c] = Wikichart(start_date,end_date,current_df)
		individual_charts[c].init_plot(fignum=current_fignum)
		individual_charts[c].plot_line('month',current_col,key_colors[c])
		individual_charts[c].plot_monthlyscatter('month',current_col,col =key_colors[c])
		individual_charts[c].plot_yoy_highlight('month',current_col)
		current_yrange = individual_charts[c].get_ytickrange()
		if current_yrange > (maxrange / 8):
			individual_charts[c].standardize_yrange(maxrange, maxrange_numticks)
		individual_charts[c].format(title = f'Unique Devices: {current_col}',
			ybuffer=False,
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			tadjust=0.825,badjust=0.125,
			titlepad=25)
		individual_charts[c].annotate(x='month',
			y=current_col,
			num_annotation=individual_charts[c].calc_yoy(y=current_col,yoy_note=yoy_note))
		individual_charts[c].finalize_plot(current_savefile,display=False)


if __name__ == "__main__":
	main(sys.argv[1:])
