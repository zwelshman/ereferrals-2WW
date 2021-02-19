import pandas as pd
import streamlit as st

def filtered_dataframe(df: pd.DataFrame, column: str, default: list):
    options = list(df[column].unique())
    options.append("All")
    value = st.multiselect(f"Select {column}", options, default=default)
    
    if "All" in value:
        value = options

    # Mask to filter dataframe
    mask = df[column].isin(value)
    df_out = df[mask]
    return df_out