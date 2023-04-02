import pandas as pd
import datetime
from math import ceil
import matplotlib.pyplot as plt
import matplotlib.font_manager
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
	print("Generating Regional Active Editors chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Regional_Active_Editors"
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
	df = pd.read_csv(data_directory + '/data/regional_editor_metrics.csv')

	#note start and end dates may be different depending on chart_type
	start_date = "2018-01-01"
	end_date = datetime.datetime.today()

	#convert string to datetime
	df['month'] = pd.to_datetime(df['month'])

	#truncate data to period of interst
	df = df[df["month"].isin(pd.date_range(start_date, end_date))]

	#fill in NaNs with blanks
	df = df.fillna('')

	#pivot to make regions separate columns
	df = df.pivot(index='month', columns='region', values='monthly_editors').reset_index()

	#sort columns by total
	#add a Totals row at bottom
	df.loc['Total'] = df.iloc[:, :-1].sum()
	#sort columns left to right for highest to lowest totals
	df = df.sort_values('Total', axis=1, ascending=False)
	#print Totals row (sorted)
	#delete Totals row
	df = df.iloc[:-1]

	#divide into sets of four
	dfs = split_df_by_col(df)
	#print(dfs)

	#generate keys that correspond each region to a diff color
	key_colors = [wmf_colors['red'], wmf_colors['orange'], wmf_colors['yellow'], wmf_colors['green'], wmf_colors['purple'], wmf_colors['blue'], wmf_colors['pink'], wmf_colors['black50'], wmf_colors['brightblue']]
	keys = gen_keys(dfs, key_colors)

	'''
	#---PREPARE TO PLOT
	key1 = pd.DataFrame([['Central & Eastern Europe & Central Asia',wmf_colors['red']],
		['East, Southeast Asia, & Pacific',wmf_colors['orange']],
		['Latin America & Caribbean',wmf_colors['yellow']],
		['Middle East & North Africa',wmf_colors['green']]],
		index=['centraleuro','asiapacific','latamcarib','mideast'],
		columns=['labelname','color'])

	key2 = pd.DataFrame([['North America',wmf_colors['blue']],
		['Northern & Western Europe',wmf_colors['purple']],
		['South Asia',wmf_colors['pink']],
		['Sub-Saharan Africa',wmf_colors['black50']]],
		index=['northam','northeu','southasia','subafri'],
		columns=['labelname','color'])
	'''
	
	#---MAKE CHART---
	'''
	#first set of four
	chart1 = Wikichart(start_date,end_date,dfs[0])
	#print(dfs[0]['month'])
	#plt.figure(1)
	chart1.init_plot(width=12,subplotsx=2,subplotsy=2,fignum=0)
	chart1.plot_subplots_lines('month', keys[0])
	maxrange1 = chart1.get_maxrange()
	#second set of four
	chart2 = Wikichart(start_date,end_date,dfs[1])
	chart2.init_plot(width=12,subplotsx=2,subplotsy=2,fignum=1)
	chart2.plot_subplots_lines('month', keys[1])
	maxrange2 = chart2.get_maxrange()
	#calculate the largest range between the two figures and 8 subplots
	maxrange = max(maxrange1,maxrange2)
	#format and display figure 1
	plt.figure(0)
	chart1.standardize_subplotyrange(maxrange)
	chart1.format_subplots(title = 'Regional Active Editors',
		key = keys[0],
		data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM")
	#save chart1 but set display to False because plt.show() will show all figures at once
	chart1.finalize_plot(save_file_name1,display=False)
	#format and display figure 2
	plt.figure(1)
	chart2.standardize_subplotyrange(maxrange)
	chart2.format_subplots(title = 'Regional Active Editors',
		key = keys[1],
		data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM")
	chart2.finalize_plot(save_file_name2,display=display_flag)
	'''
	#print(dfs[2])
	#print(dfs[2].dtypes)
	#number of charts (subtracting 1 for the "month" column)
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
		charts[f].standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=figure_num_charts)
		charts[f].format_subplots(title = 'Regional Active Editors',
			key = keys[f],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			num_charts=figure_num_charts)
		#save chart1 but set display to False because plt.show() will show all figures at once
		save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_" + str(f) + ".jpeg"
		charts[f].finalize_plot(save_file_name,display=False)
	plt.show()


if __name__ == "__main__":
	main(sys.argv[1:])
