# importing libraries
import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import plotly.express as px

st.set_page_config(page_title='Meet The Data', page_icon="📊")
st.sidebar.header("Choose the dataset you want to explore -")

# title
st.title("Meet The Data!")

# introduction
st.markdown("##### <span style='color: #5D6D7E'>Let's explore our data and build an understanding of the data \
we are working with!</span>", unsafe_allow_html=True)

# function to load data
@st.cache_data
def load_data(filename):
    data = pd.read_csv(filename)
    data.dropna(inplace=True)
    return data

# function to load and combine data
def load_combined_data(filename):
    data = pd.read_csv(filename, index_col=0)
    data.index = pd.to_datetime(data.index)
    train_data = data[data.index.year < 2020]
    test_data = data[data.index.year > 2021]
    new_date_index = pd.date_range(start=train_data.index.max() + pd.DateOffset(days=1),
                                   periods=len(test_data), freq='D')
    test_data_reindexed = pd.DataFrame(data=test_data[test_data.columns].values,
                                             columns=test_data.columns,
                                             index=new_date_index)
    combined_data = pd.concat([train_data, test_data_reindexed], axis=0)
    data.dropna(inplace=True)
    return combined_data

# creating sidebars to select data for visualization
# selecting 'Bike Rental Data' to plot visualizations for 'Average Bike Rental By Station'
if st.sidebar.checkbox('Bike Rental Data'):
    st.markdown("##### <span style='color: #E65100'>Bike Rental Data</span>", unsafe_allow_html=True)
    st.markdown('**Average Bike Rental By Station:**')
    # adding a time span filter
    target = st.selectbox('Choose a time frame', ['daily', 'weekly', 'monthly'])
    # loading data
    file_path = f'data/{target}_avg_by_station.csv'
    df = load_data(file_path)

    # visualizing 'Average Bike Rental By Station' for the chosen time span on a map using pydeck library
    view = pdk.data_utils.compute_view(df[["lon", "lat"]])
    # initializing the view
    view.pitch = 70
    view.bearing = 40
    if target != 'daily':
        view.zoom = 8
    else:
        view.zoom = 10
    # initializing the pydeck column layer
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=df,
        get_position=["lon", "lat"],
        get_elevation="bike_counts",
        elevation_scale=200,
        radius=50,
        elevation_range=[0, 1000],
        get_fill_color=["bike_counts*6", "bike_counts", "bike_counts*6", 140],
        pickable=True,
        auto_highlight=True,
    )
    # customizing tooltip
    tooltip = {
        "html": "Station ID: <b>{start_station_id}</b> <br> Station Name: <b>{start_station_name}</b> <br> Average Bikes Rented: <b>{bike_counts}</b>",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }
    # building the pydeck chart
    st.pydeck_chart(
        pdk.Deck(
            column_layer,
            initial_view_state=view,
            tooltip=tooltip,
            # initial_view_state={
            #     "latitude": 38.85,
            #     "longitude": -77.05,
            #     "zoom": 11,
            #     "pitch": 50,
            # },
            map_style="mapbox://styles/mapbox/light-v9",
        )
    )

    # visualizing the 'Best/Worst Performing Stations By Average Bike Rental'
    st.markdown('**Best/Worst Performing Stations By Average Bike Rental:**')
    # creating a filter to select criterion
    criterion = st.selectbox('Choose criterion', ['best', 'worst'])
    # creating a slider to select max values to display
    num = st.slider('Choose range', min_value=5, max_value=50, value=10, step=1)
    # sorting data based on criterion
    if criterion=='best':
        temp_df = df.sort_values(by='bike_counts', axis=0, ascending=False).iloc[:num,:]
    else:
        temp_df = df.sort_values(by='bike_counts', axis=0, ascending=True).iloc[:num, :]
    # st.bar_chart(data=temp_df, x='start_station_name', y='bike_counts', color='#2E86C1')
    # plotting using plotly
    fig = px.bar(temp_df, x="start_station_name", y="bike_counts")
    fig.update_traces(marker_color='#CC66FF')
    fig.update_layout(
        title=f"The {num} {criterion.capitalize()} Stations By Total Demand",
        xaxis_title="Station Name",
        yaxis_title="Total Demand",
        legend_title="legend",
        font=dict(family="Arial", size=12, color='darkslategray'),
        width=800, height=500
    )
    st.plotly_chart(fig)

    # visualizing the 'Average Total Bike Rental'
    st.markdown('**Average Total Bike Rental:**')
    # loading data
    file_path_2 = f'data/{target}.csv'
    df_2 = load_data(file_path_2)
    df_2 = df_2.loc[:,['date', 'bike_counts']]
    df_2 = df_2.sort_values(by='date')
    # adding a progress bar to the sidebar
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    # initializing the chart
    last_rows = df_2.iloc[0:1, :]
    chart = st.line_chart(data=last_rows, x='date', y='bike_counts', color='#8E24AA')
    # creating the dynamic plot
    upper = len(df_2)
    for i in range(1, upper+1):
        # updating status text on the sidebar
        status_text.text(f"{round(i*100/upper)}% Complete")
        # fetching the next row from the data to plot
        new_rows = df_2.iloc[i:i+1, :]
        # adding rows to the streamlit line chart
        chart.add_rows(new_rows)
        # updating progress bar
        progress_bar.progress(round(i*100/upper))
        last_rows = new_rows
        # managing the speed at which the new points are plotted
        time.sleep(0.05)

    # reset
    progress_bar.empty()
    st.button("Re-run")

