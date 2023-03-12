import pandas as pd
import plotly.express as px

#---READ IN CSV---
data_loss_df = pd.read_csv('corrected_metrics.csv')

#display top rows
#pd.options.display.max_rows = 5
#print(data_loss_df)
#data_loss_df.head()

#---CONVERT COLUMNS TO INT---
#checkdata type
#print(data_loss_df.total_pageview.dtype)
#print(data_loss_df.total_pageview_corrected.dtype)

#remove commas
data_loss_df["total_pageview"] = data_loss_df["total_pageview"].str.replace(",","")

#convert to int
data_loss_df['total_pageview'] = data_loss_df['total_pageview'].astype(str).astype(int)

#---PLOT LINES---
#Total Pageview Linechart (without correction)
data_loss_fig = px.line(data_loss_df, 
	x = 'month', 
	y = ['total_pageview','total_pageview_corrected'], 
	title='Pageviews with Data Loss',
	color_discrete_map={"total_pageview": "#9AA0A7","total_pageview_corrected": "#3366CC"})


#---PLOT FILL---



#---STYLE---
#general style
data_loss_fig.update_layout({
	'font_family':"Arial",
	'title_font_family':'Arial',
	'title_x':0.5,
	'legend_font_family':'Arial',
	'xaxis_title':"Month",
    'yaxis_title':"Pageviews",
    'legend_title':"Pageview Type",
	'plot_bgcolor':'rgba(0,0,0,0)',
	'paper_bgcolor':'rgba(0,0,0,0)'})

#style legend
#update legend names
newnames = {'total_pageview': 'Data Loss', 'total_pageview_corrected': 'Total Pageviews (Corrected)'}
data_loss_fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
data_loss_fig.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-0.16,
    xanchor="center",
    x=0.5,
    traceorder="reversed"
))

#grid lines
data_loss_fig.update_xaxes(showgrid=False, gridwidth=1, title_font_family="Arial", gridcolor='#EBF3FF')
data_loss_fig.update_yaxes(showgrid=True, gridwidth=1, title_font_family="Arial", gridcolor='#EBF3FF')

data_loss_fig.show()



