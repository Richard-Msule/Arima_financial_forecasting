import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_percentage_error


def sink(df, output):
    df.to_csv(output, index=False)


def resample_to(df, period):
    return df.resample(period).last()


def select_range(df, start, end):
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    return df[(df.index >= start_date) & (df.index <= end_date)]


def load_dataframe(filename):
    return pd.read_csv(filename)


def prepare_data(df, feature="Close"):
    df.dropna(inplace=True)
    df["Return"] = df[feature].pct_change()
    df["Log_Return"] = np.log(df[feature]).diff()
    df.dropna(inplace=True)
    return df


# Define a function to split the data frame into training and testing
def split_dataframe(df, train_size=0.75):
    split = int(df.shape[0] * train_size)
    return df.iloc[:split].copy(), df.iloc[split:].copy()


def get_scores(train, forecasts, model, ticker):
    r2 = r2_score(train, forecasts)
    mape = mean_absolute_percentage_error(train, forecasts)
    corr = np.corrcoef(forecasts, train)[0, 1]  # corr

    return {
        "Size_train": len(train),
        "Size_forecasts": len(forecasts),
        "Model": model,
        "Ticker": ticker,
        "R2_score": r2,
        "Mape": mape,
        "Corr": corr,
    }


def append_scores(df, results, model, ticker, features):
    r2 = r2_score(results[features], results["Predictions"])
    mape = mean_absolute_percentage_error(results[features], results["Predictions"])
    corr = np.corrcoef(results["Predictions"], results[features])[0, 1]  # corr

    df.append(
        {
            "Size": results.shape[0],
            "Model": model,
            "Ticker": ticker,
            "R2_score": r2,
            "Mape": mape,
            "Corr": corr,
        }
    )

    return df

def intersect_on_index(base_df, other_df):
    outcome_f = pd.merge(
        base_df,
        other_df,
        left_index=True,
        right_index=True,
        how="outer",
        indicator=True,
    )
    return outcome_f.loc[outcome_f._merge == "both", base_df.columns]

def get_data_from_past_x_months(past_months, df):
    start_date = df.index[-1] - pd.tseries.offsets.MonthBegin(past_months)
    tmp = df[start_date:].copy()
    return tmp

