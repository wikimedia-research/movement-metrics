import pandas as pd
import calendar
from datetime import date
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import math
from math import ceil
from math import floor
import numpy as np
import os
from PIL import ImageFont
import re
import warnings


#---CUSTOM DICTIONARIES
wmf_colors = {'black75':'#404040','black50':'#7F7F7F','black25':'#BFBFBF','base80':'#eaecf0','orange':'#EE8019','base70':'#c8ccd1','red':'#970302','pink':'#E679A6','green50':'#00af89','purple':'#5748B5','blue':'#0E65C0','brightblue':'#049DFF','brightbluelight':'#C0E6FF','yellow':'#F0BC00','green':'#308557','brightgreen':'#71D1B3'}
parameters = {'month_interest': 2,'author':'Hua Xi'}
style_parameters = {'font':'Montserrat','title_font_size':24,'text_font_size':14}


#---HELPER FUNCTIONS---
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
	elif order >= 3:
		multiplier = float('1e-3')
		formatting = '{:1.2f}K'
	else:
		multiplier = 1
		formatting = '{:1.0f}'
	return multiplier, formatting

#takes a dataframe and splits it into sets of four columns (for plotting multiple charts per figure)
#keeps the index column as the first column in each split dataframe
def split_df_by_col(df, index_column_name = "month", cols_per_df = 4):
	num_charts = len(df.columns) - 1
	num_figures = ceil(num_charts / cols_per_df)
	index_column = df.columns.get_loc(index_column_name)
	dfs = []
	for f in range(num_figures):
		#get a list consisting of the 0th column and the 4 columns going on the figure i
		col_start = f * cols_per_df
		col_end = min(col_start + cols_per_df,num_charts + 1)
		#list of four columns going on figure i
		cols = [index_column] + list(range(col_start,col_end))
		#remove duplicates
		cols = list(set(list(cols)))
		#create the new df and set the index
		new_df = df.iloc[:, cols]
		#new_df = new_df.reset_index(index_column_name)
		dfs.append(new_df)
	return dfs

#generate a set of key tables for a set of dfs
def gen_keys(dfs, key_colors, index_column_name = "month"):
	keys = []
	num_colors = len(key_colors)
	c = 0
	for subdf in dfs:
		variables = list(subdf.columns)
		variables.remove("month")
		new_key_values = []
		for col in variables:
			if c == 0:
				new_key_values.append([col, key_colors[c]])
			else:
				new_key_values.append([col, key_colors[(c % num_colors)]])
			c += 1
		new_key = pd.DataFrame(new_key_values, index=variables, columns=['labelname','color'])
		keys.append(new_key)
	return keys

#find number closest to n divisible by m
def closestdivisible(n, m) :
    # Find the quotient
    q = int(n / m)
    # 1st possible closest number
    n1 = m * q
    # 2nd possible closest number
    if((n * m) > 0) :
        n2 = (m * (q + 1))
    else :
        n2 = (m * (q - 1))
    # if true, then n1 is the required closest number
    if (abs(n - n1) < abs(n - n2)) :
        return n1
    # else n2 is the required closest number
    return n2

#take a df and create a parallel df of rolling averages
def roll(df, rolling_months = 3, index_column_name = "month"):
	rolled = df.set_index('month').rolling(rolling_months).mean().reset_index().dropna()
	return rolled

#---BASIC CHART---
#the wrapper's main functionality is in the formatting and annotation
#the plotting functions could actually probably be deleted bc they just repeat matplotlib's functions

