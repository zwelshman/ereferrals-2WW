# Fetch data from NHSD (CSV_File)
# Place in a data folder
# Merge data into one file (may cause issues although CAV has no limit)
# Point stream_app to the right place.

import pandas as pd
import subprocess
import os
import time
import sys
import zipfile
import shutil

import requests
from contextlib import closing
import csv

import os.path

if os.path.isfile("../app_data/all.csv"):
    print("Deleting old file and pipeline fresh")
    os.remove("../app_data/all.csv")
else:
    print("File does not exist, starting pipeline")
    time.sleep(3)


def get_referral_zip(url, target_path):
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()


def extract_zip(zip_file, destination):
    zipe = zipfile.ZipFile(zip_file)
    zipe.extractall(destination)


import subprocess


def create_merge():
    create_merge = ["cat *.csv>merged_file.csv"]
    subprocess.run(create_merge, cwd="./extracted_files", shell=True, check=True)


def remove_headers(data_folder, file_name):
    df = pd.read_csv(data_folder + file_name)
    df["week_start"], df["week_end"] = df["Week"].str.split("-", 1).str
    word = "Week"
    df = df[~df["Week"].str.contains(word, na=False)]
    return df


def format_dataframe(df):
    df["formatted_date_start"] = pd.to_datetime(
        df["week_start"], dayfirst=True, errors="coerce"
    )
    df["day_of_year"] = df.formatted_date_start.apply(lambda x: x.dayofyear)
    df["week_of_year"] = df.formatted_date_start.apply(lambda x: x.weekofyear)
    df["year"] = df.formatted_date_start.apply(lambda x: x.year)
    df["month"] = df.formatted_date_start.apply(lambda x: x.month)
    return df


def move_merged(source, destination, file_name):
    try:
        shutil.move(source + file_name, destination + file_name)
    except:
        raise FileNotFoundError("File has already been moved to the correct folder")


print("Getting Zip")
get_referral_zip(
    url="https://files.digital.nhs.uk/83/10B742/Referrals_csv_files.zip",
    target_path="Referrals_csv_files.zip",
)

print("Extracting Zip")
extract_zip("Referrals_csv_files.zip", "./extracted_files")

print("Merging files")
create_merge()

print("Removing headers")
df_headers_removed = remove_headers("./extracted_files", "/merged_file.csv")

print("Data analysis data")
data_to_analyse = format_dataframe(df_headers_removed)

print("Placing in folder")
data_to_analyse.to_csv("../app_data/all.csv")


print("cleaning up")
os.remove("Referrals_csv_files.zip")
shutil.rmtree("extracted_files")
