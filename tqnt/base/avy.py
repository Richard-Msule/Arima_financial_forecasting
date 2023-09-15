import sys
sys.path.append('/workspaces/Arima_financial_forecasting')
import streamlit as st
import numpy as np
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt
from tqnt.models.arima import Arima
import yfinance as yf

def about_page():
    st.title("About ARIMA Forecasting App")
    st.markdown("""
    This app is designed to provide financial forecasting using the ARIMA model. 
    ARIMA stands for AutoRegressive Integrated Moving Average, a forecasting algorithm 
    based on the idea that information in past values of a time series can be used 
    to predict future points in the series.
    """)

def contact_page():
    st.title("Contact Information")
    st.markdown("""
    If you have questions or suggestions about this app, please reach out to:
    
    **Email**: example@email.com
    **Phone**: +123-456-7890
    **Address**: 123 Main St, Somewhere, Country
    """)

def disclaimer_page():
    st.title("Disclaimer")
    st.markdown("""
    The forecasts provided by this app are based on historical data and the ARIMA algorithm.
    They should not be used as the sole basis for investment decisions. Always consult with 
    a financial advisor before making investment choices.
    """)

def fetch_data(ticker, data_type, start_date=None, end_date=None):
    if data_type == 'Real-time':
        data = yf.download(ticker, period="7d", interval="1m")
    elif data_type == 'Historical':
        data = yf.download(ticker, start=start_date, end=end_date)
    return data['Close']

def get_forecasts(data, ticker):
    model = Arima(data, ticker)
    scores = model.test_model()
    forecasts = model.get_forecasts()
    confidence_intervals = model.get_confidence_intervals()
    return forecasts, confidence_intervals, scores, model

def app_forecasting():  
    st.markdown("""
    # ARIMA Forecasting for Financial Instruments
    This app uses ARIMA to forecast financial instruments using real-time or historical data from Yahoo Finance.
    """)
    
    ticker = st.sidebar.text_input('Ticker', 'AAPL').upper()
    data_type = st.sidebar.radio('Data Type', ['Real-time', 'Historical'])
    future_days = st.sidebar.slider('Days to Forecast Into the Future', 1, 30, 5)

    if data_type == 'Historical':
        start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2020-01-01'))
        end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-01-01'))

    if st.sidebar.button('Fetch Data', key='btn_fetch_data'):
        with st.spinner('Fetching data...'):
            try:
                data = fetch_data(ticker, data_type, start_date if data_type == 'Historical' else None, end_date if data_type == 'Historical' else None)

                st.subheader(f'{data_type} Data for {ticker}:')
                st.line_chart(data)
                st.subheader('Latest Data:')
                st.write(data.tail())
                st.subheader('Forecasting with ARIMA:')

                #model = Arima(data, ticker, seasonal_order=(1,0,1,7), seasonal_freq=7)
                model = Arima(data, ticker)

                if 'model' in locals():
                    forecasts, confidence_intervals, scores, model = get_forecasts(data, ticker)
                else:
                    st.error("Model is not defined yet!")

                #forecasts, confidence_intervals, scores, _ = get_forecasts(data, ticker)
                forecasts, confidence_intervals = model.forecast_multiple_steps(future_days)

                # Insert the debugging statements here:
                st.write(f"Number of forecast days: {future_days}")
                st.write(f"Length of forecasts: {len(forecasts)}")
                
                next_day = data.index[-1] + pd.Timedelta(days=1)
                forecast_dates = pd.date_range(start=next_day, periods=future_days)

                print(len(forecasts))  # should print 3 based on the error
                print(forecasts)
                print(len(forecast_dates))
                print(forecast_dates)
                
                forecasted_series = pd.Series(forecasts, index=forecast_dates)
                st.subheader('Forecasted Data:')
                st.write(forecasted_series)

                # Extract the lower and upper limits from confidence_intervals
                lower_limits = [interval[0] for interval in confidence_intervals]
                upper_limits = [interval[1] for interval in confidence_intervals]
                
                fig, ax = plt.subplots()
                ax.plot(data.index, data.values, label='Observed', color='blue')
                ax.plot(forecast_dates, forecasts, label='Forecast', color='red', alpha=0.7)
                ax.fill_between(forecast_dates, lower_limits, upper_limits, color='pink', alpha=0.3)  # Modified line
                ax.legend()
                st.pyplot(fig)

                #st.subheader('Scores:')
                #st.write(scores)
                # Convert scores into a pandas DataFrame and display
                scores_df = pd.DataFrame(list(scores.items()), columns=['Metric', 'Value'])
                st.subheader('Scores:')
                st.table(scores_df)

            #except Exception as e:
                #st.error(f"An error occurred: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                import traceback
                st.write(traceback.format_exc())

                
