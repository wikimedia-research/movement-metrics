import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#---READ IN CSV---
df = pd.read_csv('corrected_metrics.csv')

#display top rows for preview
#pd.options.display.max_rows = 5
#print(df)
#df.head()
#list(df.columns)

#---CLEAN DATA--
#look at data types
#print(df.total_pageview.dtype)
#print(df.total_pageview_corrected.dtype)

#remove commas
df["total_pageview"] = df["total_pageview"].str.replace(",","")

#convert string to int
df['total_pageview'] = df['total_pageview'].astype(str).astype(int)

#convert string to datetime
df['month'] = pd.to_datetime(df['month'])

#---GET DATA SUBSETS--
#add column for corrected vs. data loss period
truncated_df = df[df["month"].isin(pd.date_range("2018-05-01", "2022-10-01"))]
data_loss_df = df[df["month"].isin(pd.date_range("2021-05-01", "2022-02-01"))]
before_data_loss = df[df["month"].isin(pd.date_range("2018-05-01", "2021-05-01"))]
after_data_loss = df[df["month"].isin(pd.date_range("2022-02-01", "2022-10-01"))]
october_df = truncated_df[truncated_df['month'].dt.month == 10]
#for highlighting
highlighted_months = df[df['month'].isin(['2019-10-01','2022-10-01'])]


#---PLOT---
oct_fig = go.Figure()
#add in blue dotted line for data loss corrected
oct_fig.add_trace(go.Scatter(
    x = data_loss_df['month'], 
    y = data_loss_df['total_pageview_corrected'],
    name='Total Pageviews (Corrected)',
    fill=None,
    mode='lines', 
    line_dash='dash',
    line_color='#3366CC')) #blue
#add in gray dotted line for data loss uncorrected 
oct_fig.add_trace(go.Scatter(
    x = data_loss_df['month'], 
    y = data_loss_df['total_pageview'],
    name='Data Loss',
    fill='tonexty', # fill area between trace0 and trace1
    mode='lines', 
    line_color='#FFFFFF',
    fillcolor='#eeeeee',
    showlegend=False))
oct_fig.add_trace(go.Scatter(
    x = data_loss_df['month'], 
    y = data_loss_df['total_pageview'],
    name='Total Pageviews (Uncorrected)',
    fill=None,
    mode='lines', 
    line_dash='dash',
    line_color='#999999')) #dark gray
#add dots for October
oct_fig.add_trace(go.Scatter(
    x = october_df['month'], 
    y = october_df['total_pageview_corrected'],
    name='October',
    mode='markers',
    marker_color='#3366CC',
    marker_size=10)) #
#add in line for everything except data loss period
oct_fig.add_trace(go.Scatter(
    x = before_data_loss['month'], 
    y = before_data_loss['total_pageview'],
    name='Total Pageviews',
    fill=None,
    mode='lines', 
    line_color='#3366CC')) #
oct_fig.add_trace(go.Scatter(
    x = after_data_loss['month'], 
    y = after_data_loss['total_pageview'],
    name='Total Pageviews',
    fill=None,
    mode='lines', 
    line_color='#3366CC',
    showlegend=False)) #blue
#add highlight circles
oct_fig.add_trace(go.Scatter(
    x = highlighted_months['month'], 
    y = highlighted_months['total_pageview'],
    name='Total Pageviews',
    mode='markers', 
    marker=dict(
            color='rgba(0,0,0,0)',
            size=30,
            line=dict(
                color='#FFF019',
                width=2
            )),
    showlegend=False))

#---STYLE---
#general style
oct_fig.update_layout({
	'title':'Content Interactions (October)',
	'font_family':"Arial",
    'font_size': 18,
	'title_font_family':'Arial',
	'title_x':0.5,
    'title_font_size': 25,
	'legend_font_family':'Arial',
	'xaxis_title':"Month",
    'yaxis_title':"Pageviews",
    'legend_title':"Pageview Type",
	'plot_bgcolor':'rgba(0,0,0,0)',
	'paper_bgcolor':'rgba(0,0,0,0)'})

#style legend
oct_fig.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-0.25,
    xanchor="center",
    x=0.5)) #traceorder="reversed"
oct_fig.update_layout(legend_title_font=dict(
    size=18))

#add margins
oct_fig.update_layout(
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
oct_fig.update_xaxes(showgrid=False, gridwidth=1, title_font_family="Arial", gridcolor='#EBF3FF')
oct_fig.update_yaxes(showgrid=True, gridwidth=1, title_font_family="Arial", gridcolor='#EBF3FF')

#x-axis time serieslabels
#oct_fig.update_layout(xaxis_range=[truncated_df['month'].iat[0],truncated_df['month'].iat[-1]])
#oct_fig.update_xaxes(
#    dtick='M12',
#    tickformat="%Y")

#---ADD ANNOTATIONS
#add note for recent uptick
oct_fig.add_annotation(
	x=df['month'].iat[-1],
	y=df['total_pageview'].iat[-1],
	font=dict(
        family="Arial",
        size=14,
        color='#18A558'),
	text="+11.6% YoY largely due to rise in automated traffic",
	showarrow=True,
	arrowhead=1,
	arrowcolor='#18A558')

#add data annotation
oct_fig.add_annotation(
	xref='paper',
	yref='paper',
	x=0,
	y=-0.3,
	font=dict(
        family="Arial",
        size=8,
        color='#9AA0A7'),
	text="Graph Notes: Created 12/2/22 by Hua Xi using data from https://github.com/wikimedia-research/Readers-movement-metrics/blob/main/04-Visualization/corrected_metrics.csv",
	showarrow=False)

oct_fig.show()

