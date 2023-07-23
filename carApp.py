import streamlit as st

st.set_page_config(
    page_title="Car Analytics",
    page_icon=":bar_chart:",
)

st.write("# Welcome to Car Analytics! :bar_chart:")

# st.sidebar.success("Select a demo above.")
st.warning("Do let each page finish loading prior to switching onto other pages")

st.markdown(
    """
    The Car Analytics App was built specifically for analysing if one should purcahse a car at any point in time, that being relative to time.
    
    **Currently data is only updated to June 2023.**

    Click on the side bar to begin exploring!
    ## Pages Available


    """    

)

st.info("This dashboard is still under-development and may experience performance issues.  If there are any issues with regards to loading a page, do reload the page.")


st.markdown(
    """

    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)

    References:
    - LTA. (2023, Janurary). Annual Motor Vehicle Population by Vehicle Quota Categories. Land Transport Data Mall. Retrieved July, 2023, from https://datamall.lta.gov.sg/content/datamall/en/static-data.html
    - LTA. (2023, June). COE Bidding Results. Land Transport Data Mall. Retrieved June, 2023, from https://datamall.lta.gov.sg/content/datamall/en/static-data.html

"""
)