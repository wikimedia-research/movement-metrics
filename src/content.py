import pandas as pd
import numpy as np
from pathlib import Path
from src.utils import load_metric_file
from src.utils import subtract_year

# Define a function to map categories to the new categories
def map_gender_category(category):
    if category in ['male', 'cisgender male']:
        return 'male'
    elif category in ['female', 'cisgender female']:
        return 'female'
    else:
        return 'gender_diverse'


def filter_wikis(df, url):
    df = pd.read_csv(url, parse_dates=["time_bucket"]).set_index('time_bucket').rename_axis('month').to_period(freq='M')    
    wikis=pd.read_csv('data/wikis')
    df = df[df['wiki_db'].isin(list(wikis['database_code']))]
    

    return df 


def process_quality_data(df, old):
    if df['category'].isin(['female']).any():
        df['category']=df['category'].apply(map_gender_category) # apply gender mapping correction for gender dataset

    
    df = df.groupby(['month', 'category'])['standard_quality_count_value'].sum().reset_index()
    df = df.pivot(index='month', columns='category',  values='standard_quality_count_value')

    
    # Filter and rename the columns
    rename_dict = {col: f"{col} total" for col in df.columns}
    df = df.rename(columns=rename_dict)

    # Identify the latest 'time' in old_geo_data

    latest_time = old.index.max()
    filtered_rows = df[df.index > latest_time]

    #Append udpated rows
    updated_df = pd.concat([old, filtered_rows], axis=0, sort=False)
    
    

    return updated_df


def calculate_mom(df):
    df = df.copy()
    
    # Create list underrepresented categories based on which dataframe is being processed.
    if 'female total' in df.columns:
        
        minority_label = 'female + gender_diverse'
        majority_label = 'all_genders_sum'
        topic = 'about gender minorities'
        
        underrepresented = ["female_MoM_difference", "gender_diverse_MoM_difference"]

    else:
        minority_label = 'underrepresented_regions_sum'
        majority_label = 'all_regions_sum'
        topic = 'about underrepresented regions'
        
        underrepresented = ["East, Southeast Asia, & Pacific_MoM_difference", "Latin America & Caribbean_MoM_difference", "Middle East & North Africa_MoM_difference" , "South Asia_MoM_difference", "Sub-Saharan Africa_MoM_difference"]
        
    
    # Compute the MoM difference
    for column in df.columns:
        if 'total' in column:
            new_column_name = column.replace(' total', '_MoM_difference')
            df[new_column_name] = df[column].diff()

    # Make a list of all the MoM columns
    mom_total = [column for column in df.columns if 'MoM_difference' in column]

    # Create sum column for MoM difference values across underrepresented categories
    df[f'{minority_label}'] = df[underrepresented].sum(axis=1)
    
    # Create sum column of all MoM difference values across all regions
    df[f'{majority_label}'] = df[mom_total].sum(axis=1)
    
    # Get the % of underrepresented out of total articles
    df[f'% of new articles {topic}'] =df[f'{minority_label}'] / df[f'{majority_label}']
    
    df = df.iloc[:-1] # Remove last row as it always contains partial data of the month the snapshot was taken.
   
    return df




def calc_content_rpt(df, reporting_period, minorities, totals, index_names):
    
    one_year_earlier = subtract_year(reporting_period)
    one_year_earlier_next_month = one_year_earlier + 1

    forecast_data = {}
    for column in df.columns:
        one_year_ago_value = df.at[one_year_earlier, column]
        one_year_ago_next_month_value = df.at[one_year_earlier_next_month, column]

        if one_year_ago_value == 0:
            last_year_diff = 0
        else:
            last_year_diff = (one_year_ago_next_month_value - one_year_ago_value) / one_year_ago_value

        forecast_col = f"{column}_forecast"
        forecast_data[forecast_col] = df.at[reporting_period, column] * (1 + last_year_diff)

    current_ratios = {}
    forecasted_ratios = {}
    
    for minor, total, index_name in zip(minorities, totals, index_names):
        current_ratios[index_name] = df.at[reporting_period, minor] / df.at[reporting_period, total]
        forecasted_ratios[index_name] = forecast_data[f"{minor}_forecast"] / forecast_data[f"{total}_forecast"]

    # Convert the dictionaries to DataFrames
    current_df = pd.DataFrame(current_ratios, index=["value"])
    forecast_df = pd.DataFrame(forecasted_ratios, index=["naive forecast"])

    # Concatenate the DataFrames vertically
    result_df = pd.concat([current_df, forecast_df])

    return result_df



def add_year(period):
    freq = period.freqstr
    year_later = period.to_timestamp() + pd.DateOffset(years=1)
    return pd.Period(year_later, freq=freq)

