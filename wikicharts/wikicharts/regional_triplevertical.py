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
from colour import Color

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "By_Country_Vertical.png"
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
#sort by proportion 23 largest to smallest
df_bycountry = df_bycountry.sort_values(by=['readers_perctotal23'],ascending=True)
#reset index
df_bycountry = df_bycountry.reset_index(level=0)

#print(df_bycountry)
#print(df_bycountry.iloc[0,:])
#print(type(df_bycountry.iloc[0,:]['readers_perctotal23']))

#---PREPARE TO PLOT ---
#adjust plot size
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
fig.set_figwidth(12)
fig.set_figheight(6)
plt.subplots_adjust(wspace = 0.05)
#plt.rcParams["figure.figsize"] = [12, 6]

#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','base80':'#eaecf0','base70':'#c8ccd1','purple':'#5748B5','orange':'#EE8019','red':'#970302','pink':'#E679A6','purple':'#5748B5','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#set up gradient
red = Color("red")
gradient = list(red.range_to(Color("green"),11))
gradient = [color.rgb for color in gradient]
#get order ranking for pageviews yoy
df_bycountry['reader_yoy_rank'] = df_bycountry['readers_yoychange'].rank()
df_bycountry['editors_yoy_rank'] = df_bycountry['editors_yoychange'].rank()
#get reodered gradients
reader_gradient = []
for index, row in df_bycountry.iterrows():
    rank = row['reader_yoy_rank']
    color = gradient[int(rank)-1]
    reader_gradient.append(color)
editor_gradient = []
for index, row in df_bycountry.iterrows():
    rank = row['editors_yoy_rank']
    color = gradient[int(rank)-1]
    editor_gradient.append(color)

#---PLOT---
bar_width = 0.5
#index w multiplier for spacing
new_index = df_bycountry.index
#plot data
bars1 = ax1.barh(new_index, df_bycountry.readers_perctotal23, bar_width,
	label='Proportion of Total User Pageviews 2023',
	color=wmf_colors['black25'],
	zorder=6)
bars2 = ax2.barh(new_index, df_bycountry.readers_yoychange, bar_width,
	label='User Pageviews YoY Change',
	color=reader_gradient,
	zorder=6)
bars3 = ax3.barh(new_index, df_bycountry.editors_yoychange, bar_width,
	label='Logged-in Editors YoY Change',
	color=editor_gradient,
	zorder=6)



#---FORMATTING---
#expand bottom margin
plt.subplots_adjust(top=0.8,bottom=0.1, right = 0.9, left=0.1)

#remove bounding box
ax1.set_frame_on(False)
ax2.set_frame_on(False)
ax3.set_frame_on(False)

#add title and axis labels
#note there seems to be a bug with ha and va args to suptitle, so just set x and y manually
fig.suptitle(f'Pageviews and Editors by Country ({month_name})',ha='left',x=0.05,y=0.97,fontsize=24,fontproperties={'family':'Montserrat','weight':'bold'})

#add subplot chart labels below
ax1.set_title('Proportion of \n Total User Pageviews 2023 (%)',fontfamily='Montserrat',fontsize=14)
ax2.set_title('User Pageviews \n YoY Change (%)',fontfamily='Montserrat',fontsize=14)
ax3.set_title('Logged-in Editors \n YoY Change (%)',fontfamily='Montserrat',fontsize=14)

#format yticks
ax1.set_yticks(new_index) 
ax1.set_yticklabels(df_bycountry.country_name,fontfamily='Montserrat',fontsize=12)
ax2.set_yticks(new_index) 
ax2.set_yticklabels([]) 
ax2.tick_params('y', length=0, width=0, which='both')
ax3.set_yticks(new_index) 
ax3.set_yticklabels([]) 
ax3.tick_params('y', length=0, width=0, which='both')
#ax3.set_yticks([]) 

#format xticks
def percent_formatter(value):
	#print(type(value))
	formatted_value = '{0:.0%}'.format(value)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
ax1.set_xticklabels([percent_formatter(float(label.get_text())) for label in ax1.get_xticklabels() ],fontfamily='Montserrat',fontsize=12)
#note that Matplotlib text objects return stirngs with the Minus Sign instead of the Hyphen which float() doesn't recognize so we replace minus signs with hyphens
ax2.set_xticklabels([percent_formatter(float(label.get_text().replace('−','-'))) for label in ax2.get_xticklabels() ],fontfamily='Montserrat',fontsize=12)
ax3.set_xticklabels([percent_formatter(float(label.get_text().replace('−','-'))) for label in ax3.get_xticklabels() ],fontfamily='Montserrat',fontsize=12)

#add gridlines
ax1.grid(visible=True,which='major',axis='y',color = wmf_colors['black25'], linewidth = 0.25)
ax2.grid(visible=True,which='major',axis='y',color = wmf_colors['black25'], linewidth = 0.25)
ax3.grid(visible=True,which='major',axis='y',color = wmf_colors['black25'], linewidth = 0.25)

#add bar labels
bar1_labels = [percent_formatter(x) for x in df_bycountry.readers_perctotal23]
ax1.bar_label(bars1, labels=bar1_labels, fontfamily='Montserrat',fontsize=8,label_type='center',color='black',zorder=8)
bar2_labels = [percent_formatter(x) for x in df_bycountry.readers_yoychange]
ax2.bar_label(bars2, labels=bar2_labels, fontfamily='Montserrat',fontsize=8,label_type='center',color='black',zorder=8)
bar3_labels = [percent_formatter(x) for x in df_bycountry.editors_yoychange]
ax3.bar_label(bars3, labels=bar3_labels, fontfamily='Montserrat',fontsize=8,label_type='center',color='black',zorder=8)

#---ADD ANNOTATIONS---
#data notes
today = date.today()
plt.figtext(0.08, 0.025, "Graph Notes: Created by Hua Xi " + str(today) + " using data from https://docs.google.com/spreadsheets/d/1YfKmAe6ViAIjnPejYEq6yCkuYa8QK8-h6VxsAlbnNGA", fontsize=8, family='Montserrat', color= wmf_colors['black25'])

#---SHOW GRAPH---
#save as image
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
#show in window
plt.show()
