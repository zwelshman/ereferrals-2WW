import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import time

from src.dataframe_manipulation import filtered_dataframe

matplotlib.style.use("ggplot")
# plt.rcParams["figure.figsize"] = [16, 6]

st.title("Open Data Extracted From NHS e-referrals.")

rad = st.sidebar.radio(
    "Navigation",
    ["Analysis for Two Week Wait", "Advanced Analytics", "About me"],
)

if rad == "About me":
    "Markdown: #Work in progress"

if rad == "Analysis for Two Week Wait":

    @st.cache(allow_output_mutation=True)
    def load_data():
        data = pd.read_csv("./app_data/all.csv")
        return data

    with st.spinner("Wait for it... Just loading the data"):

        my_bar = st.progress(0)
        for percent_complete in range(100):
            df = load_data()
            df.loc[(df.day_of_year > 358) & (df.week_of_year == 1), "week_of_year"] = 52
            my_bar.progress(percent_complete + 1)

        st.success(
            "Done, your data has loaded! Don't forget to check the correct filters are selected."
        )

    # option = st.sidebar.selectbox(
    #     'Which number do you like best?',
    #      df['month'])

    # 'You selected:', option

    df = filtered_dataframe(df, 'CCG_Name', default=["NHS LEEDS CCG", "NHS ROTHERHAM CCG"])
    df = filtered_dataframe(df, 'Specialty', default=["2WW"])
    df = filtered_dataframe(df, 'Priority', default=["2 Week Wait", "Urgent", "Routine"])

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


if rad == "Advanced Analytics":
    "Markdown: #Work in progress"
