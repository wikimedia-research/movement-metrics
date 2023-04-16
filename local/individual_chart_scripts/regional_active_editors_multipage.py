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
from wikicharts import roll

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
	df = df.rename(columns={'UNCLASSED':"Unclassed"})

	#add code to set month as index
	#df = df.set_index('month')

	#divide into sets of four
	dfs = split_df_by_col(df)

	#generate keys that correspond each region to a diff color
	key_colors = [wmf_colors['red'], wmf_colors['orange'], wmf_colors['yellow'], wmf_colors['green'], wmf_colors['purple'], wmf_colors['blue'], wmf_colors['pink'], wmf_colors['black50'], wmf_colors['brightblue']]
	keys = gen_keys(dfs, key_colors)

	#---MAKE CHARTS---
	fig_counter = 0
	total_num_charts = len(df.columns) - 1
	charts_per_figure = 4
	num_figures = ceil(total_num_charts / charts_per_figure)
	figures = [None]*num_figures
	#max range across figures
	maxranges = [None]*num_figures 
	num_ticks = [None]*num_figures
	#initialize each figure
	for f in range(num_figures):
		figure_num_charts = len(dfs[f].columns) - 1
		figures[f] = Wikichart(start_date,end_date,dfs[f])
		figures[f].init_plot(width=12,subplotsx=2,subplotsy=2,fignum=f)
		figures[f].plot_subplots_lines('month', keys[f], num_charts=figure_num_charts)
		maxranges[f], num_ticks[f] = figures[f].get_maxyrange()
	#calculate the largest range between the two figures and 8 subplots
	maxrange = max(maxranges)
	maxrange_index = maxranges.index(maxrange)
	maxrange_numticks = num_ticks[maxrange_index]
	#format and display each figure in multi-chart figures
	for f in range(num_figures):
		plt.figure(f)
		figure_num_charts = len(dfs[f].columns) - 1
		figures[f].standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=figure_num_charts)
		figures[f].format_subplots(title = 'Regional Active Editors',
			key = keys[f],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			num_charts=figure_num_charts)
		figures[f].clean_ylabels_subplots()
		#save chart1 but set display to False because plt.show() will show all figures at once
		save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_" + str(f) + ".jpeg"
		figures[f].finalize_plot(save_file_name,display=False)
	plt.show()
	fig_counter = num_figures
	
	#---GENERATE INDIVIDUAL CHARTS---
	individual_charts = [None]*total_num_charts
	columns = list(df.columns)
	columns.remove('month')
	for c in range(len(columns)):
		fig_counter = fig_counter + 1
		current_col = columns[c]
		current_df = df[['month', current_col]]
		current_savefile = dirname(script_directory) + "/charts/individual_" + outfile_name + "_" + str(c) + ".jpeg"
		individual_charts[c] = Wikichart(start_date,end_date,current_df)
		individual_charts[c].init_plot(fignum=fig_counter)
		individual_charts[c].plot_line('month',current_col,key_colors[c])
		individual_charts[c].plot_line('month',current_col,key_colors[c])
		individual_charts[c].plot_monthlyscatter('month',current_col,col =key_colors[c])
		individual_charts[c].plot_yoy_highlight('month',current_col)
		individual_charts[c].standardize_yrange(maxrange, maxrange_numticks)
		individual_charts[c].format(title = f'Active Editors: {current_col}',
			ybuffer=False,
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			tadjust=0.825,badjust=0.125,
			titlepad=25)
		individual_charts[c].annotate(x='month',
			y=current_col,
			num_annotation=individual_charts[c].calc_yoy(y=current_col,yoy_note=yoy_note))
		individual_charts[c].finalize_plot(current_savefile,display=False)
	plt.show()

	#---AGGREGATE VIEWS---
	#Eight Figure View
	charts_per_figure = 8
	keys = gen_keys([df], key_colors)
	fig_counter += 1
	main_fig = Wikichart(start_date,end_date,df)
	main_fig.init_plot(width=12,subplotsx=2,subplotsy=4,fignum=fig_counter)
	main_fig.plot_subplots_lines(x='month', key=keys[0], num_charts=charts_per_figure, subplot_title_size=9)
	main_fig.standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=charts_per_figure)
	main_fig.format_subplots(title = 'Regional Active Editors',
			key = keys[0],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			num_charts=charts_per_figure,
			tickfontsize=8)
	main_fig.clean_ylabels_subplots(tickfontsize=8)
	save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_fullview.png"
	main_fig.finalize_plot(save_file_name,display=False)
	plt.show()
	#Rolling View
	core_df = df.drop(columns=['Unclassed'])
	rolling = roll(core_df, rolling_months = 3)
	fig_counter += 1
	main_fig = Wikichart(start_date,end_date,rolling)
	main_fig.init_plot(width=12,subplotsx=2,subplotsy=4,fignum=fig_counter)
	main_fig.plot_subplots_lines(x='month', key=keys[0], num_charts=charts_per_figure, subplot_title_size=9)
	main_fig.standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=charts_per_figure)
	main_fig.format_subplots(title = 'Regional Active Editors: Rolling',
			key = keys[0],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			num_charts=charts_per_figure,
			tickfontsize=8,
			mo_in_title=False)
	main_fig.clean_ylabels_subplots(tickfontsize=8)
	save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_rolling.png"
	main_fig.finalize_plot(save_file_name,display=False)
	plt.show()
	#Annual
	core_df = df.drop(columns=['Unclassed'])
	annual = core_df.groupby(core_df.month.dt.year).mean().reset_index()
	fig_counter += 1
	main_fig = Wikichart(start_date,end_date,annual)
	main_fig.init_plot(width=12,subplotsx=2,subplotsy=4,fignum=fig_counter)
	main_fig.plot_subplots_lines(x='month', key=keys[0], num_charts=charts_per_figure, subplot_title_size=9)
	main_fig.standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=charts_per_figure)
	main_fig.format_subplots(title = 'Regional Active Editors: Annual Average',
			key = keys[0],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			num_charts=charts_per_figure,
			tickfontsize=8,
			mo_in_title=False)
	main_fig.clean_ylabels_subplots(tickfontsize=8)
	save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_annual.png"
	main_fig.finalize_plot(save_file_name,display=False)
	plt.show()
	#Quarterly
	core_df = df.drop(columns=['Unclassed'])
	quarterly = core_df.groupby(core_df['month'].dt.to_period('Q')).mean().reset_index()
	quarterly['month'] = quarterly['month'].astype(str)
	quarterly['month'] = pd.to_datetime(quarterly['month'])
	fig_counter += 1
	main_fig = Wikichart(start_date,end_date,quarterly)
	main_fig.init_plot(width=12,subplotsx=2,subplotsy=4,fignum=fig_counter)
	main_fig.plot_subplots_lines(x='month', key=keys[0], num_charts=charts_per_figure, subplot_title_size=9)
	main_fig.standardize_subplotyrange(maxrange, maxrange_numticks, num_charts=charts_per_figure)
	main_fig.format_subplots(title = 'Regional Active Editors: Quarterly Average',
			key = keys[0],
			data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
			num_charts=charts_per_figure,
			tickfontsize=8,
			mo_in_title=False)
	main_fig.clean_ylabels_subplots(tickfontsize=8)
	save_file_name = dirname(script_directory) + "/charts/" + outfile_name + "_quarterly.png"
	main_fig.finalize_plot(save_file_name,display=False)
	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])
