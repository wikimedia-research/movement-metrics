import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

#---PLOT---
data_loss_fig = go.Figure()
data_loss_fig.add_trace(go.Scatter(
	x = data_loss_df['month'], 
	y = data_loss_df['total_pageview'],
	name='Data Loss (Reference Only)',
    fill=None,
    mode='lines',
    line_color='#EF8891', #light red
    showlegend=False)) #do not show in legend
data_loss_fig.add_trace(go.Scatter(
    x = data_loss_df['month'], 
    y = data_loss_df['total_pageview_corrected'],
    name='Data Loss',
    fill='tonexty', # fill area between trace0 and trace1
    mode='lines', 
    line_color='#EF8891',
    fillcolor='#EF8891')) #light red
data_loss_fig.add_trace(go.Scatter(
    x = data_loss_df['month'], 
    y = data_loss_df['total_pageview_corrected'],
    name='Total Pageviews (Corrected)',
    fill=None,
    mode='lines', 
    line_color='#3366CC'))
#data_loss_fig.show()

#---STYLE---
#general style
data_loss_fig.update_layout({
	'title':'Pageviews with Data Loss Corrected',
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
data_loss_fig.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-0.2,
    xanchor="center",
    x=0.5,
    traceorder="reversed"))

#add margins
data_loss_fig.update_layout(
	autosize=False,
	width=1200,
    height=750,
    margin=dict(
        l=100,
        r=100,
        b=200,
        t=100,
        pad=5
    ),
)

#grid lines
data_loss_fig.update_xaxes(showgrid=False, gridwidth=1, title_font_family="Arial", gridcolor='#EBF3FF')
data_loss_fig.update_yaxes(showgrid=True, gridwidth=1, title_font_family="Arial", gridcolor='#EBF3FF')

#---ADD ANNOTATIONS
#add note for recent uptick
data_loss_fig.add_annotation(
	x=data_loss_df['month'].iat[-1],
	y=data_loss_df['total_pageview'].iat[-1],
	font=dict(
        family="Arial",
        size=12,
        color='#18A558'),
	text="+11.6% YoY largely due to rise in automated traffic",
	showarrow=True,
	arrowhead=1,
	arrowcolor='#18A558')

#add data annotation
data_loss_fig.add_annotation(
	xref='paper',
	yref='paper',
	x=0,
	y=-0.25,
	font=dict(
        family="Arial",
        size=8,
        color='#9AA0A7'),
	text="Graph Notes: Created 12/2/22 by Hua Xi using data from https://github.com/wikimedia-research/Readers-movement-metrics/blob/main/04-Visualization/corrected_metrics.csv",
	showarrow=False)

data_loss_fig.show()

