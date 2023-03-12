import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import re
import calendar
import pycountry
from datetime import date

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "By_Country.png"
yoy_note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA---
df = pd.read_csv('../data/by_country_jan23.csv')

#display top rows for preview
#df.iloc[0,:] 

#---CLEAN DATA--
#print out data types
#print(df.month.dtype)

month_interest = 1
month_name = calendar.month_name[month_interest]

#clean columns
df = df.drop(columns=['January "raw" 2022'])

#split into reader table and editor table
df_editors = df[df["category"] == "editors"]
df_readers = df[df["category"] == "readers"]

#add uniform country code label for readers
df_editors['country_code'] = df_editors['country']
#create dictionary in format {"full name" : "country code"}
countries_lookup = {}
for country in pycountry.countries:
    countries_lookup[country.name] = country.alpha_2
countries_lookup['United States'] = "US"
countries_lookup['Russia'] = "RU"
df_readers['country_code'] = df_readers.apply(lambda row : countries_lookup[row['country']],axis=1)
#add uniform country name for editors
#df_readers['country_name'] = df_readers['country']
#create dictionary in format {"country code":"full name"}
countrycode_lookup = {}
for country in pycountry.countries:
    countrycode_lookup[country.alpha_2] = country.name
countrycode_lookup['US'] = "US"
countrycode_lookup['RU'] = "Russia"
countrycode_lookup['GB'] = "UK"
df_editors['country_name'] = df_editors.apply(lambda row : countrycode_lookup[row['country']],axis=1)

#create view
df_readers.rename(columns={"Corrected January 2022": "readers_jan22"}, inplace=True)
df_readers.rename(columns={"jan23x": "readers_jan23"}, inplace=True)
df_readers.rename(columns={"% Change": "readers_yoychange"}, inplace=True)
df_editors.rename(columns={"Corrected January 2022": "editors_jan22"}, inplace=True)
df_editors.rename(columns={"jan23x": "editors_jan23"}, inplace=True)
df_editors.rename(columns={"% Change": "editors_yoychange"}, inplace=True)
df_readers.rename(columns={"Proportion_of_Total_Jan23": "readers_perctotal23"}, inplace=True)
df_readers = df_readers.drop(columns=['country','category'])
df_editors = df_editors.drop(columns=['country','category','Proportion_of_Total_Jan23'])
df_readers = df_readers.set_index('country_code')
df_editors = df_editors.set_index('country_code')
df_bycountry = df_readers.join(df_editors)
#reset index
df_bycountry = df_bycountry.reset_index(level=0)
#sort by proportion 23 largest to smallest
df_bycountry.sort_values(by=['readers_perctotal23'],ascending=False)

#print(df_bycountry)
#print(df_bycountry.iloc[0,:])
#print(type(df_bycountry.iloc[0,:]['readers_perctotal23']))

#---PREPARE TO PLOT ---
#adjust plot size
fig, ax = plt.subplots()
fig.set_figwidth(12)
fig.set_figheight(6)
#plt.rcParams["figure.figsize"] = [12, 6]

#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','base80':'#eaecf0','base70':'#c8ccd1','purple':'#5748B5','orange':'#EE8019','red':'#970302','pink':'#E679A6','purple':'#5748B5','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#add grid lines
#thin light black line
plt.grid(axis = 'y', color = wmf_colors['black25'], linewidth = 0.25)
#dashed light black line
#plt.grid(axis = 'y', color = wmf_colors['black25'], linestyle = '--', linewidth = 0.5)

#---PLOT---
bar_width = 0.4
#index w multiplier for spacing
new_index = df_bycountry.index*2
#plot data
plt.bar(new_index-0.2, df_bycountry.readers_yoychange, bar_width,
	label='User Pageviews YoY Change',
	color=wmf_colors['pink'],
	linewidth = 2,
	zorder=6)
plt.bar(new_index+0.2, df_bycountry.editors_yoychange, bar_width,
	label='Logged-in Editors YoY Change',
	color=wmf_colors['yellow'],
	linewidth = 2,
	zorder=6)


#---FORMATTING---
#expand bottom margin
plt.subplots_adjust(bottom=0.25, right = 0.95, left=0.05)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#add title and axis labels
plt.title(f'Pageviews and Editors by Country ({month_name})',font='Montserrat',weight='bold',fontsize=24,loc='left',pad=10)
plt.xlabel("Country \n % of Total Pageviews 2023",font='Montserrat', fontsize=14, labelpad=10) #source serif pro

#format axis labels
plt.yticks(fontname = 'Montserrat',fontsize=14)
def percent_formatter(value):
	#print(type(value))
	formatted_value = '{0:.0%}'.format(value)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([percent_formatter(x) for x in current_values])

#format xticks
plt.xticks(fontname = 'Montserrat',fontsize=12)
#simple country labels
#plt.xticks(new_index, df_bycountry.country_name)
#labels w proportion
x_labels = []
for index, row in df_bycountry.iterrows():
	label = row['country_name'] + "\n" + percent_formatter(row['readers_perctotal23'])
	x_labels.append(label)
print(x_labels)
plt.xticks(new_index, x_labels)



'''
#add legend
#plt.legend(fontsize=18)
'''
'''
matplotlib.rcParams['legend.fontsize'] = 14
plt.legend(frameon=False,
	loc ="upper center",
	bbox_to_anchor=(0.5, -0.1),
	fancybox=False, 
	shadow=False,
	ncol=1, 
	prop={"family":"Montserrat"},
	labelspacing=0.01,
	handlelength=0.5) #adjust space between marker and label
'''

#---ADD ANNOTATIONS---
'''
#YoY Change Annotation
#calculate YoY change
def annotate(data_label, legend_label, label_color, x_distance):
	plt.annotate(legend_label,
		xy = (df_b['month'].iat[-1],df_b[data_label].iat[-1]),
		xytext = (10,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color=label_color,
		fontsize=14,
		weight='bold',
		family='Montserrat')
	final_count = df_b[data_label].iat[-1]
	count_annotation = '{:1.2f}B'.format(final_count*1e-9)
	plt.annotate(count_annotation,
		xy = (df_b['month'].iat[-1],final_count),
		xytext = (x_distance,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		fontsize=14,
		weight='bold',
		wrap=True,
		family='Montserrat')
annotate('unique_devices', 'Unique Devices',wmf_colors['brightblue'], 130)
'''

#data notes
today = date.today()
plt.figtext(0.08, 0.025, "Graph Notes: Created by Hua Xi " + str(today) + " using data from https://docs.google.com/spreadsheets/d/1YfKmAe6ViAIjnPejYEq6yCkuYa8QK8-h6VxsAlbnNGA", fontsize=8, family='Montserrat', color= wmf_colors['black25'])

#---SHOW GRAPH---
#save as image
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
#show in window
plt.show()
