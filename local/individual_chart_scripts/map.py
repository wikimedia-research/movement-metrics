import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import path
import getopt
import geopandas as gpd
import shapefile as shp
from shapely.ops import unary_union
import shapely.ops
import shapely.geometry
import seaborn as sns
import sys
import os
from os.path import dirname
sys.path.append('../')
from wikicharts import Wikichart
from wikicharts import wmf_colors
from wikicharts import Wikimap
from wikicharts import simple_format

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
	#need to swap out for google docs version
	wmf_region_ref = pd.read_csv(data_directory + '/data/wmf_region_ref.csv', sep=',')
	#country code in alpha-3
	raw_map_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')) 
	#country code in iso-a3
	#remove antarctica
	map_df = raw_map_df[(raw_map_df.name!="Antarctica")]
	#match up wmf region data in wmf_region_ref with geographic data in map_df
	map_df = map_df.merge(wmf_region_ref, how='left', left_on="iso_a3", right_on="code")
	map_df = map_df[['name_x','iso_a3', 'pop_est', 'gdp_md_est', 'geometry', 'wmf_region']]
	map_df = map_df.rename(columns={"name_x": "name"})
	#create pivot to get sum values
	value_col = 'pop_est'
	region_table = pd.pivot_table(map_df, values=value_col, index=['wmf_region'], aggfunc=np.sum)
	region_table = region_table.rename(columns={value_col: "sum_" + value_col})
	#merge pivot table with map data
	map_df = map_df.merge(region_table, how='left', left_on="wmf_region", right_on="wmf_region")
	#generate regional linestrings
	regions = ["Central & Eastern Europe & Central Asia", "East, Southeast Asia, & Pacific", "Latin America & Caribbean", "Middle East & North Africa", "North America", "Northern & Western Europe", "South Asia", "Sub-Saharan Africa"]
	region_table['geometry'] = ''
	for region in regions:
		region_df = map_df.loc[map_df['wmf_region'] == region]
		region_polys = region_df['geometry'].values.tolist()
		region_boundary = gpd.GeoSeries(unary_union(region_polys))
		region_table.at[region,'geometry'] = region_boundary
	#get representative centroid xys for each region
	region_table['centroid'] = region_table['geometry'].apply(lambda g: g.centroid)
	region_table['label'] = region_table['sum_pop_est'].apply(lambda v: simple_format(v))
	print(region_table['label'])
	#region_table.to_csv("region_geometries.csv")

	#---MAKE CHART---
	#WORLD POPULATION
	#calculate world pop per region
	#
	chart = Wikimap(map_df)
	#format first bc the colorbar will mess up alignment
	chart.add_titles(title = 'World Population',
		data_source="geopandas")
	chart.plot_wcolorbar(col = 'sum_pop_est')
	chart.plot_regions(region_table)
	chart.label_regions(region_table)
	chart.format_simple()
	chart.format_colobar()
	chart.finalize_plot(save_file_name,display=True)

if __name__ == "__main__":
	main(sys.argv[1:])
