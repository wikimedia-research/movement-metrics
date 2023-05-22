import pandas as pd
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.font_manager
import os
from os.path import dirname
import sys
#local
from wikicharts import Wikichart, wmf_colors
#jupyter notebook
#%run wikicharts.ipynb

def main():
    print("Generating Active Editors chart...")

    #---PARAMETERS---
    #current path
    home_dir = os.getcwd()
    #where file is saved
    outfile_name = "Active_Editors.png"
    save_file_name = home_dir + "/charts/" + outfile_name
    #note for labeling the YoY highlight
    yoy_note = " "
    #display or note
    display_flag = True

    #---CLEAN DATA--
    #read in data
    try:
        df = pd.read_csv(data_path, sep='\t')
    except:
        df = pd.read_csv(home_dir + '/resources/data/editor_metrics.tsv', sep='\t')
    #df = pd.read_csv("../metrics/metrics.tsv', sep='\t')
    #note start and end dates may be different depending on chart_type
    start_date = "2019-01-01"
    end_date = datetime.today()
    #convert string to datetime
    df['month'] = pd.to_datetime(df['month'])
    #truncate data to period of interst
    df = df[df["month"].isin(pd.date_range(start_date, end_date))]

    #---MAKE CHART---
    chart = Wikichart(start_date,end_date,df)
    chart.init_plot()
    chart.plot_line('month','active_editors',wmf_colors['blue'])
    chart.plot_monthlyscatter('month','active_editors',wmf_colors['blue'])
    chart.plot_yoy_highlight('month','active_editors')
    chart.format(title = 'Active Editors',
        data_source="https://github.com/wikimedia-research/Editing-movement-metrics")
    chart.annotate(x='month',
        y='active_editors',
        num_annotation=chart.calc_yoy(y='active_editors',yoy_note=yoy_note))
    chart.finalize_plot(save_file_name,display=display_flag)

if __name__ == "__main__":
    main()
