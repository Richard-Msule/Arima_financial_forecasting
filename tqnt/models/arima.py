from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
import pandas as pd
import numpy as np
import tqnt.utils.utils as tqnt


class Arima:
    def __init__(self, df, ticker, start_p=1, start_q=1, max_p=10, max_q=10, split_ratio=0.8):
    #def __init__(self, df, ticker, start_p=1, start_q=1, max_p=10, max_q=10, split_ratio=0.8, seasonal_order=None):
        self.df = df
        self.ticker = ticker
        self.forecasts = []
        self.confidence_intervals = []
        self.scores = []

        self.train, self.test = tqnt.split_dataframe(self.df, split_ratio)
        self.train.index = pd.DatetimeIndex(self.train.index).to_period("D")
        self.test.index = pd.DatetimeIndex(self.test.index)
        self.model = pm.auto_arima(
            self.train,
            start_p=start_p,
            start_q=start_q,
            test="adf",  # use adftest to find optimal 'd'
            max_p=max_p,
            max_q=max_q,  # maximum p and q
            m=1,  # frequency of series
            d=None,  # let model determine 'd'
            seasonal=False,  # No Seasonality
            #seasonal_order=self.seasonal_order if self.seasonal_order else None,
            start_P=0,
            D=0,
            trace=True,
            error_action="ignore",
            suppress_warnings=True,
            stepwise=True,
        )

    def forecast_one_step(self):
        fc, conf_int = self.model.predict(n_periods=1, return_conf_int=True)
        fc_d, conf_d =  (fc.tolist()[0], np.asarray(conf_int).tolist()[0])
        self.forecasts.append(fc_d)
        self.confidence_intervals.append(conf_d)
        return fc_d, conf_d

    def forecast_multiple_steps(self, future_steps=1):
        forecasts = []
        confidence_intervals = []
        temp_series = self.df.copy()
    
        for _ in range(future_steps):
            # Forecast one step ahead
            forecast, conf_int = self.forecast_one_step()
    
            # Print to debug
            print(f"Forecasted value for step {_+1}: {forecast}")
    
            # Append the forecast and its confidence interval
            forecasts.append(forecast)
            confidence_intervals.append(conf_int)
    
            # Append the forecast to the temporary series for subsequent forecasting
            temp_series.at[temp_series.index[-1] + pd.Timedelta(days=1)] = forecast
            
            # Update the model with the latest forecasted value for the next iteration
            self.update_model(temp_series)
    
        return forecasts, confidence_intervals


    def get_forecasts(self):
        return self.forecasts

    def get_confidence_intervals(self):
        return self.confidence_intervals

    def get_scores(self):
        return self.scores
    
    def get_test_dataframe(self):
        return self.test.to_frame()

    def update_model(self, value):
        self.model.update(value)

    def test_model(self):
        for row in self.test:
            self.forecast_one_step()
            self.model.update(row)

        self.scores = tqnt.get_scores(self.test, self.forecasts , "Arima", self.ticker)
        return self.scores

