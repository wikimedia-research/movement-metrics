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
	print("Generating Content Interactions chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Content_Interactions.png"
	yoy_note = " "
	display_flag = True
	if len(opts) > 0:
		for opt in opts[0]:
			if opt == '-p':
				outfile_name = input('Outfile_name:\n')
				yoy_note = input('YoY annotation note (default is blank):\n')
			elif opt == '-i':
				display_flag = False
	save_file_name = dirname(script_directory) + "/charts/" + outfile_name

	#---CLEAN DATA--
	data_directory = dirname(dirname(script_directory))
	df = pd.read_csv(data_directory + '/data/reader_metrics.tsv', sep='\t')
	corrected_df = pd.read_csv(data_directory + '/data/corrected_metrics_only.csv')

	start_date = "2018-05-01"
	end_date = "2023-03-01"

	#convert string to datetime
	df['month'] = pd.to_datetime(df['month'])
	corrected_df['month'] = pd.to_datetime(corrected_df['month'])

	#set new index
	corrected_df.set_index('month')

	#truncate to preferred date range
	df = df[df["month"].isin(pd.date_range(start_date, end_date))]

	#combine datasets — add corrected values to the reader metrics dataset
	df['interactions_corrected'] = df['interactions']
	correction_range = pd.date_range(start='2021-05-01', end='2022-01-01', freq='MS')
	for m in correction_range:
		row_index = df[df['month'] == m].index 
		correct_row = corrected_df.loc[corrected_df['month'] ==  m]
		df.loc[row_index, 'interactions_corrected'] = correct_row['interactions_corrected'].values

	#---MAKE CHART---
	chart = Wikichart(start_date,end_date,df)
	chart.init_plot()
	chart.plot_data_loss('month','interactions','interactions_corrected',corrected_df)
	chart.plot_line('month','interactions_corrected',wmf_colors['blue'])
	chart.plot_monthlyscatter('month','interactions_corrected',wmf_colors['blue'])
	chart.plot_yoy_highlight('month','interactions_corrected')
	chart.format(title = f'Content Interactions',
		radjust=0.87,
		data_source="https://github.com/wikimedia-research/Reader-movement-metrics")
	chart.annotate(x='month',
		y='interactions_corrected',
		num_annotation=chart.calc_yoy(y='interactions_corrected'))
	chart.finalize_plot(save_file_name,display=display_flag)

if __name__ == "__main__":
	main(sys.argv[1:])