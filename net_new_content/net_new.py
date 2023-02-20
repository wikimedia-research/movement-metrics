import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import re
import calendar
from datetime import date

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Net_New_Chart.png"

#---READ IN DATA--
df = pd.read_csv('../data/editor_metrics.tsv', sep='\t')

#display top rows for preview
#df.head()
#df.iloc[0,:]

#---CLEAN DATA--
#print out data types
#print(df.month.dtype)
#print(df.net_new_Commons_content_pages.dtype)
#print(df.net_new_Wikidata_entities.dtype)
#print(df.net_new_Wikipedia_articles.dtype)
#print(df.net_new_content_pages.dtype)

start_date = "2018-05-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#truncate to preferred date range
df = df[df["month"].isin(pd.date_range(start_date, end_date))]

#---BREAK DATA INTO SUBSETS--
#create subsets of data for easier plotting
monthly_df = df[df['month'].dt.month == month_interest]
#subset to highlight the last two months
yoy_highlight = pd.concat([df.iloc[-13,:],df.iloc[-1,:]],axis=1).T
#subset to highlight specific months (manually entered)
#highlighted_months = df[df['month'].isin(['2021-10-01','2022-10-01'])]

#---PREPARE TO PLOT ---
#adjust plot size
plt.rcParams["figure.figsize"] = [12, 6]
#fig, ax = plt.subplots()
#plt.figure(figsize=(10, 6))

#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','base80':'#eaecf0','base70':'#c8ccd1','red':'#970302','pink':'#E679A6','purple':'#5748B5','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#print list of font paths (for troubleshooting) — clear font cache in ~/.matplotlib when adding new font
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#add grid lines
#thin light black line
plt.grid(axis = 'y', color = wmf_colors['black25'], linewidth = 0.25)
#dashed light black line
#plt.grid(axis = 'y', color = wmf_colors['black25'], linestyle = '--', linewidth = 0.5)

key = pd.DataFrame([['net_new_Commons_content_pages','Commons',wmf_colors['pink']],
	['net_new_Wikidata_entities','Wikidata',wmf_colors['brightgreen']],
	['net_new_Wikipedia_articles','Wikipedia',wmf_colors['purple']]],
	index=['commons','wikidata','wikipedia'],
	columns=['colname','labelname','color'])
#key.loc['commons','colname']

#---PLOT---
#plot data
plt.plot(df.month, df.net_new_Commons_content_pages,
	label=key.loc['commons','labelname'],
	color=key.loc['commons','color'],
	zorder=4)
plt.plot(df.month, df.net_new_Wikidata_entities,
	label=key.loc['wikidata','labelname'],
	color=key.loc['wikidata','color'],
	zorder=4)
plt.plot(df.month, df.net_new_Wikipedia_articles,
	label=key.loc['wikipedia','labelname'],
	color=key.loc['wikipedia','color'],
	zorder=4)

#draw circle on octobers by plotting scatter
plt.scatter(monthly_df.month, monthly_df.net_new_Commons_content_pages,
	label='_nolegend_',
	color=key.loc['commons','color'],
	zorder=5)
plt.scatter(monthly_df.month, monthly_df.net_new_Wikidata_entities,
	label='_nolegend_',
	color=key.loc['wikidata','color'],
	zorder=5)
plt.scatter(monthly_df.month, monthly_df.net_new_Wikipedia_articles,
	label='_nolegend_',
	color=key.loc['wikipedia','color'],
	zorder=5)

#draw circle on 2021 and 2022 to highlight for comparison
#scatter s variable sets size by "typographic points"
'''
highlight_radius = 1000000
plt.scatter(yoy_highlight.month, yoy_highlight.interactions_corrected,
	label='_nolegend_',
	s=(highlight_radius**0.5),
	facecolors='none',
	edgecolors=wmf_colors['yellow'],
	zorder=8)
#I explored using plt.patch.Circle but due to the unequal axes, it caused more trouble than this even though typographic points is not the ideal metric to be using
'''

#---FORMATTING---
#add title and labels
plt.title(f'Net New Content ({month_name})',font='Montserrat',weight='bold',fontsize=24,loc='left',pad=15)
#plt.xlabel("Month",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
#plt.ylabel("Active Editors",font='Montserrat', fontsize=14)

#add y axis labels
def y_label_formatter(value):
	formatted_value = '{:1.1f}M'.format(value*1e-6)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
plt.yticks(fontname = 'Montserrat',fontsize=14)

#format x axis
plt.xticks(fontname = 'Montserrat',fontsize=14)

