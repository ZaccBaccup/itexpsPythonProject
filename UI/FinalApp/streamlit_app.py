# Required: run both Flask and Streamlit from command prompt
# Flask command (runs on port 8085)     = python app.py
# Streamlit command (runs on port 8501) = streamlit run streamlit_app.py

# pip install streamlit pandas
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from config import OUTPUT_DIR # config.py has the directory where csv files are stored

st.set_page_config(layout="wide", page_title="Dashboard")

# CSS
st.markdown("""
<style>
/* Main container padding */
.block-container {
    padding-top: 24px !important;
    padding-bottom: 16px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
/* Divider spacing */
hr {
    margin-top: 6px !important;
    margin-bottom: 6px !important;
    border: none;
    border-top: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

st.subheader("Interactive Dashboard")

# Combine the directory from OUTPUT_DIR with the filename
csv_file_path = os.path.join(OUTPUT_DIR, "jobapps.csv")

df = pd.read_csv(csv_file_path)
df['date'] = pd.to_datetime(df['date'])

# Display the filter dropdowns
with st.container():
    col1, col2, col3 = st.columns(3)

    companies = col1.multiselect("Company", df['company'].unique(), placeholder="Filter by company", label_visibility="collapsed")
    roles = col2.multiselect("Role", df['role'].unique(), placeholder="Filter by role", label_visibility="collapsed")
    status = col3.multiselect("Status", df['status'].unique(), placeholder="Filter by status", label_visibility="collapsed")

# Apply filters
filtered_df = df.copy()

if companies:
    filtered_df = filtered_df[filtered_df['company'].isin(companies)]

if roles:
    filtered_df = filtered_df[filtered_df['role'].isin(roles)]

if status:
    filtered_df = filtered_df[filtered_df['status'].isin(status)]

total_apps = len(filtered_df)

# Define active applications
active_statuses = [
    'Applied',
    'Interview Scheduled',
    'Interviewed',
    'Offer Received'
]

active_df = filtered_df[
    filtered_df['status'].isin(active_statuses)
]

active_apps = len(active_df)

followup_rate = (
    active_df['followedup'].fillna(0).astype(int).sum() / active_apps * 100
    if active_apps else 0
)

interviewed_apps = filtered_df[
    filtered_df['status'].isin(['Interviewed', 'Interview Scheduled', 'Offer Received'])
].shape[0]

interview_rate = (
    interviewed_apps / total_apps * 100
    if total_apps else 0
)

ghost_apps = filtered_df[
    (filtered_df['status'].isin(['Applied', 'Interviewed', 'Interview Scheduled', 'Offer Received'])) &
    (filtered_df['followedup'] == 1) &
    ((pd.Timestamp.today() - filtered_df['date']).dt.days > 30)
].shape[0]

ghost_rate = (ghost_apps / total_apps * 100) if total_apps else 0

st.markdown("---")

# Display the key metrics
# st.subheader("Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Applications", total_apps)
col2.metric("Active Applications", active_apps)
col3.metric("Follow-up Rate", f"{followup_rate:.1f}%")
col4.metric("Interview Rate", f"{interview_rate:.1f}%")
col5.metric("Ghost Rate", f"{ghost_rate:.1f}%")

st.markdown("---")

# Display the charts
col1, spacer, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown(
        "<h3 style='text-align: center;'>Applications by Month</h3>",
        unsafe_allow_html=True
    )

    monthly = filtered_df.groupby(
        filtered_df['date'].dt.to_period("M")
    ).size().reset_index(name="count")

    monthly['date'] = monthly['date'].dt.to_timestamp()

    fig = px.line(
        monthly,
        x='date',
        y='count',
        markers=True,
        text='count'
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Applications",
        margin=dict(t=30)
    )

    fig.update_xaxes(tickformat="%b %Y", tickangle=-45) # diagonal label

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(
        "<h3 style='text-align: center;'>Applications by Status</h3>",
        unsafe_allow_html=True
    )

    status_counts = filtered_df['status'].value_counts()

    status_order = [
        "Applied",
        "Interview Scheduled",
        "Interviewed",
        "Offer Received",
        "Rejected",
        "Withdrawn"
    ]

    status_counts = status_counts.reindex(status_order).fillna(0)

    status_df = status_counts.reset_index()
    status_df.columns = ["Status", "Count"]

    color_map = {
        "Applied": "#3B82F6",
        "Interview Scheduled": "#F59E0B",
        "Interviewed": "#8B5CF6",
        "Offer Received": "#10B981",
        "Rejected": "#EF4444",
        "Withdrawn": "#6B7280"
    }

    fig = px.bar(
        status_df,
        x="Status",          # swap axes
        y="Count",
        color="Status",
        color_discrete_map=color_map,
        text="Count"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, l=20, r=20, b=20),
        xaxis_title="Status",
        yaxis_title="Applications",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

st.write("")  # lightweight spacer

col3, spacer, col4 = st.columns([1, 0.1, 1])

with col3:
    st.markdown(
        "<h3 style='text-align: center;'>Applications by Role</h3>",
        unsafe_allow_html=True
    )

    # Count + sort
    role_counts = filtered_df['role'].value_counts().reset_index()
    role_counts.columns = ['role', 'count']
    role_counts = role_counts.sort_values(by='count', ascending=True)

    # Optional: custom color palette
    color_map = px.colors.qualitative.Set3  # nice soft variety

    # Horizontal bar chart
    fig = px.bar(
        role_counts,
        x='count',
        y='role',
        text='count',
        orientation='h',
        color='role',
        color_discrete_sequence=color_map
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        xaxis_title="Applications",
        yaxis_title="Role",
        height=400,
        margin=dict(t=20),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
with col4:
    st.markdown(
        "<h3 style='text-align: center;'>Follow-up Status (Active Apps)</h3>",
        unsafe_allow_html=True
    )

    active_df = filtered_df[filtered_df['status'].isin(active_statuses)]

    active_apps = len(active_df)

    followed_up_count = active_df['followedup'].fillna(0).astype(int).sum()
    not_followed_up_count = active_apps - followed_up_count

    follow_counts = pd.DataFrame({
        "followedup": ["Followed Up", "Not Followed Up"],
        "count": [followed_up_count, not_followed_up_count]
    })

    color_map = {
        "Followed Up": "#4CAF50",
        "Not Followed Up": "#F44336"
    }

    fig = px.pie(
        follow_counts,
        names='followedup',
        values='count',
        color='followedup',
        color_discrete_map=color_map
    )

    fig.update_traces(textinfo='percent+label')

    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20)
    )

    st.plotly_chart(fig, use_container_width=True)
