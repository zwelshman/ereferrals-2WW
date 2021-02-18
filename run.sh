FILE=app_data/Referrals_csv_files/all.csv

if test -f "$FILE"
then
    streamlit run stream_app.py
else
    python ./data_processing/data_processing.py 
    streamlit run stream_app.py
fi
