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
	#print update
	print("Generating New Returning chart...")

	#---INTERPRET COMMANDLINE ARGUEMNTS---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "New_Returning.png"
	yoy_note = " "
	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")
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
	df = pd.read_csv(data_directory + '/data/editor_metrics.tsv', sep='\t')

	start_date = "2019-01-01"
	end_date = datetime.datetime.today()

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
	chart = Wikichart(start_date,end_date,df)
	chart.init_plot(width=12)
	chart.plot_line('month','returning_active_editors',key.loc['returning_active_editors','color'])
	chart.plot_line('month','new_active_editors',key.loc['new_active_editors','color'])
	chart.plot_monthlyscatter('month','returning_active_editors',key.loc['returning_active_editors','color'])
	chart.plot_monthlyscatter('month','new_active_editors',key.loc['new_active_editors','color'])
	chart.plot_yoy_highlight('month','returning_active_editors')
	chart.plot_yoy_highlight('month','new_active_editors')
	chart.format(title = f'New and Returning Editors',
		radjust=0.75,
		data_source="https://github.com/wikimedia-research/Editing-movement-metrics")

	chart.multi_yoy_annotate(['returning_active_editors','new_active_editors'],key,chart.calc_yoy)

	chart.finalize_plot(save_file_name,display=display_flag)


if __name__ == "__main__":
	main(sys.argv[1:])