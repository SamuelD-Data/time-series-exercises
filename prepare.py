# imports
from acquire import df_combiner
from acquire import get_power
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


import warnings
warnings.filterwarnings("ignore")

from datetime import datetime
from sklearn.metrics import mean_squared_error
from math import sqrt 

import statsmodels.api as sm
from statsmodels.tsa.api import Holt


############# STORES, SALES, AND ITEMS DATA FUNCTIONS #############

# function retrieves sales, stores and items data then combines into single df 
def stores_sales_items_complete():
    """
    No arguments needed. Function retrieves data from 3 csv files then combines into single DF.
    """
    # reading in data from CSVs and storing
    stores = pd.read_csv('stores.csv') 
    items = pd.read_csv('items.csv')
    sales = pd.read_csv('sales.csv')
    
    # using function from acquire to combine DFs into single df
    df = df_combiner(items, stores, sales)
    
    # reading DF
    return df

# function combined df of sales, stores, and items data for exploration
def prep_all_data(df):
    """
    Accepts DF and preps it for exploration by changing date data type, setting date as index and adding new columns.
    """
    # convert sale_date column to datetime format
    df.sale_date = pd.to_datetime(df.sale_date)

    # set sale_date as index then sort df by index 
    df = df.set_index('sale_date').sort_index()

    # creating column with day name from sale_date (now index)
    df['day_week'] = df.index.day_name()

    # creating column with month name from sale_date (now index)
    df['month'] = df.index.month_name()

    # creating column with sales total calculated via sale_amount x item_price
    df['sales_total'] = df.sale_amount * df.item_price

    # returning dataframe
    return df

# creating function to convert date values to datetime format
def datetime_formatter(df):
    """
    Accepts DF. Converts sale_date column to datetime format then returns DF.
    """
    # converting date to datetime format
    df.sale_date = pd.to_datetime(df.sale_date)
    # returning df
    return df

# creating function that outputs distribution of 2 variables
def sales_plotter(dftime):
    """
    Accepts DF then creates plot of sale_amount and item_price.
    """
    # grouping by sales date and summing sale_amount from each date
    by_date = df.groupby(['sale_date']).sale_amount.sum().reset_index()
    # returning plot
    return by_date.plot(x='sale_date', y='sale_amount')

# creating function that sets date column as index
def date_time_indexer(dftime):
    """
    Accepts DF and returns with date column as index, sorted.
    """
    # setting sale_date column as index and sorting
    dftime = dftime.set_index("sale_date").sort_index()
    # returning DF
    return dftime

# function adds month and day of week column to DF
def month_day_adder(df):
    """
    Accepts DF. Adds column containing month and day of each sales. Returns DF.
    """
    # creating month and day of week columns
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    # returning df
    return df

# function calculates total sale amount
def sales_total_adder(df):
    """
    Accepts DF. Calculates total sale by multiplying sale_amount and item_price and add as new columns. Returns DF.
    """
    # creating new column sales_total and storing product of sale amount and item price
    df['sales_total'] = df.sale_amount * df.item_price
    # returning DF
    return df

############# GERMAN DATA FUNCTIONS #############

# creating function to convert date values to datetime format
def g_datetime_formatter(df):
    """
    Accepts DF. Converts date column to datetime format then returns DF.
    """
    # converting date to datetime format
    df.Date = pd.to_datetime(df.Date)
    # returning df
    return df

# function plots each variable in DF
def pairplotter(gdf):
    """
    Accepts DF and plots distribution of each variable via pairplot.
    """
    # creating pairplot
    return sns.pairplot(gdf)

# creating function that sets date column as index
def g_date_time_indexer(gdf):
    """
    Accepts DF and returns with date column as index, sorted.
    """
    # setting sale_date column as index and sorting
    gdf = gdf.set_index("Date").sort_index()
    # returning DF
    return gdf

# function adds month and year column to DF
def g_month_year_adder(gdf):
    """
    Accepts DF. Adds column containing month and year based on date column. Returns DF.
    """
    # creating month and year columns
    gdf['year'] = gdf.index.year
    gdf['month'] = gdf.index.month_name()
    # returning df
    return gdf

# function fills null values in various columns
def g_null_filler(gdf):
    """
    Accepts DF. Fills wind and solar null values with mean of respective columns. 
    Fills wind+solar null values with sum of respective values. 
    """
    # using fillna to fill null values
    gdf.Wind = gdf.Wind.fillna(gdf.Wind.mean())
    gdf.Solar = gdf.Solar.fillna(gdf.Solar.mean())
    gdf['Wind+Solar'] = gdf['Wind+Solar'].fillna(gdf.Solar + gdf.Wind)
    # returning df
    return gdf

# function acquires german data and prepares it for exploration
def germany_acquire_prep():
    """
    No arguments needed. Acquires germany data and preps for exploration via changing date to datetime format, setting date as index,
    creating new columns and filling null values.
    """
    # acquiring data
    df = get_power()

    # converting date column data type to datetime
    df.Date = pd.to_datetime(df.Date)

    # set date as index and sort df by date
    df = df.set_index("Date").sort_index()
    
    # creating columns that hold year and month of date
    df['year'] = df.index.year
    df['month'] = df.index.month_name()

    # filling wind and solar columns with avg. of their respective values
    df.Wind = df.Wind.fillna(df.Wind.mean())
    df.Solar = df.Solar.fillna(df.Solar.mean())

    # filling wind+solar nulls with sum of solar and wind
    df['Wind+Solar'] = df['Wind+Solar'].fillna(df.Solar + df.Wind)

    # returning DF
    return df

####### MODELING FUNCTIONS #######

def evaluate(target_var, test, yhat_df):
    """
    Calculates RMSE value of predictions vs actual values.
    """
    # calculate RMSE
    rmse = round(sqrt(mean_squared_error(test[target_var], yhat_df[target_var])), 0)
    # return RMSE value
    return rmse

def plot_and_eval(target_var, train, test, yhat_df, title):
    """
    Evaluates predictions using evaluate function 
    while also plotting train and test values with the predicted values in order to compare performance
    """
    # set figure size
    plt.figure(figsize = (15,7))
    plt.rc('font', size=16)
    # plot train and test target varaibles
    plt.plot(train[target_var], label='Train', linewidth=1)
    plt.plot(test[target_var], label='Test', linewidth=1)
    # plot predicted values
    plt.plot(yhat_df[target_var], label='Prediction')
    # set title
    plt.title(target_var)
    # calculate RMSE
    rmse = evaluate(target_var, test, yhat_df)
    # print RMSE value
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    # show legend
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Sales Total')
    plt.title(title)
    # show plot
    plt.show()
