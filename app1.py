import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# LOAD DATA
# -------------------------------
data = pd.read_excel("FINAL_DATASET.xlsx")

data.columns = data.columns.str.strip().str.lower()

# -------------------------------
# TITLE
# -------------------------------
st.title("Real Estate Buyer Segmentation Dashboard")

# -------------------------------
# FILTERS
# -------------------------------
st.sidebar.header("Filters")

country = st.sidebar.selectbox("Country", ["All"] + list(data['country'].dropna().unique()))
region = st.sidebar.selectbox("Region", ["All"] + list(data['region'].dropna().unique()))
purpose = st.sidebar.selectbox("Purpose", ["All"] + list(data['acquisition_purpose'].dropna().unique()))
client = st.sidebar.selectbox("Client Type", ["All"] + list(data['client_type'].dropna().unique()))

filtered_data = data.copy()

if country != "All":
    filtered_data = filtered_data[filtered_data['country'] == country]

if region != "All":
    filtered_data = filtered_data[filtered_data['region'] == region]

if purpose != "All":
    filtered_data = filtered_data[filtered_data['acquisition_purpose'] == purpose]

if client != "All":
    filtered_data = filtered_data[filtered_data['client_type'] == client]
st.subheader("Filtered Data Size")
st.write(filtered_data.shape)

# -------------------------------
# GRAPHS
# -------------------------------
st.header("Cluster Distribution")

fig, ax = plt.subplots()
filtered_data['cluster'].value_counts().plot(kind='bar', ax=ax)
st.pyplot(fig)

st.header("Satisfaction by Cluster")

fig2, ax2 = plt.subplots()
filtered_data.groupby('cluster')['satisfaction_score'].mean().plot(kind='bar', ax=ax2)
st.pyplot(fig2)

st.header("Geographic Analysis")

geo = filtered_data.groupby(['region', 'cluster']).size().unstack()

fig3, ax3 = plt.subplots()
geo.plot(kind='bar', stacked=True, ax=ax3)
st.pyplot(fig3)

st.header("Insights")

st.write(filtered_data.groupby('cluster').mean(numeric_only=True))
