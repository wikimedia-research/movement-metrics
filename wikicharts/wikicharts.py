import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import numpy as np
import math
import re
import calendar
from datetime import date
from PIL import ImageFont
import warnings


#---CUSTOM DICTIONARIES
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','base80':'#eaecf0','orange':'#EE8019','base70':'#c8ccd1','red':'#970302','pink':'#E679A6','green50':'#00af89','purple':'#5748B5','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}
parameters = {'month_interest':2,'author':'Hua Xi'}
style_parameters = {'font':'Montserrat','title_font_size':24,'text_font_size':14}


#---CUSTOM FUNCTIONS---
#takes a y value, an order to divide it by, and a format and produces a label-ready text
def y_label_formatter(value,multiplier,format_text):
	formatted_value = format_text.format(value*multiplier)
	#remove trailing zeros after decimal point only
	tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
	return tail_dot_rgx.sub(r'\2',formatted_value)

#takes a value and calculates the order and a reasonable default text formatting
def calc_order_format(value):
	if value == 0:
		order = 1
	else:
		order = math.floor(math.log10(abs(value)))
	if order >= 12:
		multiplier = float('1e-12')
		formatting = '{:1.2f}T'
	elif order >= 9:
		multiplier = float('1e-9')
		formatting = '{:1.2f}B'
	elif order >= 6:
		multiplier = float('1e-6')
		formatting = '{:1.2f}M'
	elif order > 3:
		multiplier = float('1e-3')
		formatting = '{:1.2f}K'
	else:
		multiplier = 1
		formatting = '{:1.0f}'
	return multiplier, formatting

#---BASIC CHART---
#the wrapper's main functionality is in the formatting and annotation
#the plotting functions could actually probably be deleted bc they just repeat matplotlib's functions

