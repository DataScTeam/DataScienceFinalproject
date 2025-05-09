import streamlit as st
import joblib
import pandas as pd
import numpy as np
import altair as alt

def load_model():
    return joblib.load("sales_forecast_model.pkl")

@st.cache_data
def load_data():
    df = pd.read_csv('retail_store_inventory.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Price Diff'] = df['Price'] - df['Competitor Pricing']
    def get_season(m):
        if m in [3,4,5]: return 'Spring'
        if m in [6,7,8]: return 'Summer'
        if m in [9,10,11]: return 'Autumn'
        return 'Winter'
    df['Season'] = df['Date'].dt.month.map(get_season)
    df['YearMonth'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    return df

st.set_page_config(page_title="Retail Sales App", layout="wide")
st.title("Retail Sales Application")
type_choice = st.sidebar.selectbox(
    "Select Mode:",
    ["Prediction", "Visualization"]
)

if type_choice == "Prediction":
    st.header("Sales Prediction")
    st.markdown("Enter the following values to get the prediction:")

    model = load_model()

    month = st.slider("Month", 1, 12, 1)
    day_of_week = st.selectbox(
        "Day of the Week",
        options=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')],
        format_func=lambda x: x[1]
    )[0]
    discount = st.slider("Discount %", 0, 50, 5)
    holiday = st.radio("Is there a promotional offer or a holiday?", [1, 0])
    season = st.selectbox("Season", ['Spring', 'Summer', 'Autumn', 'Winter'])
    weather = st.selectbox("Weather State", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])
    demand_forecast = st.number_input("Order forecast (from the system)", min_value=0, value=300)
    competitor_price = st.number_input("Competitor's price", min_value=0, value=100)
    price = st.number_input("Actual price", min_value=0, value=100)
    category = st.selectbox("Category", ['Groceries', 'Toys', 'Electronics', 'Furniture', 'Clothing'])
    region = st.selectbox("Region", ['North', 'South', 'East', 'West'])

    if st.button("Calculate Prediction"):
        input_data = pd.DataFrame([{
            'Month': month,
            'DayOfWeek': day_of_week,
            'Discount': discount,
            'Holiday/Promotion': holiday,
            'Category': category,
            'Region': region,
            'Weather Condition': weather,
            'Seasonality': season,
            'Demand Forecast': demand_forecast,
            'Competitor Pricing': competitor_price,
            'Price': price
        }])
        prediction = int(model.predict(input_data)[0])
        st.success(f"Number of units sold ≈ {prediction} units")

