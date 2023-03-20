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
	print("Generating Active Editors chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Active_Editors.png"
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
	df = pd.read_csv(data_directory + '/data/editor_metrics.tsv', sep='\t')

	#note start and end dates may be different depending on chart_type
	start_date = "2019-01-01"
	end_date = datetime.datetime.today()

	#convert string to datetime
	df['month'] = pd.to_datetime(df['month'])

	#truncate data to period of interst
	df = df[df["month"].isin(pd.date_range(start_date, end_date))]

	#---MAKE CHART---
	chart = Wikichart(start_date,end_date,df)
	chart.init_plot()
	chart.plot_line('month','active_editors',wmf_colors['blue'])
	chart.plot_monthlyscatter('month','active_editors',wmf_colors['blue'])
	chart.plot_yoy_highlight('month','active_editors')
	chart.format(title = 'Active Editors',
		data_source="https://github.com/wikimedia-research/Editing-movement-metrics")
	chart.annotate(x='month',
		y='active_editors',
		num_annotation=chart.calc_yoy(y='active_editors',yoy_note=yoy_note))
	chart.finalize_plot(save_file_name,display=display_flag)

if __name__ == "__main__":
	main(sys.argv[1:])
