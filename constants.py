"""
This file contains all constants
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