# selecting 'Weather Data' to plot visualizations for average temperature/rainfall by month'
if st.sidebar.checkbox('Weather Data'):
    st.markdown("##### <span style='color: #E65100'>Weather Data</span>", unsafe_allow_html=True)
    st.markdown('**Average Temperature By Month:**')
    # target = st.selectbox('Choose a time frame', ['daily', 'weekly', 'monthly'])
    # loading data
    combined_data = load_combined_data('data/combined_data.csv')
    # preparing monthly average temperature data
    monthly_avg_temp = combined_data.groupby(combined_data.index.month)['temp_obs'].mean()
    monthly_avg_temp = monthly_avg_temp.to_frame().reset_index()
    monthly_avg_temp = monthly_avg_temp.rename({'index': 'month'}, axis=1)
    # plotting a line chart using plotly
    fig = px.line(monthly_avg_temp, x='month', y="temp_obs")
    fig.update_traces(line=dict(width=4, color='#EF6C00'))
    fig.update_layout(
        title="Average Observed Temperature (tenths of °C) By Month",
        xaxis_title="Month",
        yaxis_title="Observed Temperature (tenths of °C)",
        legend_title="legend",
        font=dict(family="Arial", size=12, color='darkslategray'),
        xaxis=dict(
            tickmode='array',
            tickvals=[1,2,3,4,5,6,7,8,9,10,11,12],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        width=800, height=500
    )
    st.plotly_chart(fig)

    st.markdown('**Average Rainfall By Month:**')
    # preparing monthly average precipitation data
    monthly_avg_prcp = combined_data.groupby(combined_data.index.month)['prcp'].mean()
    monthly_avg_prcp = monthly_avg_prcp.to_frame().reset_index()
    monthly_avg_prcp = monthly_avg_prcp.rename({'index': 'month', 'prcp': 'rainfall'}, axis=1)
    # plotting using plotly
    fig = px.line(monthly_avg_prcp, x='month', y="rainfall")
    fig.update_traces(line=dict(width=4, color='#1E88E5'))
    fig.update_layout(
        title="Average Observed Rainfall (tenths of mm) By Month",
        xaxis_title="Month",
        yaxis_title="Rainfall (tenths of mm)",
        legend_title="legend",
        font=dict(family="Arial", size=12, color='darkslategray'),
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        width=800, height=500
    )
    st.plotly_chart(fig)


