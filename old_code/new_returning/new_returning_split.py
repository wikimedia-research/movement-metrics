import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np

#---READ IN DATA--
df = pd.read_csv('editor_metrics.tsv', sep='\t')

#display top rows for preview
#df.head()

#---CLEAN DATA--
#look at data types
#print(df.active_editors.dtype)
#print(df.month.dtype)

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#---BREAK DATA INTO SUBSETS--
#display only data since 2019
truncated_df = df[df["month"].isin(pd.date_range("2019-01-01", "2022-12-01"))]
#display octobers only
october_df = truncated_df[truncated_df['month'].dt.month == 10]
#highlight the last two months
yoy_highlight = pd.concat([df.iloc[-13,:],df.iloc[-1,:]],axis=1).T
#highlighted_months = df[df['month'].isin(['2021-10-01','2022-10-01'])]

#---ADJUST PLOT SIZE---
matplotlib.rcParams.update({'font.size': 14, 'font.family':'Montserrat'})
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.set_figheight(6)
fig.set_figwidth(10)

#---PREPARE TO PLOT
#create a dictionary for colors
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','blue':'#0E65C0','green50':'#00af89','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}

#print list of available font names
#matplotlib.font_manager.get_font_names()
#print list of font paths (for troubleshooting) — clear font cache in ~/.matplotlib when adding new font
#matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

#put in fontsize formatting

#add grid lines
ax1.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
ax2.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
#linestyle = '--'

#---PLOT---
#plot active editor data
ax1.plot(truncated_df.month, truncated_df.returning_active_editors,
	label='Returning Active Editors',
	color=wmf_colors['blue'],
	zorder=3)
ax2.plot(truncated_df.month, truncated_df.new_active_editors,
	label='New Active Editors',
	color=wmf_colors['green50'],
	zorder=4)
ax2.plot(truncated_df.month, truncated_df.returning_active_editors,
	label='Returning Active Editors',
	color=wmf_colors['blue'],
	zorder=3)

#dots on Octobers
ax1.scatter(october_df.month, october_df.returning_active_editors,
	label='_nolegend_',
	color=wmf_colors['blue'],
	zorder=4)
ax2.scatter(october_df.month, october_df.new_active_editors,
	label='_nolegend_',
	color=wmf_colors['green50'],
	zorder=4)
#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5

#---FORMATTING---
#view broken axis
ax1.set_ylim(65000, 80000)  # outliers only
ax2.set_ylim(10000, 25000)  # most of the data
# hide the spines between ax and ax2
ax1.tick_params(labeltop=False,labelbottom=False)  # don't put tick labels at the top
ax1.set_xticks([])
ax1.set_xticks([], minor=True)
ax2.get_shared_x_axes().remove(ax1)
#add october x-axis labels
date_labels = []
for dl in october_df['month']:
	date_labels.append(datetime.datetime.strftime(dl, '%b %Y'))
ax2.set_xticks(ticks=october_df['month'],labels=date_labels,fontsize=14,fontname = 'Montserrat')

#add title and labels
fig.suptitle('New and Returning Editors',font='Montserrat',weight='bold',fontsize=24,horizontalalignment='right')
fig.text(0.04, 0.5, 'Active Editors', va='center', rotation='vertical',fontsize=18)

#add legend
matplotlib.rcParams['legend.fontsize'] = 14
plt.legend(frameon=False,
	loc ="upper center",
	bbox_to_anchor=(0.5, -0.15),
	fancybox=False, 
	shadow=False, 
	ncol=5,
	prop={"family":"Montserrat"},
	fontsize=18)

#expand bottom margin
plt.subplots_adjust(bottom=0.2)

#remove bounding box
for pos in ['right', 'top', 'bottom']:
	#plt.gca().spines[pos].set_visible(False)
	ax1.spines[pos].set_visible(False)
	ax2.spines[pos].set_visible(False)


#format y-axis labels
current_values = ax1.get_yticks()
ax1.set_yticklabels(['{:1.0f}K'.format(x*1e-3) for x in current_values])
current_values = ax2.get_yticks()
ax2.set_yticklabels(['{:1.0f}K'.format(x*1e-3) for x in current_values])

#add split
d = 0.005  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
#ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
#ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal


#---ADD ANNOTATIONS---
#make YoY annotation
def get_yoy(data_label):
	yoy_change_percent = ((yoy_highlight[data_label].iat[-1] - yoy_highlight[data_label].iat[0]) /  yoy_highlight[data_label].iat[0]) * 100
	if yoy_change_percent > 0:
		yoy_annotation = f"+{yoy_change_percent:.1f}% YoY"
	else:
		yoy_annotation = f"{yoy_change_percent:.1f}% YoY"
	return yoy_annotation
yoy_new = get_yoy('new_active_editors')
yoy_returning = get_yoy('returning_active_editors')
#data notes
plt.figtext(0.1, 0.05, "Graph Notes: Created by Hua Xi 12/12/22 using data from https://github.com/wikimedia-research/Editing-movement-metrics", fontsize=8, family='Montserrat',color= wmf_colors['black25'])

#---SHOW GRAPH---
plt.savefig('NewReturning_1.png', dpi=300)
plt.show()
