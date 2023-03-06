import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re
from datetime import date
from matplotlib.patches import Ellipse
import matplotlib.dates as mdates
import calendar

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Pageviews_YoY.png"
note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/monthly_pageviews.csv')

#display top rows for preview
#df.head()

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

start_date = "2020-07-01"
end_date = "2023-01-01"
month_interest = 1
month_name = calendar.month_name[month_interest]

#convert string to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by='timestamp')

#truncate to preferred date range
df = df[df["timestamp"].isin(pd.date_range(start_date, end_date))]

#---ADJUST PLOT SIZE---
#plt.figure(figsize=(12, 6))
fig, ax = plt.subplots()
fig.set_figwidth(12)
fig.set_figheight(6)

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

#---BREAK DATA INTO SUBSETS
#monthly highlight
monthly_df = df[df['timestamp'].dt.month == month_interest]

#subset to highlight the last year
yoy_highlight = pd.concat([df.iloc[-13,:],df.iloc[-1,:]],axis=1).T

#---PLOT---
#plot data
plt.plot(df.timestamp, df.pageviews_corrected,
	label='_nolegend_',
	color=wmf_colors['blue'])

plt.scatter(monthly_df.timestamp, monthly_df.pageviews_corrected,
	label='_nolegend_',
	color=wmf_colors['blue'])

#draw circle on 2021 and 2022 to highlight for comparison
#scatter s variable sets size by "typographic points"
highlight_radius = 1000000
plt.scatter(yoy_highlight.timestamp, yoy_highlight.pageviews_corrected,
	label='_nolegend_',
	s=(highlight_radius**0.5),
	facecolors='none',
	edgecolors=wmf_colors['yellow'],
	zorder=8)
#I explored using plt.patch.Circle but due to the unequal axes, it caused more trouble than this even though typographic points is not the ideal metric to be using


#---CIRCLE YTD AREA---
#add a circle to highlight the YTD area
#year to date
year_end = df.iloc[-1,:].timestamp
year_start = pd.to_datetime(date(year_end.year, 1, 1))
ytd = df[df["timestamp"].isin(pd.date_range(year_start, year_end))]

#estimate a center for ellipse
year_endnum = mdates.date2num(year_end)
year_startnum = mdates.date2num(year_start)
halfway_num = (year_endnum - year_startnum) / 2 + year_startnum

#estimated width/height for ellipse
xstart = mdates.date2num(year_start)
xend = mdates.date2num(year_end)
bracket_w = xend - xstart
ellipse_w = xend - xstart

'''
# Plot rectangle
circ = Ellipse((halfway_num, ytd_max), width=ellipse_w,height=ellipse_h,
	color='red')
	#fill=None,
	#linestyle='--',
	#edgecolor='red')
ax.add_patch(circ)  
'''

#---FORMATTING---
#add title and labels
plt.title(f'Monthly User Pageviews to Wikimedia ({month_name})',font='Montserrat',weight='bold',fontsize=24,loc='left',pad=25)
#plt.xlabel("2022",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
#plt.ylabel("Active Editors",font='Montserrat', fontsize=18)

#expand bottom margin
plt.subplots_adjust(bottom=0.15,left=0.1,right=0.825,top=0.85)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#format y-axis labels
def y_label_formatter(value):
	formatted_value = '{:1.1f}B'.format(value*1e-9)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
plt.yticks(fontname = 'Montserrat',fontsize=14)

#format x-axis labels
plt.xticks(fontname = 'Montserrat',fontsize=14)

#yearly x-axis labels on January
date_labels = []
date_labels_raw = pd.date_range(start_date, end_date, freq='AS-JAN')
for dl in date_labels_raw:
	date_labels.append(datetime.datetime.strftime(dl, '%Y'))
plt.xticks(ticks=date_labels_raw,labels=date_labels)

#add monthly x-axis labels
'''date_labels = []
for dl in df['timestamp']:
	date_labels.append(datetime.datetime.strftime(dl, '%b'))
plt.xticks(ticks=df['timestamp'],labels=date_labels,fontsize=14,fontname = 'Montserrat')
'''

