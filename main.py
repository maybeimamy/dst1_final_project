import os.path
import argparse
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from constants import *
from helpers import *

## Cleans the raw data with the option to write clean data to a CSV.
## Returns the dataframe to be used to Summarize the Stats and/or Generate Visualizations.
def clean_raw_data(write_to_csv):
    ## Create Dataframe with only applicable columns
    df = pd.read_csv(input_file_path, usecols=column_names)

    ## Filtering unusable or unnecessary data
    filter_rows(df, ((df['AGE'] == -9) | (df['AGE'] <= 3)))
    filter_rows(df, ((df['ETHNIC'] == -9) & (df['RACE'] == -9)))
    filter_rows(df, (df['GENDER'] == -9))
    filter_rows(df, (df['MH1'] == -9))

    ## Replace all codes to the mapped values
    for column, code in cols_codes_mapping.items():
        df[column] = df[column].replace(code)

    ## Rename columns
    df = df.rename(columns={'STATEFIP': 'STATE', 'DIVISION': 'CENSUS_DIVISION'})

    ## Merging all MH columns and merging 'ETHNIC' and 'RACE'
    df['ALL_DIAGNOSES'] = merge_columns(df, ['MH1', 'MH2', 'MH3'])
    df['RACE/ETHNICITY'] = merge_columns(df, ['ETHNIC', 'RACE'])

    ## Drop single instance rows after merge
    df.drop(columns=['ETHNIC', 'RACE', 'MH1', 'MH2', 'MH3'], inplace=True)

    ## Write to csv
    if write_to_csv:
        df.to_csv(output_file, index=False, chunksize=10000)

    return df


## Summarizes the stats from the cleaned data.
## Returns a dictionary with pertinent data to run the visualizations
def summarize_stats(df):
    ## If no dataframe is provided, create one from the clean data output file
    df = pd.read_csv(output_file) if df is None else df

    ## Split the 'ALL_DIAGNOSES' column into individual diagnoses
    df['NUM_DIAGNOSES'] = df['ALL_DIAGNOSES'].str.split(', ').apply(lambda x: len(x))

    ## Find the top ten most common diagnoses with two or three diagnoses
    df['ALL_DIAGNOSES'] = df['ALL_DIAGNOSES'].str.split(', ').apply(
        lambda x: ', '.join(sorted(x)))

    top_ten_diagnoses = df[df['NUM_DIAGNOSES'].isin([2, 3])]['ALL_DIAGNOSES'].value_counts().head(10)

    ## Create summary dataframe
    summary_df = pd.DataFrame({'Diagnosis': top_ten_diagnoses.index, 'Count': top_ten_diagnoses.values}).reset_index(
        drop=True)

    print(summary_df)

    return {
        'df': df,
        'summary_df': summary_df,
        'top_ten_diagnoses': top_ten_diagnoses,
    }


## Generates 5 visualizations based on the summary stats.
def generate_visualizations(df, summary_stats):
    ## Summarize stats from clean data if summarize_stats has not run
    if df is None:
        df = pd.read_csv(output_file)

    if summary_stats is None:
        summary_stats = summarize_stats(df)

    top_ten_diagnoses = summary_stats['top_ten_diagnoses']
    num_diagnoses_counts = df['NUM_DIAGNOSES'].value_counts()
    summary_df = summary_stats['summary_df']

    ## Plot the doughnut chart of the diagnosis number frequency
    plt.figure(figsize=(8, 8))
    explode = [0, 0.1, 0.1]  # Explosion effect on the segments representing 2 and 3 diagnoses
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    plt.pie(num_diagnoses_counts, labels=num_diagnoses_counts.index, autopct='%1.1f%%', startangle=90, colors=colors,
            wedgeprops=dict(width=0.4), explode=explode)
    plt.gca().add_artist(
        plt.Circle((0, 0), 0.3, color='white'))  # Draw a white circle in the middle to create the doughnut effect
    plt.title('Instance Of Comorbidity')
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.
    plt.show()

    ## Plot the top ten most common diagnoses as a bar plot with a trend line and custom colors
    plt.figure(figsize=(10, 10))
    ax = sns.barplot(x=top_ten_diagnoses.index, y=top_ten_diagnoses.values, palette='magma')
    ax.set_ylabel('Count')
    ax.set_xlabel('Diagnosis Combination')
    ax.set_title('Top Ten Most Common Comorbidity Sets')

    ## Add count above each bar
    for index, value in enumerate(top_ten_diagnoses.values):
        ax.text(index, value, f'{value}', ha='center', va='bottom', fontsize=10)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    ## Initialize new columns with 0 for each combination of breakout column and level
    for column_name, levels in breakout_info.items():
        for level in levels:
            summary_df[f'{column_name}_{level}'] = 0

    ## Iterate through each diagnosis and update counts for each combination of breakout column and level
    for i, diag in enumerate(summary_df['Diagnosis']):
        filtered_df = df[df['ALL_DIAGNOSES'] == diag]
        for column_name, levels in breakout_info.items():
            for level in levels:
                count = len(filtered_df[(filtered_df[column_name] == level)])
                summary_df.at[i, f'{column_name}_{level}'] = count

    # Set diagnosis as index for plotting
    summary_df.set_index('Diagnosis', inplace=True)

    ## Create the levels_per_column list with the number of levels for each breakout column
    levels_per_column = [len(gender_levels), len(re_levels), len(age_levels)]

    ## Loop through each breakout column and create stacked bar plots with the custom color palette
    for column_name, levels in breakout_info.items():
        columns_to_plot = [col for col in summary_df.columns if col.startswith(f'{column_name}_')]
        plot_stacked_bar(summary_df[columns_to_plot], f'Common Comorbidity by {column_name}', column_name,
                         levels_per_column, sns, plt)


## Handles the arguments passed in when running the script.
## Options include:
    ## Writing the clean output data to a CSV (-csv or --csv)
    ## Cleaning the data only (-clean or --clean)
    ## Summarizing the data only (-summary or --summary)
    ## Generating the visualizations only (-visualize or --visualize)
def handle_args(args):
    write_to_csv = True if args.csv else False
    clean_data_only = True if args.clean else False
    summarize_only = True if args.summary else False
    visualize_only = True if args.visualize else False

    if clean_data_only:
        if os.path.isfile(output_file) and write_to_csv:
            print(f"This action will overwrite the previous output file {output_file}")
        clean_raw_data(write_to_csv)
        return True

    if not os.path.isfile(output_file):
        clean_raw_data(write_to_csv)

    if summarize_only:
        summarize_stats(df=None)
        return True

    if visualize_only:
        generate_visualizations(df=None, summary_stats=None)
        return True

    return False


## Conditionally runs the correct function(s) based on arguments.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", "--csv", help="write output to csv", action="store_true")
    parser.add_argument("-clean", "--clean", help="clean the raw data only", action="store_true")
    parser.add_argument("-summary", "--summary", help="summarize the data only", action="store_true")
    parser.add_argument("-visualize", "--visualize", help="visualize the data only", action="store_true")
    args = parser.parse_args()

    if handle_args(args):
        return

    df = None

    ## Only run clean_raw_data if a clean_data.csv doesn't exist
    if not os.path.isfile(output_file):
        write_to_csv = True if args.csv else False
        df = clean_raw_data(write_to_csv)

    summary_stats = summarize_stats(df)
    generate_visualizations(summary_stats['df'], summary_stats)

if __name__ == "__main__":
    main()