class Wikichart:
	#initialize chart object
	def __init__(self,start_date, end_date,dataset,month_interest=parameters['month_interest'],yoy_highlight=None):
		self.start_date = start_date
		self.end_date = end_date
		self.month_interest = month_interest
		self.month_name = calendar.month_name[month_interest]
		self.df = dataset
		self.fig = None
		self.ax = None
		self.yranges = []
		self.ynumticks = []

	'''
	def get_inputs(self, script_dir, outfile_name = "Chart", annotation_note = "", display_flag = True):
		outfile_name = "Regional_Active_Editors"
		outfile_name = input('Outfile_name:\n')
		yoy_note = input('YoY annotation note (default is blank):\n')
		input1 = input()
	'''

	#initialize a figure of given height width and number of subplots
	def init_plot(self,width=10,height=6,subplotsx=1,subplotsy=1,fignum=0):
		#plt.figure(figsize=(width, height))
		self.fig, self.ax = plt.subplots(subplotsx,subplotsy, num=fignum)
		self.fig.set_figwidth(width)
		self.fig.set_figheight(height)

	#---PLOTTING FUNCTIONS---
	#basic line
	def plot_line(self, x, y, col, legend_label ='_nolegend_',linewidth = 2):
		plt.plot(self.df[str(x)], self.df[str(y)],
			label=legend_label,
			color=col,
			zorder=3,
			linewidth=linewidth)

	#dots to indicate a given month
	def plot_monthlyscatter(self, x, y, col, month=parameters['month_interest'], legend_label ='_nolegend_'):
		#dots on month of interest
		monthly_df = self.df[self.df[str(x)].dt.month == month]
		plt.scatter(monthly_df[str(x)], monthly_df[str(y)],
			label=legend_label,
			color=col,
			zorder=4)
			#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5

	#yellow circles to highlight a YoY
	def plot_yoy_highlight(self, x, y, highlight_radius = 1000, col = wmf_colors['yellow'], legend_label ='_nolegend_'):
		yoy_highlight = pd.concat([self.df.iloc[-13,:],self.df.iloc[-1,:]],axis=1).T
		#dots on month of interest
		plt.scatter(yoy_highlight[str(x)], yoy_highlight[str(y)],
			label=legend_label,
			s=highlight_radius,
			facecolors='none',
			edgecolors=col,
			zorder=5)
			#note: due to a bug in matplotlib, the grid's zorder is fixed at 2.5 so everything plotted must be above 2.5

	#grayed out area to represent data loss
	def plot_data_loss(self, x, y1, y2, data_loss_df, col = wmf_colors['base80'], legend_label ='_nolegend_'):
		plt.fill_between(data_loss_df[str(x)], data_loss_df[str(y1)], data_loss_df[str(y2)],
			label=legend_label,
			color=col,
			edgecolor=col,
			zorder=3)

	#draws a rectangle to block off a set of dates
	def block_off(self,axis, blockstart, blockend, xbuffer = 7):
		#convert dates to x axis coordinates
		xstart = mdates.date2num(blockstart)
		xend = mdates.date2num(blockend)
		block_width = xend - xstart

		#get height
		ymin, ymax = axis.get_ylim()
		block_height = ymax - ymin

		#plot rectangle
		matplotlib.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
		rect = Rectangle((xstart - xbuffer, ymin), block_width + 2 * xbuffer, block_height, 
			linewidth=0, #no edge around rectangle
			hatch='////',
			edgecolor=wmf_colors['black75'], #hatch color
			facecolor='white', #bg color
			zorder=10)
		axis.add_patch(rect) 

	#---FORMATTING FUNCTIONS---
	#basic formatting — title, bottom note, axis formatting, gridlines
	def format(self, title, author=parameters['author'], data_source="N/A",ybuffer=True,format_x_yearly=True,radjust=0.85,ladjust=0.1,tadjust=0.9,badjust=0.1,titlepad=0):
		#add gridlines
		plt.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
		#format title
		custom_title = f'{title} ({calendar.month_name[self.month_interest]})'
		plt.title(custom_title,font=style_parameters['font'],fontsize=style_parameters['title_font_size'],weight='bold',loc='left',wrap=True,pad=titlepad)
		#remove bounding box
		for pos in ['right', 'top', 'bottom', 'left']:
			plt.gca().spines[pos].set_visible(False)
		#expand bottom margin (to make room for author and data source annotation)
		plt.subplots_adjust(bottom=badjust, right = radjust, left=ladjust, top=tadjust)
		#buffer y-axis range to be 2/3rds of the total y axis range
		#note: gca = get current axis
		if ybuffer == True:
			ax = plt.gca()
			current_ymin, current_ymax = ax.get_ylim()
			current_yrange = current_ymax - current_ymin
			new_ymin = current_ymin - current_yrange / 4
			#if the currentymin is already negative, do nothing
			if current_ymin > 0 :		
				#if the new ymin is positive, increase to have 2/3 buffer
				if new_ymin >= 0:
					new_ymax = new_ymin + current_yrange * 1.5
				#if the new_ymin is negative, expand the yrange to have a minimum of zero and corresponding increase above the plot
				else:
					new_ymin = 0
					new_ymax = current_ymin + current_ymax
				ax.set_ylim([new_ymin, new_ymax])
		#format x-axis labels — yearly x-axis labels on January
		if format_x_yearly == True:
			plt.xticks(fontname=style_parameters['font'],fontsize=style_parameters['text_font_size'])
			date_labels = []
			date_labels_raw = pd.date_range(self.start_date, self.end_date, freq='AS-JAN')
			for dl in date_labels_raw:
				date_labels.append(datetime.strftime(dl, '%Y'))
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

	#annotate the end of the plotted line
	def annotate(self, x, y, num_annotation, legend_label="", label_color='black', xpad=0, ypad=0,zorder=10):
		#legend annotation
		#note that when legend_label="", xpad should be 0 (only a numerical annotation is produced)
		plt.annotate(legend_label,
			xy = (self.df[str(x)].iat[-1],self.df[str(y)].iat[-1]),
			xytext = (20+xpad,-5+ypad),
			xycoords = 'data',
			textcoords = 'offset points',
			color=label_color,
			fontsize=style_parameters['text_font_size'],
			weight='bold',
			family=style_parameters['font'],
			bbox=dict(pad=5, facecolor="white", edgecolor="none"),
			zorder=zorder)
		#increase xpad for numerical annotation if legend annotation is present (prevent overlap)
		num_xpad = xpad
		if(len(legend_label) > 0):
			try:
				font = ImageFont.truetype('Montserrat-Bold.ttf', style_parameters['text_font_size'])
				labelsize = font.getsize(legend_label)
				num_xpad= xpad + labelsize[0] + 5
				print("labelsize: " + str(labelsize[0]))
			except:
				num_xpad = xpad + len(legend_label) * 4
		print("num_xpad: " + str(num_xpad))
		#numerical annotation
		plt.annotate(num_annotation,
			xy = (self.df[str(x)].iat[-1],self.df[str(y)].iat[-1]),
			xytext = (20+num_xpad,-5+ypad),
			xycoords = 'data',
			textcoords = 'offset points',
			color='black',
			fontsize=style_parameters['text_font_size'],
			weight='bold',
			wrap=True,
			family=style_parameters['font'])

	#annotation helper function
	def calc_yoy(self,y,yoy_note=""):
		yoy_highlight = pd.concat([self.df.iloc[-13,:],self.df.iloc[-1,:]],axis=1).T
		yoy_change_percent = ((yoy_highlight[str(y)].iat[-1] - yoy_highlight[str(y)].iat[0]) /  yoy_highlight[str(y)].iat[0]) * 100
		if math.isnan(yoy_change_percent):
			yoy_annotation = "YoY N/A"
		elif yoy_change_percent > 0:
			yoy_annotation = f" +{yoy_change_percent:.1f}% YoY" + " " + yoy_note
		else:
			yoy_annotation = f" {yoy_change_percent:.1f}% YoY" + " " + yoy_note
		return(yoy_annotation)

	#annotation helper function
	def calc_finalcount(self,y,yoy_note=""):
		final_count = self.df[str(y)].iat[-1]
		multiplier, formatting = calc_order_format(final_count)
		count_annotation = y_label_formatter(value = final_count,multiplier = multiplier,format_text=formatting)
		return(count_annotation)

	#annotation helper function
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

	#annotate a single chart with multiple lines
	def multi_yoy_annotate(self,ys,key,annotation_fxn,x='month',xpad=0):
		#takes a key referenced by y column name and with columns labelname, color
		lastys = self.calc_yspacing(ys)
		for i in range(len(ys)):
			y = lastys.iloc[i].name
			self.annotate(x=x,
				y=y,
				num_annotation=annotation_fxn(y=y),
				legend_label=key.loc[y,'labelname'],
				label_color=key.loc[y,'color'],
				xpad=xpad, 
				ypad=lastys.iloc[i].ypad)

	#add a custom note at the top of the chart under the title
	def top_annotation(self, x = 0.05, y =0.87, annotation_text = ""):
		plt.figtext(x, y, annotation_text, family=style_parameters['font'],fontsize=10, color= wmf_colors['black75'])

	#add blocked out area to legend — alternative is to use '///' string
	def add_legend(self,legend_fontsize=14):
		matplotlib.rcParams['legend.fontsize'] = legend_fontsize
		plt.legend(frameon=False,
			loc ="upper center",
			bbox_to_anchor=(0.5, -0.15, ),
			fancybox=False, 
			shadow=False,
			ncol=4, 
			prop={"family":style_parameters['font']})

	#add blocked out area to legend — alternative is to use '///' string
	def add_block_legend(self):
		self.fig.patches.extend([plt.Rectangle((0.05, 0.868), 0.01, 0.02,
			linewidth=0.1, #no edge around rectangle
			hatch='//////',
			edgecolor='black', #hatch color
			facecolor='white', #bg color
			zorder=100,
			transform=self.fig.transFigure,
			figure = self.fig)])
		#self.ax[0][1].add_patch(rect) 

	#---SHOW AND SAVE---
	def finalize_plot(self, save_file_name, display=True):
		plt.savefig(save_file_name, dpi=300)
		if display:
			plt.show()
	
	#---MULTI-CHART FIGURES
	#plot lines on subplots
	def plot_subplots_lines(self, x, key, linewidth=2, num_charts=4, subplot_title_size = 12):
		#remove bounding box
		i = 0
		for row in self.ax:
			for axis in row:
				if i < num_charts:
					region_label = key.iloc[i]['labelname']
					region_color = key.iloc[i]['color']
					axis.plot(self.df['month'], 
						self.df[region_label],
						label='_no_legend_,',
						color=region_color,
						zorder=3,
						linewidth=linewidth)
					axis.set_title(region_label,fontfamily=style_parameters['font'],fontsize=subplot_title_size)
				i += 1

	#draws a rectangle to block off a set of dates
	def block_off_multi(self,blockstart, blockend, xbuffer = 6):
		for row in self.ax:
			for axis in row:
				self.block_off(axis,blockstart, blockend, xbuffer)

	#formatting across multichart figures
	def format_subplots(self, title, key, author=parameters['author'], data_source="N/A", radjust=0.85, ladjust=0.1,tadjust=0.85,badjust=0.1, num_charts=4,tickfontsize=12,mo_in_title=True):
		#expand bottom margin
		plt.subplots_adjust(bottom=badjust, right = radjust, left=ladjust, top=tadjust, wspace=0.2, hspace=0.4)
		#count number of charts and stop when num_charts is hit
		i = 0
		for row in self.ax:
			for axis in row:
				if i < num_charts:
					#remove bounding box
					axis.set_frame_on(False)
					#gridlines
					axis.grid(axis = 'y', zorder=-1, color = wmf_colors['black25'], linewidth = 0.25)
					#format x axis labels
					axis.set_xticklabels(axis.get_xticklabels(),fontfamily=style_parameters['font'],fontsize=tickfontsize)
					#format x axis labels to show year only
					xaxisFormatter = mdates.DateFormatter('%Y')
					axis.xaxis.set_major_formatter(xaxisFormatter)
					#format y axis labels
					current_values = axis.get_yticklabels()
					new_labels = []
					#format in abbreviated notation
					for y_label in current_values:
						y_value = float(y_label.get_position()[1])
						y_order, y_label_format = calc_order_format(y_value)
						new_label = y_label_formatter(y_value, y_order, y_label_format)
						new_labels.append(new_label)
					'''
					#if 0 is the bottom label, remove aka don't label at all
					print(type(new_labels[0]))
					if new_labels[0] == str(0):
						new_labels[0] = ""
					'''
					axis.set_yticklabels(new_labels,fontfamily=style_parameters['font'],fontsize=tickfontsize)
				else:
					#make invisible if outside of num_charts
					axis.set_visible(False)
				i += 1
		#add title and axis labels
		#note there seems to be a bug with ha and va args to suptitle, so just set x and y manually
		if mo_in_title:
			figure_title = f'{title} ({calendar.month_name[self.month_interest]})'
		else:
			figure_title = f'{title}'
		self.fig.suptitle(figure_title,ha='left',x=0.05,y=0.97,fontsize=style_parameters['title_font_size'],fontproperties={'family':style_parameters['font'],'weight':'bold'})
		#add bottom annotation
		today = date.today()
		plt.figtext(0.05,0.01, "Graph Notes: Created by " + str(author) + " " + str(today) + " using data from " + str(data_source), fontsize=8, va="bottom", ha="left", color=wmf_colors['black25'], fontproperties={'family':style_parameters['font']})
	
	#show only bottom and top ylabel, set to bold
	def clean_ylabels_subplots(self,tickfontsize=12):
		#count number of charts and stop when num_charts is hit
		i = 0
		for row in self.ax:
			for axis in row:
				current_labels = axis.get_yticklabels()
				new_labels = ['']*len(current_labels)
				new_labels[0] = current_labels[0]
				new_labels[-1] = current_labels[-1]
				axis.set_yticklabels(new_labels,fontfamily=style_parameters['font'],fontsize=tickfontsize, weight='bold')
				i += 1	

	#set every subplot to the same ymin and ymax
	def standardize_subplotyaxis(self, ymin, ymax, num_charts=4):
		i = 0
		for row in self.ax:
			for axis in row:
				if i < num_charts:
					axis.set_ylim([ymin, ymax])
				i += 1

	#set yrange for a single chart plot
	def standardize_yrange(self, yrange, num_ticks,std_cutoff=15):
		#get the standard y interval
		std_yinterval = yrange / (num_ticks - 1)
		ax = plt.gca()
		current_ymin, current_ymax = ax.get_ylim()
		current_yrange = current_ymax - current_ymin
		if current_yrange > (yrange / std_cutoff):
			current_ymedian = current_ymin + ((current_ymax - current_ymin) / 2)
			if (num_ticks % 2) == 0:
				#for final even num ticks
				new_ymedian = closestdivisible(current_ymedian, std_yinterval)
				if new_ymedian < current_ymedian:
					new_ymin = new_ymedian - (std_yinterval * (num_ticks / 2 - 1))
				else:
					new_ymin = new_ymedian - (std_yinterval * (num_ticks / 2))
			else:
				#for final odd number of ticks 
				new_ymedian = closestdivisible(current_ymedian, std_yinterval)
				new_ymin = new_ymedian - (yrange / 2)
			#set min to 0 if negative
			new_ymin = max(0, new_ymin)
			#set ymax
			new_ymax = new_ymin + yrange
			ax.set_ylim(new_ymin, new_ymax)

	#set every subplot to the same yrange and intervals
	#std_cutoff is a number where if the current yrange < (std_cutoff x std_yrange), then we don't standardize it; used to keep natural range for very small ranged plots
	def standardize_subplotyrange(self, yrange, num_ticks, num_charts=4, std_cutoff=15):
		#get the standard y interval
		std_yinterval = yrange / (num_ticks - 1)
		#keep track of chart num
		i = 0
		#minorLocator = ticker.MultipleLocator(yspacing)
		for row in self.ax:
			for axis in row:
				if i < num_charts:
					#get current y range
					current_ymin, current_ymax = axis.get_ylim()
					current_yrange = current_ymax - current_ymin
					if current_yrange > (yrange / std_cutoff):
						current_ymedian = current_ymin + ((current_ymax - current_ymin) / 2)
						if (num_ticks % 2) == 0:
							#for final even num ticks
							new_ymedian = closestdivisible(current_ymedian, std_yinterval)
							if new_ymedian < current_ymedian:
								new_ymin = new_ymedian - (std_yinterval * (num_ticks / 2 - 1))
							else:
								new_ymin = new_ymedian - (std_yinterval * (num_ticks / 2))
						else:
							#for final odd number of ticks 
							new_ymedian = closestdivisible(current_ymedian, std_yinterval)
							new_ymin = new_ymedian - (yrange / 2)
						#set min to 0 if negative
						new_ymin = max(0, new_ymin)
						#set ymax
						new_ymax = new_ymin + yrange
						axis.set_ylim(new_ymin, new_ymax)
						#axis.yaxis.set_major_locator(ticker.MultipleLocator(yspacing))
						#axis.Axis.set_minor_locator(minorLocator)
				i += 1

	def get_ytickrange(self):
		ticks = self.ax.get_yticklabels()
		tick_range = ticks[-1].get_position()[1] - ticks[0].get_position()[1]
		return tick_range

	#returns the subplot with the max range, and its corresponding number of ticks
	#need to change to getting max tick range
	def get_maxyrange(self):
		for row in self.ax:
			for axis in row:
				#note that the axis limits are not necessarily the range displayed by the min and max ticks
				#the axis limits might slightly wider than the min-max tick range — we use the min max tick range to ensure congruity btw charts
				#gets the tick range
				ticks = axis.get_yticklabels()
				tick_range = ticks[-1].get_position()[1] - ticks[0].get_position()[1]
				self.yranges.append(tick_range)
				#get tick intervals
				self.ynumticks.append(len(ticks))
		maxrange = max(self.yranges)
		maxrange_index = self.yranges.index(maxrange)
		maxrange_numticks = self.ynumticks[maxrange_index]
		return maxrange, maxrange_numticks

	def expand_yrange(self):
		'''
		print("initial yrange " + str(axis.get_ylim()))
		print("initial tick num " + str(len(axis.get_yticklabels())))
		current_ticks = axis.get_yticklabels()
		current_tick_range = current_ticks[-1].get_position()[1] - current_ticks[0].get_position()[1]
		print("initial tick range " + str(current_tick_range))
		#expands the axis limits via the 2/3rds rule
		#expanding the ylim via set_ylim will recalibrate ticks automatically
		current_ylim = axis.get_ylim()
		current_ylim_range = current_ylim[1] - current_ylim[0]
		print(current_ylim_range)
		current_ticknum = len(axis.get_yticklabels())
		new_ymin = current_ylim[0] - current_ylim_range / 4
		new_ymax = current_ylim[1] + current_ylim_range / 4
		axis.set_ylim([new_ymin, new_ymax])
		print("expanded yrange " + str(axis.get_ylim()))
		print("expanded tick num " + str(len(axis.get_yticklabels())))
		'''









