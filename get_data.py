from data_processing.download_data import (
    merge_cvs,
    remove_headers,
    format_dataframe,
    to_folder_csv,
)

print("Merging files")
merge_cvs()
print("Removing headers")
df_headers_removed = remove_headers("app_data/Referrals_csv_files/", "merge.csv")
print("Data analysis data")
data_to_analyse = format_dataframe(df_headers_removed)
print("Placing in folder")
to_folder_csv(data_to_analyse, "app_data/all.csv")