class Wikichart:
	def __init__(self,start_date, end_date,dataset,month_interest=parameters['month_interest'],yoy_highlight=None):
		self.start_date = start_date
		self.end_date = end_date
		self.month_interest = month_interest
		self.month_name = calendar.month_name[month_interest]
		self.df = dataset

	def init_plot(self,width=10,height=6):
		#plt.figure(figsize=(width, height))
		fig, ax = plt.subplots()
		fig.set_figwidth(width)
		fig.set_figheight(height)
		plt.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)

	def plot_line(self, x, y, col, legend_label ='_nolegend_',linewidth = 2):
		plt.plot(self.df[str(x)], self.df[str(y)],
			label=legend_label,
			color=col,
			zorder=3,
			linewidth=linewidth)

	def plot_monthlyscatter(self, x, y, col, legend_label ='_nolegend_'):
		#dots on month of interest
		monthly_df = self.df[self.df[str(x)].dt.month == self.month_interest]
		plt.scatter(monthly_df[str(x)], monthly_df[str(y)],
			label=legend_label,
			color=col,
			zorder=4)
			#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5
	
	def plot_yoy_highlight(self, x, y, col = wmf_colors['yellow'], legend_label ='_nolegend_'):
		yoy_highlight = pd.concat([self.df.iloc[-13,:],self.df.iloc[-1,:]],axis=1).T
		#dots on month of interest
		highlight_radius = 1000000
		plt.scatter(yoy_highlight[str(x)], yoy_highlight[str(y)],
			label=legend_label,
			s=(highlight_radius**0.5),
			facecolors='none',
			edgecolors=col,
			zorder=5)
			#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5

	def plot_data_loss(self, x, y1, y2, data_loss_df, col = wmf_colors['base80'], legend_label ='_nolegend_'):
		plt.fill_between(data_loss_df[str(x)], data_loss_df[str(y1)], data_loss_df[str(y2)],
			label=legend_label,
			color=col,
			edgecolor=col,
			zorder=3)

	def format(self, title, author=parameters['author'], data_source="N/A",radjust=0.85,ladjust=0.1,tadjust=0.9,badjust=0.1):
		#format title
		custom_title = f'{title} ({calendar.month_name[self.month_interest]})'
		plt.title(custom_title,font=style_parameters['font'],fontsize=style_parameters['title_font_size'],weight='bold',loc='left')
		#remove bounding box
		for pos in ['right', 'top', 'bottom', 'left']:
			plt.gca().spines[pos].set_visible(False)
		#expand bottom margin (to make room for author and data source annotation)
		plt.subplots_adjust(bottom=badjust, right = radjust, left=ladjust, top=tadjust)
		#format y-axis range (gca = get current axis)
		#we want the plotted portion to be 2/3rds the total y axis range
		ax = plt.gca()
		current_ylim = ax.get_ylim()
		current_yrange = current_ylim[1] - current_ylim[0]
		new_ymin = current_ylim[0] - current_yrange / 4
		new_ymax = current_ylim[1] + current_yrange / 4
		ax.set_ylim([new_ymin, new_ymax])
		#format x-axis labels — yearly x-axis labels on January
		plt.xticks(fontname=style_parameters['font'],fontsize=style_parameters['text_font_size'])
		date_labels = []
		date_labels_raw = pd.date_range(self.start_date, self.end_date, freq='AS-JAN')
		for dl in date_labels_raw:
			date_labels.append(datetime.datetime.strftime(dl, '%Y'))
		plt.xticks(ticks=date_labels_raw,labels=date_labels)
		#format y-axis labels
		warnings.filterwarnings("ignore")
		current_values = plt.gca().get_yticks()
		new_labels = []
		for y_value in current_values:
			y_order, y_label_format = calc_order_format(y_value)
			new_label = y_label_formatter(y_value, y_order, y_label_format)
			new_labels.append(new_label)
		plt.gca().set_yticklabels(new_labels)
		plt.yticks(fontname=style_parameters['font'],fontsize=style_parameters['text_font_size'])
		#add bottom annotation
		today = date.today()
		plt.figtext(0.1, 0.025, "Graph Notes: Created by " + str(author) + " " + str(today) + " using data from " + str(data_source), family=style_parameters['font'],fontsize=8, color= wmf_colors['black25'])

	def calc_yoy(self,y,yoy_note=""):
		yoy_highlight = pd.concat([self.df.iloc[-13,:],self.df.iloc[-1,:]],axis=1).T
		yoy_change_percent = ((yoy_highlight[str(y)].iat[-1] - yoy_highlight[str(y)].iat[0]) /  yoy_highlight[str(y)].iat[0]) * 100
		if yoy_change_percent > 0:
			yoy_annotation = f" +{yoy_change_percent:.1f}% YoY" + " " + yoy_note
		else:
			yoy_annotation = f" {yoy_change_percent:.1f}% YoY" + " " + yoy_note
		return(yoy_annotation)

	def calc_finalcount(self,y,yoy_note=""):
		final_count = self.df[str(y)].iat[-1]
		multiplier, formatting = calc_order_format(final_count)
		count_annotation = y_label_formatter(value = final_count,multiplier = multiplier,format_text=formatting)
		return(count_annotation)

	def annotate(self, x, y, num_annotation, legend_label="", label_color='black', xpad=0, ypad=0):
		#legend annotation
		#note that when legend_label="", xpad should be 0 (only a numerical annotation is produced)
		plt.annotate(legend_label,
			xy = (self.df[str(x)].iat[-1],self.df[str(y)].iat[-1]),
			xytext = (20,-5+ypad),
			xycoords = 'data',
			textcoords = 'offset points',
			color=label_color,
			fontsize=style_parameters['text_font_size'],
			weight='bold',
			family=style_parameters['font'])
		#increase xpad for numerical annotation if legend annotation is present (prevent overlap)
		if(len(legend_label) > 0):
			try:
				font = ImageFont.truetype('Montserrat-Bold.ttf', style_parameters['text_font_size'])
				labelsize = font.getsize(legend_label)
				xpad= labelsize[0] + 3
			except:
				xpad = len(legend_label) * 4
		#numerical annotation
		plt.annotate(num_annotation,
			xy = (self.df[str(x)].iat[-1],self.df[str(y)].iat[-1]),
			xytext = (20+xpad,-5+ypad),
			xycoords = 'data',
			textcoords = 'offset points',
			color='black',
			fontsize=style_parameters['text_font_size'],
			weight='bold',
			wrap=True,
			family=style_parameters['font'])
		
	def finalize_plot(self, save_file_name, display=True):
		plt.savefig(save_file_name, dpi=300)
		if display:
			plt.show()

	def calc_yspacing(self, ys):
		lastys = self.df[ys].iloc[-1]
		lastys = lastys.to_frame('lasty')
		lastys = lastys.sort_values(by=['lasty'],ascending=True)
		lastys['ypad']=0
		#add padding
		padmultiplier = 1 
		#set remaining two paddings
		for i in range(1,len(ys)):
			valuedistance = lastys.iloc[i]['lasty'] - lastys.iloc[i-1]['lasty']
			if valuedistance < 250000:
				#add padding if too close
				lastys.at[lastys.iloc[i].name,'ypad'] = 5 * padmultiplier
				#increase multiplier in event that multiple values are too close together
				padmultiplier += 1
			else:
				#reset multiplier to 1 if there is a label that doesnt need a multiplier
				padmultiplier = 1
		return lastys

	def multi_yoy_annotate(self,ys,key,annotation_fxn):
		#takes a key referenced by y column name and with columns labelname, color
		lastys = self.calc_yspacing(ys)
		for i in range(len(ys)):
			y = lastys.iloc[i].name
			self.annotate(x='month',
				y=y,
				num_annotation=annotation_fxn(y=y),
				legend_label=key.loc[y,'labelname'],
				label_color=key.loc[y,'color'],
				xpad=75, 
				ypad=lastys.iloc[i].ypad)






