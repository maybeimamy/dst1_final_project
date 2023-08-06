import os.path
import argparse
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

"""
HELPER FUNCTIONS
"""
## Merges columns based on range. Returns the updated dataframe.
def merge_columns(df, column_range):
    return df.loc[:, column_range].apply(
        lambda x: ', '.join(x.dropna().astype(str)),
        axis=1
    )

## Filters rows based on a condition. Returns the updated dataframe.
def filter_rows(df, condition):
    index = df[condition].index
    df.drop(index, inplace=True)

    return df

## Filters a dataframe by column value and data set. Returns the value counts.
def filtered_by(df, filter_value, column_value, data_set):
        return df[df['ALL_DIAGNOSES_SET'].isin(data_set) & (df[column_value] == filter_value)].value_counts()

## Generates a custom color palette. Returns a custom color palette.
def generate_custom_palette(sns, levels_per_column):
    num_colors = sum(levels_per_column)
    custom_palette = sns.color_palette('dark', n_colors=50)[:num_colors]
    return custom_palette

## Creates a stacked bar plot. Returns a stacked bar plot.
def plot_stacked_bar(df, title, column_prefix, levels_per_column, sns, plt):
    color_palette = generate_custom_palette(sns, levels_per_column)

    ax = df.plot(kind='bar', stacked=True, figsize=(12, 6), color=color_palette)
    ax.set_xlabel('Diagnosis')
    ax.set_ylabel('Count')
    ax.set_title(title)
    ax.legend(title=column_prefix, loc='lower center', bbox_to_anchor=(1, -0.25), ncol=len(df.columns))
    ax.set_xticklabels(df.index, rotation=45, ha='right')

    return plt.show()

"""
CONSTANTS
"""
input_file_path = '~/Downloads/mhcld-puf-2020-csv.csv'

output_file = 'clean_data.csv'

column_names = ['AGE', 'ETHNIC', 'RACE', 'GENDER', 'MH1', 'MH2', 'MH3', 'STATEFIP', 'DIVISION']

age_codes = {
    4: '18-20 years',
    5: '21-24 years',
    6: '25-29 years',
    7: '30-34 years',
    8: '35-39 years',
    9: '40-44 years',
    10: '45-49 years',
    11: '50-54 years',
    12: '55-59 years',
    13: '60-64 years',
    14: '65 years and older',
    -9: None
}

ethnic_codes = {
    1: 'Mexican',
    2: 'Puerto Rican',
    3: 'Other Hispanic or Latino Origin',
    4: 'Not of Hispanic or Latino Origin',
    -9: None
}

race_codes = {
    1: 'American Indian/Alaska Native',
    2: 'Asian',
    3: 'Black or African American',
    4: 'Native Hawaiian or Other Pacific Islander',
    5: 'White',
    6: 'Some other race alone/two or more races',
    -9: None
}

gender_codes = {
    1: 'Male',
    2: 'Female',
    -9: None
}

mh_codes = {
    1: 'Trauma and stressor-related disorders',
    2: 'Anxiety disorders',
    3: 'Attention deficit/hyperactivity disorder (ADHD)',
    4: 'Conduct disorders',
    5: 'Delirium/dementia',
    6: 'Bipolar disorders',
    7: 'Depressive disorders',
    8: 'Oppositional defiant disorders',
    9: 'Pervasive development disorders',
    10: 'Personality disorders',
    11: 'Schizophrenia or other psychotic disorders',
    12: 'Alcohol or substance use disorders',
    13: 'Other disorders/conditions',
    -9: None
}

state_codes = {
    1: 'Alabama',
    2: 'Alaska',
    4: 'Arizona',
    5: 'Arkansas',
    6: 'California',
    8: 'Colorado',
    9: 'Connecticut',
    10: 'Delaware',
    11: 'District of Columbia',
    12: 'Florida',
    13: 'Georgia',
    15: 'Hawaii',
    16: 'Idaho',
    17: 'Illinois',
    18: 'Indiana',
    19: 'Iowa',
    20: 'Kansas',
    21: 'Kentucky',
    22: 'Louisiana',
    25: 'Massachusetts',
    26: 'Michigan',
    27: 'Minnesota',
    28: 'Mississippi',
    29: 'Missouri',
    30: 'Montana',
    31: 'Nebraska',
    32: 'Nevada',
    34: 'New Jersey',
    35: 'New Mexico',
    36: 'New York',
    37: 'North Carolina',
    38: 'North Dakota',
    39: 'Ohio',
    40: 'Oklahoma',
    41: 'Oregon',
    42: 'Pennsylvania',
    44: 'Rhode Island',
    45: 'South Carolina',
    46: 'South Dakota',
    47: 'Tennessee',
    48: 'Texas',
    49: 'Utah',
    50: 'Vermont',
    51: 'Virginia',
    53: 'Washington',
    55: 'Wisconsin',
    56: 'Wyoming',
    72: 'Puerto Rico',
    99: 'Other jurisdictions'
}

division_codes = {
    0: 'Other jurisdictions',
    1: 'New England',
    2: 'Middle Atlantic',
    3: 'East North Central',
    4: 'West North Central',
    5: 'South Atlantic',
    6: 'East South Central',
    7: 'West South Central',
    8: 'Mountain',
    9: 'Pacific'
}

cols_codes_mapping = {
    'AGE': age_codes,
    'ETHNIC': ethnic_codes,
    'RACE': race_codes,
    'GENDER': gender_codes,
    'MH1': mh_codes,
    'MH2': mh_codes,
    'MH3': mh_codes,
    'STATEFIP': state_codes,
    'DIVISION': division_codes,
}

gender_levels = ['Male', 'Female']
re_levels = ['Not of Hispanic or Latino Origin, Black or African American', 'Not of Hispanic or Latino Origin, Native Hawaiian or Other Pacific Islander', 'Not of Hispanic or Latino Origin, Asian', 'Not of Hispanic or Latino Origin, Some other race alone/two or more races', 'Other Hispanic or Latino Origin, American Indian/Alaska Native', 'Other Hispanic or Latino Origin, White', 'Not of Hispanic or Latino Origin, American Indian/Alaska Native', 'Other Hispanic or Latino Origin, Black or African American', 'Not of Hispanic or Latino Origin, White', 'Puerto Rican, Some other race alone/two or more races', 'Other Hispanic or Latino Origin, Some other race alone/two or more races', 'Puerto Rican, Black or African American', 'Mexican, Some other race alone/two or more races', 'Mexican, White', 'Puerto Rican, White', 'Other Hispanic or Latino Origin, Native Hawaiian or Other Pacific Islander', 'Other Hispanic or Latino Origin', 'Mexican, Black or African American', 'Mexican, American Indian/Alaska Native', 'Other Hispanic or Latino Origin, Asian', 'Mexican, Asian', 'Puerto Rican, Asian', 'Native Hawaiian or Other Pacific Islander', 'Mexican', 'American Indian/Alaska Native', 'Some other race alone/two or more races', 'Asian', 'Not of Hispanic or Latino Origin', 'White', 'Black or African American', 'Puerto Rican', 'Puerto Rican, American Indian/Alaska Native', 'Puerto Rican, Native Hawaiian or Other Pacific Islander', 'Mexican, Native Hawaiian or Other Pacific Islander']
age_levels = ['65 years and older', '25-29 years', '60-64 years', '55-59 years', '40-44 years', '45-49 years', '35-39 years', '30-34 years', '50-54 years', '21-24 years', '18-20 years']

breakout_info = {
        'GENDER': gender_levels,
        'RACE/ETHNICITY': re_levels,
        'AGE': age_levels
}


"""
METHODS
"""
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