#add monthly x-axis labels
'''
date_labels = []
for dl in monthly_df['month']:
	date_labels.append(datetime.datetime.strftime(dl, '%b %Y'))
plt.xticks(ticks=monthly_df['month'],labels=date_labels,fontsize=14,minor=False)
'''

#yearly x-axis labels on January
date_labels = []
date_labels_raw = pd.date_range(start_date, end_date, freq='AS-JAN')
for dl in date_labels_raw:
	date_labels.append(datetime.datetime.strftime(dl, '%Y'))
plt.xticks(ticks=date_labels_raw,labels=date_labels)


'''
#add legend
#plt.legend(fontsize=18)
matplotlib.rcParams['legend.fontsize'] = 14
plt.legend(frameon=False,
	loc ="upper center",
	bbox_to_anchor=(0.5, -0.1, ),
	fancybox=False, 
	shadow=False,
	ncol=4, 
	prop={"family":"Montserrat"})
'''

#expand bottom margin
plt.subplots_adjust(bottom=0.2, left=0.1, right=0.75)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#---ADD ANNOTATIONS---
#a = commons, b = wikidata, c = wikipedia
#check to see if labels need to adjusted for overlap
lastys = pd.DataFrame([yoy_highlight["net_new_Commons_content_pages"].iat[-1],
	yoy_highlight["net_new_Wikidata_entities"].iat[-1],
	yoy_highlight["net_new_Wikipedia_articles"].iat[-1]],
	index=['commons','wikidata','wikipedia'],
	columns=['lasty'])
lastys = lastys.sort_values(by=['lasty'],ascending=True)
#add column for y-padding
#set padding to 0 for lowest entry
lastys['ypad']=0
#doubles padding in case both labels need to be moved up
padmultiplier = 1 
#set remaining two paddings
for i in range(1,3):
	valuedistance = lastys.iloc[i]['lasty'] - lastys.iloc[i-1]['lasty']
	if valuedistance < 150000:
		lastys.at[lastys.iloc[i].name,'ypad'] = 5 * padmultiplier
	padmultiplier += 1

#add legend as data labels
def legend_annotate(data_label, legend_label, label_color,ypad):
	plt.annotate(legend_label,
		xy = (df['month'].iat[-1],df[data_label].iat[-1]),
		xytext = (20,-5 + ypad),
		xycoords = 'data',
		textcoords = 'offset points',
		color=label_color,
		fontsize=14,
		weight='bold',
		family='Montserrat')
#annotate in order of last-y (for padding)
for i in range(3):
	keyref = lastys.iloc[i].name
	legend_annotate(key.loc[keyref,'colname'],
		key.loc[keyref,'labelname'],
		key.loc[keyref,'color'],
		lastys.iloc[i].ypad)
#legend_annotate('net_new_Commons_content_pages', 'Commons',wmf_colors['pink'])
#legend_annotate('net_new_Wikidata_entities', 'Wikidata',wmf_colors['brightgreen'])
#legend_annotate('net_new_Wikipedia_articles', 'Wikipedia',wmf_colors['purple'])

#make YoY annotation
def yoy_annotation(data_label,label_color,ypad):
	yoy_change_percent = ((yoy_highlight[data_label].iat[-1] - yoy_highlight[data_label].iat[0]) /  yoy_highlight[data_label].iat[0]) * 100
	if yoy_change_percent > 0:
		yoy_annotation = f"+{yoy_change_percent:.1f}% YoY"
	else:
		yoy_annotation = f"{yoy_change_percent:.1f}% YoY"
	plt.annotate(yoy_annotation,
		xy = (yoy_highlight['month'].iat[-1],yoy_highlight[data_label].iat[-1]),
		xytext = (100,-5 + ypad),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		family='Montserrat',
		fontsize=14,
		weight='bold')
for i in range(3):
	keyref = lastys.iloc[i].name
	yoy_annotation(key.loc[keyref,'colname'],
		key.loc[keyref,'color'],
		lastys.iloc[i].ypad)
#yoy_annotation('net_new_Commons_content_pages',wmf_colors['pink'])
#yoy_annotation('net_new_Wikidata_entities',wmf_colors['brightgreen'])
#yoy_annotation('net_new_Wikipedia_articles',wmf_colors['purple'])

#data notes
today = date.today()
plt.figtext(0.1, 0.1, "Graph Notes: Created by Hua Xi " + str(today) + " using data from https://github.com/wikimedia-research/Reader-movement-metrics", fontsize=8, family='Montserrat', color= wmf_colors['black25'])

#---SHOW GRAPH---
#save as image
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
#show in window
plt.show()

