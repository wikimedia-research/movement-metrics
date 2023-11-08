import pandas as pd
import numpy as np
from pathlib import Path
from src.utils import load_metric_file
from src.utils import subtract_year

# Define a function to group gender categories
def map_gender_category(category):
    if category in ['male', 'cisgender male']:
        return 'males'
    elif category in ['female', 'cisgender female']:
        return 'females'
    else:
        return 'gender_diverse'
    

# Group by 'month' and 'category', then pivot the table
def group_and_separate_categories(df):
    grouped = df.groupby(['month', 'category'])['standard_quality_count_value'].sum().reset_index()
    pivoted = grouped.pivot(index='month', columns='category', values='standard_quality_count_value')
    pivoted.columns.name = None  # Remove the column name
    return pivoted

# Clean up function to facilitate combine_first() with csv.
def process_quality_data(df):
    # Separate data based on 'content_gap'
    df_gender = df[df['content_gap'] == 'gender'].copy()
    df_geo = df[df['content_gap'] == 'geography_wmf_region'].copy()
   
    # Apply the gender mapping function to the 'category' column
    df_gender['category'] = df_gender['category'].apply(map_gender_category)
    
    # Group and separate data for gender and geography
    df_gender_grouped = group_and_separate_categories(df_gender)
    df_geo_grouped = group_and_separate_categories(df_geo)
    
    # Concatenate the two dataframes along columns
    combined_df = pd.concat([df_gender_grouped, df_geo_grouped], axis=1)

    # Rename the columns with a prefix
    rename_dict = {col: f"total_quality_articles_about_{col}" for col in combined_df.columns}
    combined_df = combined_df.rename(columns=rename_dict)
 
    return combined_df


# Calculate MoM and totals as well proportions
def calculate_mom(df):
    # Define column names using the categories
    gender_categories = ['gender_diverse', 'males', 'females']
    region_categories = [
        'Central & Eastern Europe & Central Asia', 'East, Southeast Asia, & Pacific',
        'Latin America & Caribbean', 'Middle East & North Africa',
        'North America', 'Northern & Western Europe', 'South Asia',
        'Sub-Saharan Africa', 'UNCLASSED'
    ]
    
    # Create list of genders and regions using prefixes
    all_genders = ['MoM_net_new_quality_articles_about_' + gender for gender in gender_categories]
    all_regions = ['MoM_net_new_quality_articles_about_' + region for region in region_categories]
    
    underrepresented_gender = [name for name in all_genders if 'females' in name or 'gender_diverse' in name]
    underrepresented_region = [name for name in all_regions if name.rsplit('_', 1)[-1] not in ['Central & Eastern Europe & Central Asia', 'North America', 'Northern & Western Europe', 'UNCLASSED']]

    # Compute the MoM difference only for the last value
    for column in df.columns:
        if 'total' in column:
            mom_column_name = column.replace('total_', 'MoM_net_new_')
            df.at[df.index[-1], mom_column_name] = df[column].iloc[-1] - df[column].iloc[-2]
    
    # Calculate and update the last row for the sum columns
    df.at[df.index[-1], 'gender_minorities_net_new_articles_sum'] = df.loc[df.index[-1], underrepresented_gender].sum()
    df.at[df.index[-1], 'underrepresented_regions_net_new_articles_sum'] = df.loc[df.index[-1], underrepresented_region].sum()
    df.at[df.index[-1], 'all_genders_net_new_articles_sum'] = df.loc[df.index[-1], all_genders].sum()
    df.at[df.index[-1], 'all_regions_net_new_articles_sum'] = df.loc[df.index[-1], all_regions].sum()

    # Calculate and update the last row for the percentage columns
    df.at[df.index[-1], '% of new articles about gender minorities'] = df.at[df.index[-1], 'gender_minorities_net_new_articles_sum'] / df.at[df.index[-1], 'all_genders_net_new_articles_sum']
    df.at[df.index[-1], '% of new articles about underrepresented regions'] = df.at[df.index[-1], 'underrepresented_regions_net_new_articles_sum'] / df.at[df.index[-1], 'all_regions_net_new_articles_sum']

    return df


# Calculate monthly and quarterly reporting for content gap metrics
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


def check_for_incomplete_quarterly_data(df):
    """
    Checks if the last row of the '% new quality articles about regions that are underrepresented' 
    column in the DataFrame is NaN and prints an error message if true.
    """
    column_name = "% new quality articles about regions that are underrepresented"
    if pd.isna(df[column_name].iloc[-1]):
        wmfdata.utils.print_err("The quarterly report is based on incomplete data as the final month's data is not available.")
