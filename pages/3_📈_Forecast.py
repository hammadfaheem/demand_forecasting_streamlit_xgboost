import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

st.set_page_config(page_title="Let's Forecast!", page_icon="📈")
st.sidebar.header("Choose the model you want to use -")

# title
st.title("Let's Forecast!")
st.markdown("##### <span style='color: #5D6D7E'>Let's use our models to forecast over a time period of our choice \
and plot it against actual data!</span>", unsafe_allow_html=True)

# function to load data
@st.cache_data
def load_data(filename):
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

# creating sidebars to select model for evaluation
# selecting 'Baseline: Naïve Forecast'
if st.sidebar.checkbox('Baseline: Naïve Forecast'):
    st.markdown("##### <span style='color: #E65100'>Baseline Method: Naïve Forecast</span>", unsafe_allow_html=True)
    # loading data
    combined_data = load_data('data/combined_data.csv')
    # creating a filter to select forecast period
    st.markdown('**Forecast Period:**')
    period = st.selectbox('Choose forecast period', ['1 day', '7 days', '30 days', '90 days'])
    n = int(period.split()[0])
    # preparing the data and selecting data based on the period
    combined_data['forecast'] = combined_data['total_demand'].shift(1)
    train_idx = combined_data[combined_data.index.year<2020].index
    test_idx = combined_data[combined_data.index.year> 2019].index
    data = combined_data.loc[train_idx[-5:].append(test_idx[:n]),]
    data.index = data.index.date
    # plotting the forecast and actual values using plotly graph objects
    # instantiating figure
    fig = go.Figure()
    # creating the hover template
    ht = "<br>".join([
        "Date: %{customdata[0]}",
        "Demand: %{y}"
    ])
    cd = np.stack([data.index, data.total_demand, data.forecast], axis=-1)
    # adding line charts
    fig.add_trace(go.Scatter(
        x=data.index.values,
        y=data.total_demand,
        name="Demand",
        customdata=cd,
        hovertemplate=ht,
        line=dict(color='#4FC3F7')
    ))
    fig.add_trace(go.Scatter(
        x=data.index.values,
        y=data.forecast,
        name="Forecast",
        customdata=cd,
        hovertemplate=ht,
        line=dict(color='#FF6F00')
    ))
    # inserting a vertical line to mark the point from where the forecast begins
    fig.add_vline(x=data.index[4], line_width=3, line_dash="dash", line_color="#ABB2B9")
    # updating the layout to add title and labels
    fig.update_layout(
        title="Daily Total Demand vs Forecast",
        xaxis_title="Date Range",
        yaxis_title="Daily Total Demand / Daily Forecast",
        legend_title="legend",
        font=dict(family="Arial", size=12, color='darkslategray'),
        width=800, height=500
    )
    st.plotly_chart(fig)
    # calculating the MAPE and RMSE
    mape = round(mean_absolute_percentage_error(data.total_demand[-n:], data.forecast[-n:]),2)
    rmse = round(np.sqrt(mean_squared_error(data.total_demand[-n:], data.forecast[-n:])),2)
    st.write(f'**Mean Absolute Percentage Error: {mape}%**')
    st.write(f'**Root Mean Squared Error: {rmse}**')
    # viewing the dataframe
    st.markdown("###### <span style='color: #01579B'>Actual Demand vs. Forecast- Dataset</span>", unsafe_allow_html=True)
    st.dataframe(data.loc[data.index[5:],['total_demand', 'forecast']])

# selecting 'XGBoost'
if st.sidebar.checkbox('XGBoost'):
    st.markdown("##### <span style='color: #E65100'>XGBoost - Our Best Performing Model</span>", unsafe_allow_html=True)
    st.markdown('**Forecast Period:**')
     # creating a filter to select forecast period
    period_xgb = st.selectbox('Choose forecast period', ['1 day', '7 days', '30 days', '90 days'], key='period_xgb')
    n = int(period_xgb.split()[0])
    # loading the model
    model = joblib.load('models/xgb_gs_best_estimator.pkl')
    # loading the data
    combined_data_2 = load_data('data/combined_data.csv')
    # preparing the data for the xgboost model
    combined_data_2['total_demand_lag_1'] = combined_data_2.total_demand.shift(periods=1, fill_value=0)
    combined_data_2['total_demand_lag_2'] = combined_data_2.total_demand.shift(periods=2, fill_value=0)
    combined_data_2['total_demand_lag_3'] = combined_data_2.total_demand.shift(periods=3, fill_value=0)
    combined_data_2['total_demand_lag_4'] = combined_data_2.total_demand.shift(periods=4, fill_value=0)
    combined_data_2['total_demand_lag_5'] = combined_data_2.total_demand.shift(periods=5, fill_value=0)
    combined_data_2['total_demand_lag_6'] = combined_data_2.total_demand.shift(periods=6, fill_value=0)
    combined_data_2['total_demand_lag_7'] = combined_data_2.total_demand.shift(periods=7, fill_value=0)
    X = combined_data_2.drop(columns='total_demand')
    y = combined_data_2.total_demand
    # using the loaded xgboost model to make predictions
    combined_data_2['forecast_xgb'] = model.predict(X.values)
    # preparing the data for plotting
    train_idx = combined_data_2[combined_data_2.index.year<2020].index
    test_idx = combined_data_2[combined_data_2.index.year> 2019].index
    data = combined_data_2.loc[train_idx[-5:].append(test_idx[:n]),]
    data.index = data.index.date
    # plotting the forecast and actual values using plotly graph objects
    # instantiating figure
    fig = go.Figure()
    # creating the hover template
    ht = "<br>".join([
        "Date: %{customdata[0]}",
        "Demand: %{y}"
    ])
    cd = np.stack([data.index, data.total_demand, data.forecast_xgb], axis=-1)
    # adding line charts
    fig.add_trace(go.Scatter(
        x=data.index.values,
        y=data.total_demand,
        name="Demand",
        customdata=cd,
        hovertemplate=ht,
        line=dict(color='#4FC3F7')
    ))
    fig.add_trace(go.Scatter(
        x=data.index.values,
        y=data.forecast_xgb,
        name="Forecast",
        customdata=cd,
        hovertemplate=ht,
        line=dict(color='#FF6F00')
    ))
    # inserting a vertical line to mark the point from where the forecast begins
    fig.add_vline(x=data.index[4], line_width=3, line_dash="dash", line_color="#ABB2B9")
    # updating the layout to add title and labels
    fig.update_layout(
        title="Daily Total Demand vs Forecast",
        xaxis_title="Date Range",
        yaxis_title="Daily Total Demand / Daily Forecast",
        legend_title="legend",
        font=dict(family="Arial", size=12, color='darkslategray'),
        width=800, height=500
    )
    st.plotly_chart(fig)
    # calculating the MAPE and RMSE
    mape = round(mean_absolute_percentage_error(data.total_demand[-n:], data.forecast_xgb[-n:]), 2)
    rmse = round(np.sqrt(mean_squared_error(data.total_demand[-n:], data.forecast_xgb[-n:])), 2)
    st.write(f'**Mean Absolute Percentage Error: {mape}%**')
    st.write(f'**Root Mean Squared Error: {rmse}**')
    # viewing the dataframe
    st.markdown("###### <span style='color: #01579B'>Actual Demand vs. Forecast- Dataset</span>", unsafe_allow_html=True)
    st.dataframe(data.loc[data.index[5:], ['total_demand', 'forecast_xgb']])
