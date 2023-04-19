import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import path
import getopt
import geopandas as gpd
import shapefile as shp
import seaborn as sns
import sys
import os
from os.path import dirname
sys.path.append('../')
from wikicharts import Wikichart
from wikicharts import wmf_colors

def main(argv):
	print("Generating Map chart...")

	#parse commandline arguments
	opts, args = getopt.getopt(argv,"pi")

	#---PROMPT FOR INPUT---
	script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
	outfile_name = "Map.png"
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

	#---MAKE CHART---
	world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
	world.plot()
	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])
