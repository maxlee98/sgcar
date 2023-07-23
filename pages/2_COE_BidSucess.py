
import streamlit as st
import os
import altair as alt
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas as pd
import numpy as np
st.set_page_config(page_title="Team Demo", page_icon="📈")
fl_name = __file__.split("\\")[-1].split(".")[0]

st.title('Trend Analysis')
st.write(
    """
    This demo shows a COE relationship along with bid success to find if there are any correlation.
    Here it also shows the price trends for a specific category of COE. \\
    An Example: "Finding out whether to purchase a COE at a point in time."

    """
)


current_path = os.getcwd()
coe_path = os.path.join(current_path, "data", 'M11-coe_results.csv')
coePQP_path = os.path.join(current_path, "data", 'M11-coe_results_pqp.csv')

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def plotBidPremium(df):
    nearest = alt.selection_point(nearest=True, on='mouseover',
                                fields=['date'], empty=False)

    base = alt.Chart(df).encode(x='date:O')

    bar = base.mark_bar().encode(y='bids_success:Q')

    line =  base.mark_line(color='red').encode(
        y='premium:Q'
    )
    scaled_bar_chart = bar.encode(
        y=alt.Y('bids_success:Q', scale=alt.Scale(domain=(0, 1/3)))
    )

    # selectors = alt.Chart(filtered_coe).mark_point().encode(
    #     x='date:T',
    #     opacity=alt.value(0),
    # ).add_params(
    #     nearest
    # )

    # points = base.mark_point().encode(
    #     opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    # )

    # text = base.mark_text(align='left', dx=5, dy=-5).encode(
    #     text=alt.condition(nearest, 'premium:Q', alt.value(' '))
    # )

    # rules = alt.Chart(filtered_coe).mark_rule(color='gray').encode(
    #     x='date:T',
    # ).transform_filter(
    #     nearest
    # )



    # chart = alt.layer(
    #     base, selectors, points, rules, text
    # ).properties(
    #     width=300, height=600
    # )

    chart = (bar + line).properties(width=600).resolve_scale(y='independent')




    return chart

def plotPremiumBB(df):
    df_bb = df.drop(columns=['bidding_no', 'month', 'vehicle_class'])
    # df_bb['date'] = pd.to_datetime(df_bb['date'])


    # Calculate the middle band (simple moving average)
    window_size = 12  # You can adjust the window size as needed
    df_bb['middle'] = df_bb['premium'].rolling(window=window_size).mean()
    std_dev = df_bb['premium'].rolling(window=window_size).std()
    # Calculate the upper and lower bands
    df_bb['upper_band'] = df_bb['middle'] + 2 * std_dev
    df_bb['lower_band'] = df_bb['middle'] - 2 * std_dev

    base = alt.Chart(df_bb).encode(x='date:O')

    # Line chart for COE Premium
    line_premium = base.mark_line(color='red').encode(
        y='premium:Q'
    )

    # Line chart for Middle Band
    line_middle = base.mark_line(color='green').encode(
        y='middle:Q'
    )

    # Area chart for Bollinger Band
    band = base.mark_area(opacity=0.5, color='gray').encode(
        y='lower_band:Q',
        y2='upper_band:Q'
    )

    # Combine the charts
    chart = (line_premium + line_middle + band).properties(
        width=600,
        height=500,
        title='COE Premium with Bollinger Band'
    ).encode(
        y=alt.Y('premium:Q', axis=alt.Axis(title='Premium'))
    )


    return chart

try:
    df_coe = pd.read_csv(coe_path)
    df_pqp = pd.read_csv(coePQP_path)
    df_coe['date'] = df_coe.apply(lambda row: f"{row['month']}-01" if row['bidding_no'] == 1 else f"{row['month']}-15", axis=1)

    vehicle_classes = df_coe['vehicle_class'].unique()
    v_class = st.selectbox(label = 'Category Selector', options=vehicle_classes)

    df_coe = df_coe[df_coe['vehicle_class'] == v_class]

    # Define the default range for the slider
    start_slider = int(len(df_coe) *  2/3)
    default_start_date = pd.to_datetime(df_coe['date'].iloc[start_slider]).date()
    default_end_date = pd.to_datetime(df_coe['date'].iloc[-1]).date()

    # Add the slider for date range selection
    start_date, end_date = st.slider(
        "Select Date Range",
        min_value=pd.to_datetime(df_coe['date'].iloc[0]).date(),
        max_value=pd.to_datetime(df_coe['date'].iloc[-1]).date(),
        value=(default_start_date, default_end_date),
        format="DDMMMYY"
    )

    # Filter the data based on the selected date range
    filtered_coe = df_coe[(df_coe['date'] >= start_date.strftime('%Y-%m-%d')) & (df_coe['date'] <= end_date.strftime('%Y-%m-%d'))]



    # Create the line chart
    st.altair_chart(plotBidPremium(filtered_coe),use_container_width=True)
    st.altair_chart(plotPremiumBB(filtered_coe),use_container_width=True)



    # Display the chart using Streamlit
    


except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
        """
        % e.reason
    )
