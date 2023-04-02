import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import path
import getopt
import sys
import os
from os.path import dirname
sys.path.append('../')
from wikicharts import Wikichart
from wikicharts import wmf_colors

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
	print(df.columns)
	print(len(df.columns))

	#divide into two datasets
	df1 = df[['month','Central & Eastern Europe & Central Asia','East, Southeast Asia, & Pacific','Latin America & Caribbean','Middle East & North Africa']]
	df2 = df[['month','North America','Northern & Western Europe','South Asia','Sub-Saharan Africa']]

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

	annotation_text = "*Data unreliable [February 2021 - June 2022] (period not shown)"

	#---MAKE CHART---
	#first set of four
	chart1 = Wikichart(start_date,end_date,df1)
	#plt.figure(1)
	chart1.init_plot(width=12,height=6,subplotsx=2,subplotsy=2,fignum=0)
	chart1.plot_subplots_lines('month', key1)
	maxrange1 = chart1.get_maxrange()
	#second set of four
	chart2 = Wikichart(start_date,end_date,df2)
	chart2.init_plot(width=12,height=6,subplotsx=2,subplotsy=2,fignum=1)
	chart2.plot_subplots_lines('month', key2)
	maxrange2 = chart2.get_maxrange()
	#calculate the largest range between the two figures and 8 subplots
	maxrange = max(maxrange1,maxrange2)
	#format and display figure 1
	plt.figure(0)
	chart1.standardize_subplotyrange(maxrange)
	chart1.block_off_multi(block_off_start,block_off_end)
	chart1.format_subplots(title = 'Regional Unique Devices',
		key = key1,
		data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
		tadjust=0.8, badjust=0.1)
	chart1.top_annotation(annotation_text = annotation_text)
	#save chart1 but set display to False because plt.show() will show all figures at once
	chart1.finalize_plot(save_file_name1,display=False)
	#format and display figure 2
	plt.figure(1)
	chart2.standardize_subplotyrange(maxrange)
	chart2.block_off_multi(block_off_start,block_off_end)
	chart2.format_subplots(title = 'Regional Unique Devices',
		key = key2,
		data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM",
		tadjust=0.8, badjust=0.1)
	chart2.top_annotation(annotation_text = annotation_text)
	chart2.finalize_plot(save_file_name2,display=display_flag)

	#---MARK CHART PROGRAMMATIC
	'''
	keys = []
	charts = []
	num_figures = ceil(len(df.columns) / 4)
	'''


if __name__ == "__main__":
	main(sys.argv[1:])