#---ADD ANNOTATIONS---
#add combined annotation
def yoy_annotate():
	yoy_change_percent = ((yoy_highlight['pageviews_corrected'].iat[-1] - yoy_highlight['pageviews_corrected'].iat[0]) /  yoy_highlight['pageviews_corrected'].iat[0]) * 100
	#make YoY annotation (add text her if relevant)
	if yoy_change_percent > 0:
		yoy_annotation = f"+{yoy_change_percent:.1f}% YoY" + " " + note
	else:
		yoy_annotation = f"{yoy_change_percent:.1f}% YoY" + " " + note
	#annotate
	plt.annotate(yoy_annotation,
		xy = (yoy_highlight['timestamp'].iat[-1],yoy_highlight['pageviews_corrected'].iat[-1]),
		xytext = (20,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		family='Montserrat',
		fontsize=12,
		weight='bold',
		wrap=True,
		bbox=dict(pad=10, facecolor="white", edgecolor="none"))
yoy_annotate()

'''
#year to date
year_end = df.iloc[-1,:].timestamp
year_start = pd.to_datetime(date(year_end.year, 1, 1))
ytd = df[df["timestamp"].isin(pd.date_range(year_start, year_end))]
ytd_views = ytd['pageviews_corrected'].sum()
#convert date to axis number
year_startnum = mdates.date2num(year_start)
year_endnum = mdates.date2num(year_end)
halfway_num = (year_endnum - year_startnum) / 2 + year_startnum
#views for same period last year
lastyear_end = df.iloc[-13,:].timestamp
lastyear_start = pd.to_datetime(date(lastyear_end.year, 1, 1))
lastyear = df[df["timestamp"].isin(pd.date_range(lastyear_start, lastyear_end))]
#find maximum and minimum y value over period
ytd_max = ytd['pageviews_corrected'].max()
ytd_min = ytd['pageviews_corrected'].min()
ellipse_h = ytd_max - ytd_max
lastytd_views = lastyear['pageviews_corrected'].sum()
def ytd_annotate():
	#calculate change
	ytd_change_percent = ((ytd_views - lastytd_views) /  lastytd_views) * 100
	#make YoY annotation (add text her if relevant)
	lastyear_str = str(df.iloc[-13,:].timestamp.year)
	if ytd_change_percent > 0:
		ytd_annotation = f"+{ytd_change_percent:.1f}% YTD \n vs. {lastyear_str}" 
	else:
		ytd_annotation = f"{ytd_change_percent:.1f}% YTD \n vs. {lastyear_str}"
	#annotate
	plt.annotate(ytd_annotation,
		#xy = (df['timestamp'].iat[-1],df['pageviews_corrected'].iat[-1]), #place at end
		#xytext=(10,-5),
		xy = (halfway_num - 30, ytd_max), #place in middle, raised slightly
		xytext = (20,20),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		family='Montserrat',
		fontsize=12,
		weight='bold',
		wrap=True,
		#ha='center', 
		va='bottom',
		bbox=dict(boxstyle='square', fc='white',edgecolor="none"))
#lw = line width
ytd_annotate()
plt.plot([year_startnum, year_startnum, year_endnum, year_endnum], [ytd_max * 1.005, ytd_max * 1.01, ytd_max * 1.01, ytd_max * 1.005], lw=1.5, color = 'black')
'''

#data notes
today = date.today()
plt.figtext(0.1, 0.015, "Graph Notes: Created by Hua Xi " + str(today) + " using data from https://docs.google.com/spreadsheets/d/1YfKmAe6ViAIjnPejYEq6yCkuYa8QK8-h6VxsAlbnNGA/edit#gid=1529620965", fontsize=8, family='Montserrat',color= wmf_colors['black25'])
#https://superset.wikimedia.org/superset/explore/p/YMKXW7zXw4l/

#---SHOW GRAPH---
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
plt.show()
