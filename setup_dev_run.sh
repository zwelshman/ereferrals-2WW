#!/bin/bash
cd ./data_processing && python data_processing.py && cd ..
streamlit run stream_app.py