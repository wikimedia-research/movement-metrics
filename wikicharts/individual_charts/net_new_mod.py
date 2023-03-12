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
	print("Generating Net New Content chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Net_New.png"
	yoy_note = " "
	display_flag = True
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

	start_date = "2018-05-01"
	end_date = "2023-01-01"

	#convert string to datetime
	df['month'] = pd.to_datetime(df['month'])

	#truncate to preferred date range
	df = df[df["month"].isin(pd.date_range(start_date, end_date))]

	#---PREPARE TO PLOT
	key = pd.DataFrame([['Commons',wmf_colors['pink']],
		['Wikidata',wmf_colors['brightgreen']],
		['Wikipedia',wmf_colors['purple']]],
		index=['net_new_Commons_content_pages','net_new_Wikidata_entities','net_new_Wikipedia_articles'],
		columns=['labelname','color'])

	#---MAKE CHART---
	chart = Wikichart(start_date,end_date,df)
	chart.init_plot(width=12)
	chart.plot_line('month','net_new_Commons_content_pages',key.loc['net_new_Commons_content_pages','color'])
	chart.plot_line('month','net_new_Wikidata_entities',key.loc['net_new_Wikidata_entities','color'])
	chart.plot_line('month','net_new_Wikipedia_articles',key.loc['net_new_Wikipedia_articles','color'])

	chart.plot_monthlyscatter('month','net_new_Commons_content_pages',key.loc['net_new_Commons_content_pages','color'])
	chart.plot_monthlyscatter('month','net_new_Wikidata_entities',key.loc['net_new_Wikidata_entities','color'])
	chart.plot_monthlyscatter('month','net_new_Wikipedia_articles',key.loc['net_new_Wikipedia_articles','color'])

	chart.format(title = f'Net New Content',
		y_order=1e-6,
		y_label_format='{:1.1f}M',
		radjust=0.75,
		data_source="https://github.com/wikimedia-research/Editing-movement-metrics")

	#labeling is done together in order to calculate correct spacing to prevent label overlap whereas the lines can be plotted separately
	chart.multi_yoy_annotate(['net_new_Commons_content_pages','net_new_Wikidata_entities','net_new_Wikipedia_articles'],key,chart.calc_yoy)

	chart.finalize_plot(save_file_name,display=display_flag)

if __name__ == "__main__":
	main(sys.argv[1:])


