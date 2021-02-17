import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import time

matplotlib.style.use("ggplot")
# plt.rcParams["figure.figsize"] = [16, 6]

st.title("Open Data Extracted From NHS e-referrals")

rad = st.sidebar.radio("Navigation", ["Two Week Wait Analysis", "About me"])

if rad == "About me":
    "Markdown: #Work in progress"

if rad == "Two Week Wait Analysis":

    @st.cache(allow_output_mutation=True)
    def load_data():
        data = pd.read_csv("./app_data/all.csv")
        return data

    with st.spinner(
        "Wait for it... Just loading the data "
    ):

        my_bar = st.progress(0)
        for percent_complete in range(100):
            df = load_data()
            df.loc[(df.day_of_year > 358) & (df.week_of_year == 1), "week_of_year"] = 52
            my_bar.progress(percent_complete + 1)

        st.success("Done, your data has loaded! Don't forget to check the correct filters are selected.")

    # option = st.sidebar.selectbox(
    #     'Which number do you like best?',
    #      df['month'])

    # 'You selected:', option

    # Create a list of possible values and multiselect menu with them in it.
    CCG = list(df["CCG_Name"].unique())
    CCG_SELECTED = st.multiselect("Select CCG", CCG, default=['NHS LEEDS CCG'])
    # Mask to filter dataframe
    mask_CCG = df["CCG_Name"].isin(CCG_SELECTED)
    df = df[mask_CCG]
    # st.write('You selected:', CCG_SELECTED)

    # Create a list of possible values and multiselect menu with them in it.
    Specialty = list(df["Specialty"].unique())
    Specialty_SELECTED = st.multiselect("Select Specialty", Specialty, default=['2WW'])
    # Mask to filter dataframe
    mask_Specialty = df["Specialty"].isin(Specialty_SELECTED)
    df = df[mask_Specialty]

    # Create a list of possible values and multiselect menu with them in it.
    Priority = list(df["Priority"].unique())
    Priority = st.multiselect("Select Priority", Priority, default=['2WW'])
    # Mask to filter dataframe
    mask_Priority = df["Priority"].isin(Priority_SELECTED)
    df = df[mask_Priority]
    # st.write('You selected:', Specialty_SELECTED)

    # months_values = list(df['month'].unique())
    # Months_SELECTED = st.slider('Select a range of values for months', 0, 12, (0, 12))
    # mask_Months = df['month'].isin(Months_SELECTED)
    # df = df[mask_Months]
    # st.write('Values:', Months_SELECTED)

    st.subheader("Raw Weekly Referral 2WW data")
    st.write(df)

    testing_group_month = df.drop(columns=["day_of_year", "week_of_year"])
    testing_group_month = testing_group_month.groupby(
        ["CCG_Name", "year", "month"]
    ).sum()

    st.subheader("Comparing two years for aggregate 2WW data Monthly")
    fig, ax = plt.subplots()  # solved by add this line
    ax = sns.lineplot(
        x="month",
        y="Referrals",
        hue="year",
        style="CCG_Name",
        palette="colorblind",
        data=testing_group_month,
    )
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    st.pyplot(fig)

    st.subheader("Monthly Referral Aggregate 2WW data")
    st.write(testing_group_month)

    testing_group_week = df.drop(columns=["day_of_year", "month"])
    testing_group_week = testing_group_week.groupby(
        ["CCG_Name", "year", "week_of_year"]
    ).sum()

    st.subheader("Comparing two years for aggregate 2WW data weekly")
    fig, ax = plt.subplots()  # solved by add this line
    ax = sns.lineplot(
        x="week_of_year",
        y="Referrals",
        hue="year",
        style="CCG_Name",
        palette="colorblind",
        data=testing_group_week,
    )
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    st.pyplot(fig)

    st.subheader("Weekly Referral Aggregate 2WW data")
    st.write(testing_group_week)

