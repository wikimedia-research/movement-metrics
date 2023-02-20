import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re
import calendar

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "New_Returning_Chart.png"
yoy_note = input('YoY annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/editor_metrics.tsv', sep='\t')

#display top rows for preview
#df.head()

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

start_date = "2019-01-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#---BREAK DATA INTO SUBSETS--
#only data since 2019
df = df[df["month"].isin(pd.date_range(start_date, end_date))]
#month of interest only
monthly_df = df[df['month'].dt.month == month_interest]
#highlight the last two months
yoy_highlight = pd.concat([df.iloc[-13,:],df.iloc[-1,:]],axis=1).T
#highlighted_months = df[df['month'].isin(['2021-10-01','2022-10-01'])]

#---ADJUST PLOT SIZE---
plt.figure(figsize=(12, 6))

#---PREPARE TO PLOT
#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','blue':'#0E65C0','green50':'#00af89','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#print list of font paths (for troubleshooting) — clear font cache in ~/.matplotlib when adding new font
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#add grid lines
plt.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
#linestyle = '--'

#---PLOT---
#plot active editor data
plt.plot(df.month, df.returning_active_editors,
	label='Returning Active Editors',
	color=wmf_colors['blue'],
	zorder=3)
plt.plot(df.month, df.new_active_editors,
	label='New Active Editors',
	color=wmf_colors['green50'],
	zorder=3)

#dots on month of interest
plt.scatter(monthly_df.month, monthly_df.returning_active_editors,
	label='_nolegend_',
	color=wmf_colors['blue'],
	zorder=4)
plt.scatter(monthly_df.month, monthly_df.new_active_editors,
	label='_nolegend_',
	color=wmf_colors['green50'],
	zorder=4)
#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5

#draw circle on 2019 and 2022 to highlight for comparison
highlight_radius = 1000000
plt.scatter(yoy_highlight.month, yoy_highlight.returning_active_editors,
	label='_nolegend_',
	s=(highlight_radius**0.5),
	facecolors='none',
	edgecolors=wmf_colors['yellow'],
	zorder=5)
plt.scatter(yoy_highlight.month, yoy_highlight.new_active_editors,
	label='_nolegend_',
	s=(highlight_radius**0.5),
	facecolors='none',
	edgecolors=wmf_colors['yellow'],
	zorder=5)

#---FORMATTING---
#add title and labels
plt.title(f'New and Returning Editors ({month_name})',font='Montserrat',weight='bold',fontsize=24,loc='left',pad=10)
#plt.xlabel("Month",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
#plt.ylabel("Active Editors",font='Montserrat', fontsize=18)

#add legend
'''
matplotlib.rcParams['legend.fontsize'] = 14
plt.legend(frameon=False,
	loc ="upper center",
	bbox_to_anchor=(0.5, -0.075),
	fancybox=False, 
	shadow=False, 
	ncol=5,
	prop={"family":"Montserrat"},
	fontsize=18)
'''

#expand bottom margin
plt.subplots_adjust(bottom=0.1, left=0.1, right=0.75)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#format y-axis labels
def y_label_formatter(value):
	formatted_value = '{:1.0f}K'.format(value*1e-3)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
plt.yticks(fontname = 'Montserrat',fontsize=14)
plt.xticks(fontname = 'Montserrat',fontsize=14)

#add monthly x-axis labels
'''
date_labels = []
for dl in monthly_df['month']:
	date_labels.append(datetime.datetime.strftime(dl, '%b %Y'))
plt.xticks(ticks=monthly_df['month'],labels=date_labels,fontsize=14,fontname = 'Montserrat')
'''

#yearly x-axis labels on January
date_labels = []
date_labels_raw = pd.date_range(start_date, end_date, freq='AS-JAN')
for dl in date_labels_raw:
	date_labels.append(datetime.datetime.strftime(dl, '%Y'))
plt.xticks(ticks=date_labels_raw,labels=date_labels)


#---ADD ANNOTATIONS---
#add combined annotation
def annotate(data_label, legend_label, label_color, x_distance):
	yoy_change_percent = ((yoy_highlight[data_label].iat[-1] - yoy_highlight[data_label].iat[0]) /  yoy_highlight[data_label].iat[0]) * 100
	if yoy_change_percent > 0:
		yoy_annotation = f" +{yoy_change_percent:.1f}% YoY" + " " + yoy_note
	else:
		yoy_annotation = f" {yoy_change_percent:.1f}% YoY" + " " + yoy_note
	plt.annotate(legend_label,
		xy = (df['month'].iat[-1],df[data_label].iat[-1]),
		xytext = (20,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color=label_color,
		fontsize=14,
		weight='bold',
		family='Montserrat')
	plt.annotate(yoy_annotation,
		xy = (df['month'].iat[-1],df[data_label].iat[-1]),
		xytext = (x_distance,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		fontsize=14,
		weight='bold',
		wrap=True,
		family='Montserrat')
annotate('new_active_editors', 'New',wmf_colors['green50'], 55)
annotate('returning_active_editors', 'Returning',wmf_colors['blue'], 95)

'''
#add legend as data labels
def legend_annotate(data_label, legend_label, label_color):
	plt.annotate(legend_label,
		xy = (df['month'].iat[-1],df[data_label].iat[-1]),
		xytext = (20,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color=label_color,
		fontsize=14,
		weight='bold',
		family='Montserrat')
legend_annotate('new_active_editors', 'New',wmf_colors['green50'])
legend_annotate('returning_active_editors', 'Returning',wmf_colors['blue'])

#make YoY annotation
def yoy_annotation(data_label,label_color):
	yoy_change_percent = ((yoy_highlight[data_label].iat[-1] - yoy_highlight[data_label].iat[0]) /  yoy_highlight[data_label].iat[0]) * 100
	if yoy_change_percent > 0:
		yoy_annotation = f"+{yoy_change_percent:.1f}% YoY"
	else:
		yoy_annotation = f"{yoy_change_percent:.1f}% YoY"
	plt.annotate(yoy_annotation,
		xy = (yoy_highlight['month'].iat[-1],yoy_highlight[data_label].iat[-1]),
		xytext = (100,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color=label_color,
		family='Montserrat',
		fontsize=14,
		weight='bold',
		bbox=dict(pad=0, facecolor="white", edgecolor="none"))
yoy_annotation('new_active_editors',wmf_colors['green50'])
yoy_annotation('returning_active_editors',wmf_colors['blue'])
'''
#data notes
plt.figtext(0.1, 0.025, "Graph Notes: Created by Hua Xi 12/12/22 using data from https://github.com/wikimedia-research/Editing-movement-metrics", fontsize=8, family='Montserrat',color= wmf_colors['black25'])

#---SHOW GRAPH---
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
plt.show()
