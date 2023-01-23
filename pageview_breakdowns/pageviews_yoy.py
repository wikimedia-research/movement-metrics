import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np

#---PROMPT FOR INPUT---
outfile_name = input('Outfile_name:\n') or "Pageviews_YoY.png"
note = input('Annotation note (default is blank):\n') or " "

#---READ IN DATA--
df = pd.read_csv('../data/pageviews_2022.csv')

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

#---BREAK DATA INTO SUBSETS
#subset to highlight the last two months
mom_highlight = pd.concat([df.iloc[-2,:],df.iloc[-1,:]],axis=1).T

#---PLOT---
#plot data
plt.plot(df.timestamp, df.sum_view_count,
	label='_nolegend_',
	color=wmf_colors['blue'])

plt.scatter(mom_highlight.timestamp, mom_highlight.sum_view_count,
	label='_nolegend_',
	color=wmf_colors['blue'])

#---FORMATTING---
#add title and labels
plt.title('Monthly Automated Pageviews',font='Montserrat',weight='bold',fontsize=24,loc='left')
plt.xlabel("2022",font='Montserrat', fontsize=18, labelpad=10) #source serif pro
#plt.ylabel("Active Editors",font='Montserrat', fontsize=18)

#expand bottom margin
plt.subplots_adjust(bottom=0.15,left=0.1,right=0.825)

#remove bounding box
for pos in ['right', 'top', 'bottom', 'left']:
	plt.gca().spines[pos].set_visible(False)

#format y-axis labels
def y_label_formatter(value):
	formatted_value = '{:1.1f}B'.format(value*1e-9)
	formatted_value = formatted_value.replace('.0','')
	return formatted_value
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([y_label_formatter(x) for x in current_values])
plt.yticks(fontname = 'Montserrat',fontsize=14)


#add monthly x-axis labels
date_labels = []
for dl in df['timestamp']:
	date_labels.append(datetime.datetime.strftime(dl, '%b'))
plt.xticks(ticks=df['timestamp'],labels=date_labels,fontsize=10,fontname = 'Montserrat')

#---ADD ANNOTATIONS---
#add combined annotation
def annotate():
	pageviews = df['sum_view_count'].iat[-1]
	annotation = '{:1.2f}B Pageviews'.format(pageviews*1e-9)
	plt.annotate(annotation,
		xy = (df['timestamp'].iat[-1],pageviews),
		xytext = (20,-5),
		xycoords = 'data',
		textcoords = 'offset points',
		color='black',
		fontsize=14,
		weight='bold',
		wrap = 'True',
		family='Montserrat')
annotate()

#data notes
plt.figtext(0.1, 0.015, "Graph Notes: Created by Hua Xi 12/12/22 using data from https://docs.google.com/spreadsheets/d/1Aw5kjj47cEi-PSX0eApCUp3Ww9_XNyARxcdoL9QnHp4", fontsize=8, family='Montserrat',color= wmf_colors['black25'])

#---SHOW GRAPH---
save_file_name = "charts/" + outfile_name
plt.savefig(save_file_name, dpi=300)
plt.show()
