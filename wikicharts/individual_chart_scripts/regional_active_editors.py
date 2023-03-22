import pandas as pd
import datetime
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

	#pivot to make regions separate columns
	df = df.pivot(index='month', columns='region', values='monthly_editors').reset_index()
	print(df.dtypes)

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

	#---MAKE CHART---
	#first set of four
	chart1 = Wikichart(start_date,end_date,df1)
	#plt.figure(1)
	chart1.init_plot(width=12,subplotsx=2,subplotsy=2,fignum=0)
	chart1.plot_subplots_lines('month', key1)
	maxrange1 = chart1.get_maxrange()
	#second set of four
	chart2 = Wikichart(start_date,end_date,df2)
	chart2.init_plot(width=12,subplotsx=2,subplotsy=2,fignum=1)
	chart2.plot_subplots_lines('month', key2)
	maxrange2 = chart2.get_maxrange()
	#calculate the largest range between the two figures and 8 subplots
	maxrange = max(maxrange1,maxrange2)
	#format and display figure 1
	plt.figure(0)
	chart1.standardize_subplotyrange(maxrange)
	chart1.format_subplots(title = 'Regional Active Editors',
		key = key1,
		data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM")
	#save chart1 but set display to False because plt.show() will show all figures at once
	chart1.finalize_plot(save_file_name1,display=False)
	#format and display figure 2
	plt.figure(1)
	chart2.standardize_subplotyrange(maxrange)
	chart2.format_subplots(title = 'Regional Active Editors',
		key = key2,
		data_source="https://docs.google.com/spreadsheets/d/13XrrnCaz9qsKs5Gu_lUs2jtsK9VrSiGlilCleDgR6KM")
	chart2.finalize_plot(save_file_name2,display=display_flag)

if __name__ == "__main__":
	main(sys.argv[1:])
