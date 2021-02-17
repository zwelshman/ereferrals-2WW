import pandas as pd
import streamlit as st

def filtered_dataframe(df: pd.DataFrame, column: str, default: list):
    Specialty = list(df[column].unique())
    Specialty_SELECTED = st.multiselect(f"Select {column}", Specialty, default=default)
    # Mask to filter dataframe
    mask = df[column].isin(Specialty_SELECTED)
    df_out = df[mask]
    return df_out

    # # Create a list of possible values and multiselect menu with them in it.
    # CCG = list(df["CCG_Name"].unique())
    # CCG_SELECTED = st.multiselect("Select CCG", CCG, default=["NHS LEEDS CCG", "NHS ROTHERHAM CCG"])
    # # Mask to filter dataframe
    # mask_CCG = df["CCG_Name"].isin(CCG_SELECTED)
    # df = df[mask_CCG]
    # # st.write('You selected:', CCG_SELECTED)