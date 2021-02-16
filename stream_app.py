import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.style.use('ggplot')
# plt.rcParams["figure.figsize"] = [16, 6]

st.title("Open Data Extracted From NHS e-referrals for Leeds CCG")


@st.cache
def load_data():
    data = pd.read_csv("./app_data/testing_group_2.csv")
    return data


data_load_state = st.text("Loading data")
df = load_data() 

st.subheader("Raw Weekly Referral 2WW data")
st.write(df)

st.subheader("Monthly Referral Aggregate 2WW data")
testing_group_month = df.groupby(["year", "month"]).sum()
st.write(testing_group_month)

st.subheader("Comparing two years for aggregate 2WW data Monthly")
fig, ax = plt.subplots()  # solved by add this line
ax = sns.lineplot(
    x="month",
    y="Referrals",
    hue="year",
    style="year",
    palette="colorblind",
    data=testing_group_month,
)

st.pyplot(fig)

st.subheader("Weekly Referral Aggregate 2WW data")
testing_group_week = df.groupby(["year", "week_of_year"]).sum()
st.write(testing_group_week)

st.subheader("Comparing two years for aggregate 2WW data weekly")
fig, ax = plt.subplots()  # solved by add this line
ax = sns.lineplot(
    x="week_of_year",
    y="Referrals",
    hue="year",
    style="year",
    palette="colorblind",
    data=testing_group_week,
)

st.pyplot(fig)

