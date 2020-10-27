# imports
from acquire import df_combiner
from acquire import get_power
import pandas as pd
import seaborn as sns

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