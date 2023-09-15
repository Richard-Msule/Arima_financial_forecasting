# Arima Financial Forecasting

Arima Financial Forecasting is a project that uses the ARIMA (AutoRegressive Integrated Moving Average) model to forecast the future values of financial time series data. The project is based on the paper "Forecasting Stock Prices Using ARIMA Model" by K. Senthamarai Kannan, P. Sailapathi Sekaran, M.Mohamed Sathik and P. Arumugam¹.

## Motivation

The motivation behind this project is to explore the applicability and performance of the ARIMA model in forecasting financial data, such as stock prices, exchange rates, and inflation rates. The project aims to provide a simple and user-friendly interface for users to input their own data and parameters, and obtain the forecasted values and graphs.

## Installation

To run this project, you need to have Python 3 installed on your machine. You also need to install the following Python libraries:

- pandas
- numpy
- matplotlib
- statsmodels
- pmdarima
- streamlit

You can install them using pip:

```bash
pip install pandas numpy matplotlib statsmodels pmdarima
```

Alternatively, you can use the `pyproject.toml` file provided in the repository:

```bash
pip install poetry #then
 poetry install #in your project directory to install the dependencies specified in your pyproject.toml file.
```

## Usage

To use this project, you need to clone or download the repository from GitHub:

```bash
git clone [2](https://github.com/Richard-Msule/Arima_financial_forecasting.git)
cd Arima_financial_forecasting
```

Then, you can run the `avy.py` file using Python:

```bash
streamlit run avy.py
```

This will launch a graphical user interface (GUI) where you can select your data file, choose the ARIMA parameters (p, d, q), and click on the "Forecast" button. The program will then display the original and forecasted data on a plot, as well as the mean absolute error (MAE) and the root mean square error (RMSE) of the forecast.

You can also use the `arima.py` file as a module in your own Python scripts. For example, you can import it and use the `forecast` function to get the forecasted values and errors:

```python
import arima

# Load your data as a pandas Series
data = ...

# Specify the ARIMA parameters
p = ...
d = ...
q = ...

# Get the forecasted values and errors
forecast, mae, rmse = arima.forecast(data, p, d, q)

# Print or plot the results
print(forecast)
print(mae)
print(rmse)
```

## Citation

If you use this project in your research or work, please cite it as follows:

```bibtex
@misc{msule2023,
  author = {Msule, Richard},
  title = {Arima Financial Forecasting},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{[2](https://github.com/Richard-Msule/Arima_financial_forecasting)}}
}
```

## References

¹: Kannan, K.S., Sekaran, P.S., Sathik, M.M. and Arumugam, P., 2010. Forecasting stock prices using ARIMA model. International Journal of Computer Applications in Engineering Sciences (IJCAES), 1(2), pp.77-80.

