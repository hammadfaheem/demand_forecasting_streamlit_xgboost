# importing libraries
import streamlit as st
import base64

st.set_page_config(page_title='Home',page_icon=":house:")
st.sidebar.header("About")

# title
st.title("Bike Share: Demand Forecasting")

# introduction
st.markdown("##### <span style='color: #5D6D7E'>Welcome to this app on visualizing and forecasting \
the demand of bicycles in Washington DC.</span>", unsafe_allow_html=True)
st.markdown("##### <span style='color: #E65100'>Have fun 🎉!</span>", unsafe_allow_html=True)

# adding gif
file_ = open("assets/bike_2_giphy.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="bike gif">',
    unsafe_allow_html=True,
)
