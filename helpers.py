"""
This file contains helper methods
"""

"""
Merges columns based on range.
Returns the updated dataframe.
"""
def merge_columns(df, column_range):
    return df.loc[:, column_range].apply(
        lambda x: ', '.join(x.dropna().astype(str)),
        axis=1
    )

"""
Filters rows based on a condition.
Returns the updated dataframe.
"""
def filter_rows(df, condition):
    index = df[condition].index
    df.drop(index, inplace=True)

    return df

"""
Filters a dataframe by column value and data set
Returns the value counts
"""
def filtered_by(df, filter_value, column_value, data_set):
        return df[df['ALL_DIAGNOSES_SET'].isin(data_set) & (df[column_value] == filter_value)].value_counts()

"""
Generates a custom color palette.
Returns a custom color palette.
"""
def generate_custom_palette(sns, levels_per_column):
    num_colors = sum(levels_per_column)
    custom_palette = sns.color_palette('dark', n_colors=50)[:num_colors]
    return custom_palette

"""
Creates a stacked bar plot.
Returns a stacked bar plot.
"""
def plot_stacked_bar(df, title, column_prefix, levels_per_column, sns, plt):
    color_palette = generate_custom_palette(sns, levels_per_column)

    ax = df.plot(kind='bar', stacked=True, figsize=(12, 6), color=color_palette)
    ax.set_xlabel('Diagnosis')
    ax.set_ylabel('Count')
    ax.set_title(title)
    ax.legend(title=column_prefix, loc='lower center', bbox_to_anchor=(1, -0.25), ncol=len(df.columns))
    ax.set_xticklabels(df.index, rotation=45, ha='right')

    return plt.show()

