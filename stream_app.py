import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import time

from src.dataframe_manipulation import filtered_dataframe

matplotlib.style.use("ggplot")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Helvetica"
plt.rcParams["axes.edgecolor"] = "#333F4B"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["xtick.color"] = "#333F4B"
plt.rcParams["ytick.color"] = "#333F4B"
# plt.rcParams["figure.figsize"] = [16, 6]


def main():

    st.title("Open Data Extracted From NHS e-referrals.")

    rad = st.sidebar.radio(
        "Navigation", ["Analysis for Two Week Wait", "Advanced Analytics", "About me"],
    )

    if rad == "About me":
        "Placeholder"

    if rad == "Analysis for Two Week Wait":

        @st.cache(allow_output_mutation=True)
        def load_data():
            data = pd.read_csv("./app_data/all.csv")
            return data

        with st.spinner("Wait for it... Just loading the data..."):

            my_bar = st.progress(0)
            for percent_complete in range(100):
                df = load_data()
                df.loc[
                    (df.day_of_year > 358) & (df.week_of_year == 1), "week_of_year"
                ] = 52
                my_bar.progress(percent_complete + 1)

            st.success(
                "Done, your data has loaded! Don't forget to check the correct filters are selected."
            )

        df = filtered_dataframe(
            df, "CCG_Name", default=["NHS LEEDS CCG", "NHS ROTHERHAM CCG"]
        )

        df = filtered_dataframe(df, "Specialty", default=["2WW"])

        df = filtered_dataframe(
            df,
            "Clinic_Type",
            default=[
                "2WW Breast",
                "2WW Gynaecology",
                "2WW Haematology",
                "2WW Head and Neck",
                "2WW Lower GI",
                "2WW Lung",
                "2WW Skin",
                "2WW Upper GI",
                "2WW Urology",
                "2WW Brain",
            ],
        )

        df = filtered_dataframe(
            df, "Priority", default=["2 Week Wait", "Urgent", "Routine"]
        )

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

        testing_group_clinic = df.drop(columns=["day_of_year", "week_of_year"])
        testing_group_clinic = testing_group_clinic.groupby(
            ["CCG_Name", "year", "month", "Clinic_Type"]
        ).sum()
        testing_group_clinic.reset_index(inplace=True)

        fig, ax = plt.subplots()
        ax = sns.lineplot(
            x="Clinic_Type",
            y="Referrals",
            hue="year",
            style="CCG_Name",
            palette="colorblind",
            data=testing_group_clinic,
        )

        plt.xticks(rotation=90)
        ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        st.pyplot(fig)

        st.write(testing_group_clinic)

    if rad == "Advanced Analytics":
        "Place holder"


if __name__ == "__main__":
    main()
