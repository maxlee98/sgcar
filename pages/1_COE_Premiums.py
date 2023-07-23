
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

st.title('COE Analytics')
st.write(
    """
    This demo shows a COE Premium price breakdown across a range of dates.

    """
)


current_path = os.getcwd()
coe_path = os.path.join(current_path, "data", 'M11-coe_results.csv')
coePQP_path = os.path.join(current_path, "data", 'M11-coe_results_pqp.csv')
pop_path = os.path.join(current_path, "data", 'MVP01-2_MVP_by_COE.csv')


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def plotCOEPremiumTrend(df):
 # Create the line chart
    nearest = alt.selection_point(nearest=True, on='mouseover',
                                fields=['date'], empty=False)
    brush = alt.selection_interval()
    base_chart = alt.Chart(df).mark_line().encode(
        x='date:T',
        y='premium:Q',
        color='vehicle_class:N'
    )

    selectors = alt.Chart(df).mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
    ).add_params(
        nearest
    )

    points = base_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = base_chart.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'premium:Q', alt.value(' '))
    )

    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )

    chart = alt.layer(
        base_chart, selectors, points, rules, text
    ).properties(
        width=300, height=600
    )

    return chart


def plotCOEPopulationTrend(df):

    # Altair chart components
    chart = alt.Chart(df).mark_bar().encode(
        x='year:O',
        y='number:Q',
        color='category:N',
        tooltip=['category:N', 'number:Q']
    ).properties(
        width=600,
        height=400,
        title='COE Category Population'
    )


    return chart


try:
    df_coe = pd.read_csv(coe_path)
    df_pqp = pd.read_csv(coePQP_path)
    df_pop = pd.read_csv(pop_path)
    

    df_coe['date'] = df_coe.apply(lambda row: f"{row['month']}-01" if row['bidding_no'] == 1 else f"{row['month']}-15", axis=1)
    vehicle_classes = list(set(list(df_pop['category'].unique()) + list(df_coe['vehicle_class'].unique())))
    vehicle_classes.sort()
    v_classes = st.multiselect(label = 'Category Selector', options=vehicle_classes, default=vehicle_classes)
    if len(v_classes) < 1:
        st.error("Please Select more than 1 category")
    else:
        df_coe = df_coe[df_coe['vehicle_class'].isin(v_classes)]
        df_pop = df_pop[df_pop['category'].isin(v_classes)]

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
        filtered_pop = df_pop[(df_pop['year'] >= start_date.year) & (df_pop['year'] <= end_date.year)]

        # Display the chart using Streamlit
        st.altair_chart(plotCOEPremiumTrend(filtered_coe),use_container_width=True)
        st.altair_chart(plotCOEPopulationTrend(filtered_pop),use_container_width=True)


except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
        """
        % e.reason
    )
