import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import re

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Pageviews_Source.png"
note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/pageviews_source.csv')

#display top rows for preview
#df.head()

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

#convert string to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by='timestamp')

#truncate to preferred date range
df = df[df["timestamp"].isin(pd.date_range("2022-02-01", "2022-12-01"))]

#long to wide
df = pd.pivot(df, index = 'timestamp', columns='access_method', values='sum_view_count')
df = df.reset_index()     
df = df.rename_axis(None, axis=1)
df = df.rename(columns={'mobile web':'mobile_web'})

#---ADJUST PLOT SIZE---
plt.figure(figsize=(12, 6))

#---PREPARE TO PLOT
#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','base80':'#eaecf0','base70':'#c8ccd1','red':'#970302','pink':'#E679A6','purple':'#5748B5','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#print list of font paths (for troubleshooting) — clear font cache in ~/.matplotlib when adding new font
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#add grid lines
plt.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
#linestyle = '--'

#---BREAK DATA INTO SUBSETS
#subset to highlight the last two months
mom_highlight = pd.concat([df.iloc[-2,:],df.iloc[-1,:]],axis=1).T

#---PLOT---
#plot data
plt.plot(df.timestamp, df.desktop,
	label='_nolegend_',
	color=wmf_colors['brightgreen'])

plt.plot(df.timestamp, df.mobile_web,
	label='_nolegend_',
	color=wmf_colors['pink'])

#plot mom highlights
plt.scatter(mom_highlight.timestamp, mom_highlight.desktop,
	label='_nolegend_',
	color=wmf_colors['brightgreen'])
plt.scatter(mom_highlight.timestamp, mom_highlight.mobile_web,
	label='_nolegend_',
	color=wmf_colors['pink'])

#---FORMATTING---
#add title and labels
plt.title('Monthly Automated Pageviews (Source)',font='Montserrat',weight='bold',fontsize=24,loc='left')
plt.xlabel("2022",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
plt.ylabel("Pageviews",font='Montserrat', fontsize=18,labelpad=10)

#expand bottom margin
plt.subplots_adjust(bottom=0.2, left=0.1, right=0.85)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#format y-axis labels
def y_label_formatter(value):
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	if value >= 1e9:
		formatted_value = '{:1.1f}B'.format(value*1e-9)
		formatted_value = formatted_value.replace('.0','')
	else:
		formatted_value = '{:1.0f}M'.format(value*1e-6)
	return tail_dot_rgx.sub(r'\2',formatted_value)
plt.yticks(range(200000000,2200000000,200000000))
current_values = plt.gca().get_yticks()
#plt.gca().set_yticklabels(['{:1.0f}M'.format(x*1e-6) for x in current_values])
plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
plt.yticks(fontname = 'Montserrat',fontsize=14)

#add monthly x-axis labels
date_labels = []
for dl in df['timestamp']:
	date_labels.append(datetime.datetime.strftime(dl, '%b'))
plt.xticks(ticks=df['timestamp'],labels=date_labels,fontsize=14,fontname = 'Montserrat')

#---ADD ANNOTATIONS---
#add combined annotation
def annotate(data_label, legend_label, label_color):
	plt.annotate(legend_label,
		xy = (df['timestamp'].iat[-1],df[data_label].iat[-1]),
		xytext = (20,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color=label_color,
		fontsize=14,
		weight='bold',
		wrap = 'True',
		family='Montserrat')
	pageviews = df[data_label].iat[-1]
	if pageviews >= 1e9:
		annotation = '{:1.2f}B Pageviews'.format(pageviews*1e-9)
	else:
		annotation = '{:1.0f}M Pageviews'.format(pageviews*1e-6)
	plt.annotate(annotation,
		xy = (df['timestamp'].iat[-1],pageviews),
		xytext = (20,-25),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		family='Montserrat',
		fontsize=14,
		weight='bold')
annotate('desktop','Desktop',wmf_colors['brightgreen'])
annotate('mobile_web','Mobile Web',wmf_colors['pink'])

#data notes
plt.figtext(0.1, 0.05, "Graph Notes: Created by Hua Xi 12/12/22 using data from https://docs.google.com/spreadsheets/d/1Aw5kjj47cEi-PSX0eApCUp3Ww9_XNyARxcdoL9QnHp4", fontsize=8, family='Montserrat',color= wmf_colors['black25'])

#---SHOW GRAPH---
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
plt.show()
