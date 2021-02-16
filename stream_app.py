import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.style.use('ggplot')
# plt.rcParams["figure.figsize"] = [16, 6]

st.title("Data Extracted From NHS e-referrals")


@st.cache
def load_data():
    data = pd.read_csv("./app_data/testing_group_2.csv")
    return data


data_load_state = st.text("Loading data")
df = load_data() 

st.subheader("Weekly Referral Raw 2WW data")
st.write(df)

st.subheader("Weekly Referral Aggregate 2WW data")
testing_group = df.groupby(["year", "week_of_year"]).sum()
st.write(testing_group)

st.subheader("Comparing two years for Aggregate 2WW data")
fig, ax = plt.subplots()  # solved by add this line
ax = sns.lineplot(
    x="week_of_year",
    y="Referrals",
    hue="year",
    style="year",
    palette="colorblind",
    data=testing_group,
)

st.pyplot(fig)

