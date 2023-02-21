import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import re
import calendar
from datetime import date

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Unique_Devices.png"
yoy_note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA---
df = pd.read_csv('../data/reader_metrics.tsv', sep='\t')

#display top rows for preview
#df.iloc[0,:] 

#---CLEAN DATA--
#print out data types
#print(df.month.dtype)

start_date = "2018-05-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#truncate to preferred date range
df = df[df["month"].isin(pd.date_range(start_date, end_date))]

#drop unneeded columns
df = df.drop(columns=['automated_pageviews','desktop','interactions','mobileweb','previews_seen','total_pageview'])

#drop rows w data error
df_a = df[df["month"].isin(pd.date_range(start_date, "2021-01-01"))]
df_b = df[df["month"].isin(pd.date_range("2022-07-01", end_date))]

#monthly higlight
monthly_df_a = df_a[df_a['month'].dt.month == month_interest]
monthly_df_b = df_b[df_b['month'].dt.month == month_interest]
monthly_df = pd.concat([monthly_df_a,monthly_df_b])

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
#plot data
plt.plot(df_a.month, df_a.unique_devices,
	label='_nolegend_',
	color=wmf_colors['brightblue'],
	linewidth = 2,
	zorder=6)
plt.plot(df_b.month, df_b.unique_devices,
	label='_nolegend_',
	color=wmf_colors['brightblue'],
	linewidth = 2,
	zorder=6)

#draw circle on highlighted month by plotting scatter
plt.scatter(monthly_df.month, monthly_df.unique_devices,
	#label='_nolegend_',
	label=month_name,
	color=wmf_colors['brightblue'],
	zorder=7)

#---DRAW DATA ERROR AREA---
#create rectangle x coordinates
startTime = datetime.strptime("2021-01-01", '%Y-%m-%d')
endTime = datetime.strptime("2022-07-01", '%Y-%m-%d')

# convert to matplotlib date representation
xstart = mdates.date2num(startTime)
xend = mdates.date2num(endTime)
width = xend - xstart

#get height
ytick_values = plt.gca().get_yticks()
ystart = ytick_values[0]
height = ytick_values[-1] - ytick_values[0]

pale_blue = '#c0e6ff'
# Plot rectangle
rect = Rectangle((xstart, ystart), width, height, 
	color='white', 
	linewidth=0,
	#alpha=0.1,
	fill='white',
	#hatch='///',
	edgecolor=None,
	zorder=5)
	#fill=None,
ax.add_patch(rect)  

#---FORMATTING---
#add title and axis labels
plt.title(f'Unique Devices - Wikipedia Only ({month_name})',font='Montserrat',weight='bold',fontsize=24,loc='left')
#plt.xlabel("Month",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
#plt.ylabel("Items",font='Montserrat', fontsize=18)

#format axis labels
plt.xticks(fontsize=14,fontname = 'Montserrat')
def y_label_formatter(value):
	formatted_value = '{:1.2f}B'.format(value*1e-9)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
plt.yticks(fontname = 'Montserrat',fontsize=14)

#expand bottom margin
plt.subplots_adjust(bottom=0.1, right = 0.8, left=0.1)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#add legend
#plt.legend(fontsize=18)
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

#rectangle annotation
annotation_x = xstart + (width / 2)
annotation_y = ystart + (height / 2)
rectangle_text = "Data unreliable February 2021 - June 2022 (inclusive)"

rectangle_textbox = ax.text(annotation_x, annotation_y, rectangle_text, 
	ha='center', 
	va='center', 
	color=wmf_colors['black25'],
	family='Montserrat',
	fontsize=14,
	wrap=True,
	bbox=dict(pad = 100, boxstyle='square', fc='none', ec='none'),
	zorder=8) 
rectangle_textbox._get_wrap_line_width = lambda : 300.

#data notes
plt.figtext(0.08, 0.025, "Graph Notes: Created by Hua Xi 12/12/22 using data from https://github.com/wikimedia-research/Readers-movement-metrics", fontsize=8, family='Montserrat', color= wmf_colors['black25'])

#---SHOW GRAPH---
#save as image
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
#show in window
plt.show()

