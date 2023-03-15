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
	print("Generating Project_Growth chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Project_Growth.png"
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
	df = pd.read_csv(data_directory + '/data/wikidata_growth.csv', sep='\t')
	df = pd.read_csv(data_directory + '/data/wikipedia_growth.csv', sep='\t')
	df = pd.read_csv(data_directory + '/data/commons_growth.csv', sep='\t')

	#note start and end dates may be different depending on chart_type
	start_date = "2014-01-01"
	end_date = "2023-01-01"

	#convert string to datetime
	df_wikidata['month'] = df_wikidata['month'].apply(lambda x: x.rsplit("T")[0])
	df_wikipedia['month'] = df_wikipedia['month'].apply(lambda x: x.rsplit("T")[0])
	df_commons['month'] = df_commons['month'].apply(lambda x: x.rsplit("T")[0])
	df_wikidata['month'] = pd.to_datetime(df_wikidata['month'])
	df_wikipedia['month'] = pd.to_datetime(df_wikipedia['month'])
	df_commons['month'] = pd.to_datetime(df_commons['month'])

	#change column names
	df_wikidata = df_wikidata.rename(columns={'total.content':'wikidata'})
	df_wikipedia = df_wikipedia.rename(columns={'total.content':'wikipedia'})
	df_commons = df_commons.rename(columns={'total.content':'commons'})

	#drop unneeded columns
	df_wikidata = df_wikidata.drop(columns=['timeRange.start', 'timeRange.end'])
	df_wikipedia = df_wikipedia.drop(columns=['timeRange.start', 'timeRange.end'])
	df_commons = df_commons.drop(columns=['timeRange.start', 'timeRange.end'])

	#merge into one dataframe
	df = pd.merge(pd.merge(df_wikidata,df_wikipedia,on='month'),df_commons,on='month')

	#truncate date
	df = df[df["month"].isin(pd.date_range(start_date, end_date))]

	#---PREPARE TO PLOT
	key = pd.DataFrame([['Wikidata',wmf_colors['pink']],
		['Wikipedia',wmf_colors['yellow']],
		['Commons',wmf_colors['orange']]],
		index=['wikidata','wikipedia','commons'],
		columns=['labelname','color'])

	#---PLOT---
	chart = Wikichart(start_date,end_date,df)
	chart.init_plot(width=12)
	chart.plot_line('month','wikidata',key.loc['wikidata','color'],linewidth=4)
	chart.plot_line('month','wikipedia',key.loc['wikipedia','color'])
	chart.plot_line('month','commons',key.loc['commons','color'])
	chart.format(title = f'Growth of Wikimedia Projects: Content Items',
		y_order=1e-6,
		y_label_format='{:1.0f}M',
		radjust=0.75,
		data_source="https://stats.wikimedia.org")

	chart.multi_yoy_annotate(['wikidata','wikipedia','commons'],key,chart.calc_finalcount)

	chart.finalize_plot(save_file_name,display=display_flag)

if __name__ == "__main__":
	main(sys.argv[1:])