def landing_page():
    st.title("Welcome to ARIMA Forecasting App!")
    st.markdown("""
    This is a financial forecasting tool that uses ARIMA. 
    Please Register or Login to continue.
    """)

def registration_page():
    st.title("Registration Page")
    st.markdown("Enter your details to register:")
    username = st.text_input("Username", key='reg_username')
    password = st.text_input("Password", type='password', key='reg_password')
    confirm_password = st.text_input("Confirm Password", type='password', key='reg_confirm_password')

    if st.button('Register', key='btn_register_confirm'):
        if password == confirm_password:
            st.session_state.reg_username_state = username  # Store username
            st.session_state.reg_password_state = password  # Store password
            st.session_state.logged_in = True  # Log the user in
            st.session_state.page = "ARIMA Forecasting"  # Redirect to the main page
            st.success("Registration successful! You are now logged in.")
        else:
            st.error("Passwords do not match!")

     # Add navigation to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigation")
    if st.sidebar.button('Home', key='btn_home_reg'):
        st.session_state.page = "Landing"

def login_page():
    st.title("Login Page")
    st.markdown("Enter your credentials to login:")
    
    username = st.text_input("Username", key='login_username')
    password = st.text_input("Password", type='password', key='login_password')
    
    if st.button('Login', key='btn_login_confirm'):
        # Check credentials
        if st.session_state.reg_username_state and st.session_state.reg_password_state and \
           username == st.session_state.reg_username_state and password == st.session_state.reg_password_state:
            st.session_state.logged_in = True
            st.session_state.page = "ARIMA Forecasting"
        else:
            st.error("Invalid credentials!")

    # Add navigation to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigation")
    if st.sidebar.button('Home', key='btn_home_login'):
        st.session_state.page = "Landing"

def main():
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = "Landing"
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'reg_username_state' not in st.session_state:
        st.session_state.reg_username_state = ''
    if 'reg_password_state' not in st.session_state:
        st.session_state.reg_password_state = ''

    pages = {
        "Landing": landing_page,
        "About": about_page,
        "Contact": contact_page,
        "Disclaimer": disclaimer_page,
        "Register": registration_page,
        "Login": login_page,
        "ARIMA Forecasting": app_forecasting
    }

    # Sidebar navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigation")

    # Let's have main buttons always visible on the sidebar
    if st.sidebar.button('Home'):
        st.session_state.page = "Landing"
    if st.sidebar.button('About'):
        st.session_state.page = "About"
    if st.sidebar.button('Contact'):
        st.session_state.page = "Contact"
    if st.sidebar.button('Disclaimer'):
        st.session_state.page = "Disclaimer"
    
    if st.session_state.logged_in:
        if st.sidebar.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.page = "Landing"
            st.experimental_rerun()
    else:
        if st.sidebar.button('Register'):
            st.session_state.page = "Register"
        if st.sidebar.button('Login'):
            st.session_state.page = "Login"

    # Check login status
    if st.session_state.page == "ARIMA Forecasting" and not st.session_state.logged_in:
        st.warning("Please login first.")
        st.session_state.page = "Login"

    # Render the chosen page function
    pages[st.session_state.page]()

if __name__ == '__main__':
    main()