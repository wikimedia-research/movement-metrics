import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Active_Editors_Chart.png"
yoy_note = input('YoY annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/editor_metrics.tsv', sep='\t')

#display top rows for preview
#df.iloc[0,:] 

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

start_date = "2019-01-01"
end_date = "2023-01-01"
month_interest = 3

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#---BREAK DATA INTO SUBSETS--
#truncate data to period of interst
df = df[df["month"].isin(pd.date_range(start_date, end_date))]
#display data for month of interest only
monthly_df = df[df['month'].dt.month == month_interest]
#for highlighting
yoy_highlight = pd.concat([df.iloc[-13,:],df.iloc[-1,:]],axis=1).T
#highlighted_months = df[df['month'].isin(['2021-10-01','2022-10-01'])]

#---ADJUST PLOT SIZE---
#plt.figure(figsize=(10, 6))
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

#---PREPARE TO PLOT
#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#print list of font paths (for troubleshooting) — clear font cache in ~/.matplotlib when adding new font
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#add grid lines
ax1.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
#linestyle = '--'

#---PLOT---
#plot active editor data
ax1.plot(df.month, df.active_editors,
	label='_nolegend_',
	color=wmf_colors['blue'],
	zorder=3)

#dots on month of interest
ax2.scatter(monthly_df.month, monthly_df.active_editors,
	label='January',
	color=wmf_colors['blue'],
	zorder=4)
#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5

#draw circle on 2019 and 2022 to highlight for comparison
highlight_radius = 1000000
ax2.scatter(yoy_highlight.month, yoy_highlight.active_editors,
	label='_nolegend_',
	s=(highlight_radius**0.5),
	facecolors='none',
	edgecolors=wmf_colors['yellow'],
	zorder=5)


#---FORMATTING---
#add title and axis labels
plt.title('Active Editors',font='Montserrat',weight='bold',fontsize=24,loc='left')
#plt.xlabel("Month",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
#plt.ylabel("Active Editors",font='Montserrat', fontsize=18)

#add legend
'''
matplotlib.rcParams['legend.fontsize'] = 14
plt.legend(frameon=False,
	loc ="upper center",
	bbox_to_anchor=(0.5, -0.1),
	fancybox=False, 
	shadow=False, 
	ncol=1,
	prop={"family":"Montserrat"},
	fontsize=18)
'''

#expand bottom margin
plt.subplots_adjust(bottom=0.2, right = 0.85, left=0.1)

#remove bounding box
ax1.spines[['right', 'top','bottom', 'left']].set_visible(False)
ax2.spines[['right', 'top','bottom', 'left']].set_visible(False)
#for pos in ['right', 'top', 'bottom', 'left']:
#	ax1.gca().spines[pos].set_visible(False)

#format y-axis labels
def y_label_formatter(value):
	formatted_value = '{:1.0f}K'.format(value*1e-3)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
current_yvalues = ax1.get_yticks()
print(type(current_yvalues[0]))
#plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
ax1.set_yticklabels([y_label_formatter(x) for x in current_yvalues],fontname = 'Montserrat',fontsize=14)
#fontname = 'Montserrat',fontsize=14)
#plt.gca().set_yticklabels(['{:1.0f}K'.format(x*1e-3) for x in current_values])


#monthly x-axis labels on highlighted month

'''
#yearly x-axis labels on January
date_labels = []
date_labels_raw = pd.date_range(start_date, end_date, freq='AS-JAN')
for dl in date_labels_raw:
	date_labels.append(datetime.datetime.strftime(dl, '%Y'))
plt.xticks(ticks=date_labels_raw,labels=date_labels)
'''

'''
#add monthly x-axis labels with monthly ticks
date_labels = []
for dl in df['month']:
	if dl.month == month_interest:
		date_labels.append(datetime.datetime.strftime(dl, '%b %Y'))
	else:
		date_labels.append(" ")
plt.xticks(ticks=df['month'],labels=date_labels,fontsize=14,fontname = 'Montserrat')
'''

#year and month stacked label
#year label
year_labels = []
year_labels_raw = pd.date_range(start_date, end_date, freq='AS-JAN')
for dl in year_labels_raw:
	year_labels.append(datetime.datetime.strftime(dl, '%Y'))
ax1.set_xticks(ticks=year_labels_raw,labels=year_labels,fontsize=14,fontname = 'Montserrat')
ax1.tick_params(axis='x',which='major',pad=25)
#month label
ax2.xaxis.set_ticks_position("bottom")
ax2.xaxis.set_label_position("bottom")
month_labels = []
for dl in monthly_df['month']:
	month_labels.append(datetime.datetime.strftime(dl, '%b %Y'))
plt.xticks(ticks=monthly_df['month'],labels=month_labels,fontsize=10,fontname = 'Montserrat')


#---ADD ANNOTATIONS---
#YoY Change Annotation
#calculate YoY change
yoy_change_percent = ((yoy_highlight['active_editors'].iat[-1] - yoy_highlight['active_editors'].iat[0]) /  yoy_highlight['active_editors'].iat[0]) * 100
#make YoY annotation
if yoy_change_percent > 0:
	yoy_annotation = f"+{yoy_change_percent:.1f}% YoY" + " " + yoy_note
else:
	yoy_annotation = f"{yoy_change_percent:.1f}% YoY" + " " + yoy_note
plt.annotate(yoy_annotation,
	xy = (yoy_highlight['month'].iat[-1],yoy_highlight['active_editors'].iat[-1]),
	xytext = (20,-5),
	xycoords = 'data',
	textcoords = 'offset points',
	color='black',
	family='Montserrat',
	fontsize=14,
	weight='bold',
	wrap=True,
	bbox=dict(pad=10, facecolor="white", edgecolor="none"))

#data notes
plt.figtext(0.1, 0.025, "Graph Notes: Created by Hua Xi 12/12/22 using data from https://github.com/wikimedia-research/Editing-movement-metrics", fontsize=8, family='Montserrat',color= wmf_colors['black25'])

#---SHOW GRAPH---
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
plt.show()
