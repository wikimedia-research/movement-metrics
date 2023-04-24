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
	print("Generating Pageviews (Monthly Automated) chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Pageviews_Monthy_Automated.png"
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
	df = pd.read_csv(data_directory + '/data/monthly_pageviews.csv', sep=',')

	start_date = "2020-06-01"
	end_date = datetime.datetime.today()

	#convert string to datetime
	df['timestamp'] = pd.to_datetime(df['timestamp'])
	df.sort_values(by='timestamp')

	#truncate to preferred date range
	df = df[df["timestamp"].isin(pd.date_range(start_date, end_date))]

	#---PLOT---
	chart = Wikichart(start_date,end_date,df)
	chart.init_plot(width=12)
	chart.plot_line('timestamp','sum_view_count',wmf_colors['blue'])
	chart.plot_monthlyscatter('timestamp','sum_view_count',wmf_colors['blue'])
	chart.format(title = f'Monthly Automated Pageviews',
		radjust=0.825,
		data_source="https://stats.wikimedia.org")
	chart.annotate(x='timestamp',
		y='sum_view_count',
		num_annotation=chart.calc_yoy(y='sum_view_count',yoy_note=yoy_note))
	chart.finalize_plot(save_file_name,display=display_flag)

if __name__ == "__main__":
	main(sys.argv[1:])