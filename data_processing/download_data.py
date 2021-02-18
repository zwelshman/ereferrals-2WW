# Fetch data from NHSD (CSV_File)
# place in a data folder

# Merge data into one file (may cause issues although CAV has no limit)
import pandas as pd
import subprocess

def merge_cvs():
    delete_merge = ["if [ $( ls merge.csv ) ]; then rm merge.csv; fi"]
    subprocess.run(delete_merge, cwd="./app_data/Referrals_csv_files/", shell=True, check=True)
    create_merge = ["cat *.csv>merge.csv"]
    subprocess.run(create_merge, cwd="./app_data/Referrals_csv_files/", shell=True, check=True)

def remove_headers( data_folder, file_name ):
    df = pd.read_csv(data_folder + file_name)
    df['week_start'], df['week_end'] = df['Week'].str.split('-', 1).str
    word = 'Week'
    df = df[~df["Week"].str.contains(word, na=False)]
    return df

def format_dataframe(df):
    df['formatted_date_start'] = pd.to_datetime(df['week_start'], dayfirst=True, errors ='coerce')
    df['day_of_year'] = df.formatted_date_start.apply(lambda x: x.dayofyear)
    df['week_of_year'] = df.formatted_date_start.apply(lambda x: x.weekofyear)
    df['year'] = df.formatted_date_start.apply(lambda x: x.year)
    df['month'] = df.formatted_date_start.apply(lambda x: x.month)
    return df

# Place in new folder
def to_folder_csv(df, location):
    df.to_csv(location, index=False)