else:
    st.header("Interactive Retail Store Inventory Dashboard")
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Data file 'updated_data.csv' not found. Please place it in the app directory.")
        st.stop()

    st.sidebar.header("Filters")
    min_date, max_date = st.sidebar.date_input(
        "Select Date Range", [df['Date'].min(), df['Date'].max()]
    )
    categories = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())
    regions = st.sidebar.multiselect("Region", options=df['Region'].unique(), default=df['Region'].unique())
    weathers = st.sidebar.multiselect("Weather Condition", options=df['Weather Condition'].unique(), default=df['Weather Condition'].unique())
    disc_range = st.sidebar.slider("Discount Range (%)", 0, 90, (0, 90))
    price_range = st.sidebar.slider("Price Range", 0, 100, (0, 100))

    mask = (
        (df['Date'] >= pd.to_datetime(min_date)) &
        (df['Date'] <= pd.to_datetime(max_date)) &
        df['Category'].isin(categories) &
        df['Region'].isin(regions) &
        df['Weather Condition'].isin(weathers) &
        df['Discount'].between(disc_range[0], disc_range[1]) &
        df['Price'].between(price_range[0], price_range[1])
    )
    filtered = df[mask]

    st.subheader("Units Sold by Day of the Week")
    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    data_day = (filtered.groupby('DayOfWeek')['Units Sold'].sum().reindex(order).reset_index())
    chart_day = alt.Chart(data_day).mark_bar().encode(
        x=alt.X('DayOfWeek:O', sort=order), y='Units Sold:Q', tooltip=['DayOfWeek','Units Sold']
    ) + alt.Chart(data_day).mark_line(point=True).encode(
        x=alt.X('DayOfWeek:O', sort=order), y='Units Sold:Q'
    )
    st.altair_chart(chart_day, use_container_width=True)

    st.subheader("Total Units Sold by Discount Level")
    data_disc = filtered.groupby('Discount')['Units Sold'].sum().reset_index()
    chart_disc = alt.Chart(data_disc).mark_bar().encode(
        x='Discount:O', y='Units Sold:Q', tooltip=['Discount','Units Sold']
    ) + alt.Chart(data_disc).mark_line(point=True).encode(
        x='Discount:O', y='Units Sold:Q'
    )
    st.altair_chart(chart_disc, use_container_width=True)

    st.subheader("Heat Map: Avg Units Sold by Weather & Day")
    pivot = filtered.pivot_table(index='Weather Condition', columns='DayOfWeek', values='Units Sold', aggfunc='mean').reindex(columns=order)
    heat_data = pivot.reset_index().melt(id_vars=['Weather Condition'], var_name='Day', value_name='AvgUnits')
    chart_heat = alt.Chart(heat_data).mark_rect().encode(
        x=alt.X('Day:O', sort=order), y='Weather Condition:O', color='AvgUnits:Q', tooltip=['Weather Condition','Day','AvgUnits']
    )
    st.altair_chart(chart_heat, use_container_width=True)

    st.subheader("Promotion & Holiday Effects")
    non = filtered[filtered['Holiday/Promotion'] == 0]['Units Sold'].sum()
    promo = filtered[filtered['Holiday/Promotion'] == 1]['Units Sold'].sum()
    df_w = pd.DataFrame({
        'Stage': ['Non-Promo','Promo','Total'],
        'Units Sold': [non, promo, non+promo]
    })
    chart_w = alt.Chart(df_w).mark_bar().encode(x='Stage:O', y='Units Sold:Q', tooltip=['Stage','Units Sold'])
    st.altair_chart(chart_w, use_container_width=True)

    def plot_scatter(x_col, y_col, title):
        st.subheader(title)
        chart = alt.Chart(filtered).mark_circle(size=60, opacity=0.3).encode(
            x=f'{x_col}:Q', y=f'{y_col}:Q', tooltip=[x_col, y_col]
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

    plot_scatter('Price', 'Units Sold', 'Price vs Units Sold')
    plot_scatter('Price Diff', 'Units Sold', 'Price Diff vs Units Sold')
    plot_scatter('Inventory Level', 'Units Sold', 'Inventory Level vs Units Sold')
    plot_scatter('Units Ordered', 'Units Sold', 'Units Ordered vs Units Sold')

    st.subheader("Forecast vs Actual over Time")
    agg_time = filtered.groupby('YearMonth').agg({'Units Sold':'sum','Demand Forecast':'sum'}).reset_index()
    folded = agg_time.melt(id_vars=['YearMonth'], value_vars=['Units Sold','Demand Forecast'], var_name='Variable', value_name='Value')
    chart_time = alt.Chart(folded).mark_line(point=True).encode(
        x='YearMonth:T', y='Value:Q', color='Variable:N', tooltip=['YearMonth','Variable','Value']
    ).interactive()
    st.altair_chart(chart_time, use_container_width=True)

    st.subheader("Units Sold by Category, Region, Season")
    agg_cat = filtered.groupby('Category')['Units Sold'].sum().reset_index()
    agg_reg = filtered.groupby('Region')['Units Sold'].sum().reset_index()
    agg_sea = filtered.groupby('Season')['Units Sold'].sum().reset_index()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.altair_chart(alt.Chart(agg_cat).mark_bar().encode(x='Category:O', y='Units Sold:Q', tooltip=['Category','Units Sold']), use_container_width=True)
    with col2:
        st.altair_chart(alt.Chart(agg_reg).mark_bar().encode(x='Region:O', y='Units Sold:Q', tooltip=['Region','Units Sold']), use_container_width=True)
    with col3:
        st.altair_chart(alt.Chart(agg_sea).mark_bar().encode(x='Season:O', y='Units Sold:Q', tooltip=['Season','Units Sold']), use_container_width=True)

    st.subheader("Correlation Matrix")
    corr = filtered[['Price','Discount','Units Sold','Units Ordered','Demand Forecast','Inventory Level','Competitor Pricing']].corr()
    corr_reset = corr.reset_index().melt(id_vars='index', var_name='Variable', value_name='Correlation')
    chart_corr = alt.Chart(corr_reset).mark_rect().encode(
        x=alt.X('Variable:O', sort=list(corr.columns)), y=alt.Y('index:O', sort=list(corr.index)), color='Correlation:Q', tooltip=['index','Variable','Correlation']
    )
    st.altair_chart(chart_corr, use_container_width=True)

#    python -m streamlit run "DataScTeam/DataScienceFinalproject/app.py"