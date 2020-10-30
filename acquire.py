# acquire file for time series exercises

# imports
import requests
import pandas as pd

############ HEB DATA FUNCTIONS ############
# function to retrieve items data
def get_items_data():
    '''
    Creates df using data from base url 
    then retrieves data from each sequential page and combines all into one DF.
    '''
    # setting base URL (ie. first page of data)
    base_url = 'https://python.zach.lol/api/v1/items'

    # saving object retrieved from requests function being passed argument URL
    response = requests.get(base_url)
    
    # saving data from .json object
    data = response.json()
    
    # saving first page of items data to df
    df = pd.DataFrame(data['payload']['items'])
    
    # iterating range = 1 through max page count
    for i in range (1, data['payload']['max_page']):
        # passing url for next page to request.get function
        response = requests.get(base_url[:23] + data['payload']['next_page'])
        
        # saving data from response in .json format
        data = response.json()
        
        # concating each new page's data to original df
        df = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index(drop=True)
    
    # returning df
    return df

# function to retrieve stores data
def get_stores_data(base_url):
    '''
    Accepts url. Create df using data from base url 
    then retrieves data from each sequential page and combines all into one DF.
    '''
    # saving object retrieved from requests function being passed argument URL
    response = requests.get(base_url)
    
    # saving data from .json object
    data = response.json()
    
    # saving first page of stores data to df
    df = pd.DataFrame(data['payload']['stores'])
    
    # iterating range = 1 through max page count
    for i in range (1, data['payload']['max_page']):
        # passing url for next page to request.get function
        response = requests.get(base_url[:23] + data['payload']['next_page'])
        
        # saving data from response in .json format
        data = response.json()
        
        # concating each new page's data to original df
        df = pd.concat([df, pd.DataFrame(data['payload']['stores'])]).reset_index(drop=True)
    
    # returning df
    return df

# function to retrieve sales data
def get_sales_data(base_url):
    '''
    Accepts url. Create df using data from base url 
    then retrieves data from each sequential page and combines all into one DF.
    '''
    # saving object retrieved from requests function being passed argument URL
    response = requests.get(base_url)
    
    # saving data from .json object
    data = response.json()
    
    # saving first page of sales data to df
    df = pd.DataFrame(data['payload']['sales'])
    
    # iterating range = 1 through max page count
    for i in range (1, data['payload']['max_page']):
        # passing url for next page to request.get function
        response = requests.get(base_url[:23] + data['payload']['next_page'])
        
        # saving data from response in .json format
        data = response.json()
        
        # concating each new page's data to original df
        df = pd.concat([df, pd.DataFrame(data['payload']['sales'])]).reset_index(drop=True)
    
    # returning df
    return df

# function converts DFs to csv files
def csv_maker(items, stores, sales):
    """
    Accepts 3 DFs. Converts passed DFs to csv files then returns DFs.
    """
    # converting DFs
    items.to_csv('items.csv', index=False)
    stores.to_csv('stores.csv', index=False)
    sales.to_csv('sales.csv', index=False)

    # returning DFs
    return items, stores, sales

# function combines 3 DFs from exercise
def df_combiner(items, stores, sales):
    """
    Combines 3 DFs into 1 DF.
    """
    # merging sales and stores DFs by matching store (sales) and store_id (stores)
    complete_df = sales.merge(stores, left_on='store', right_on='store_id')
    
    # adding items DF to complete_df by matching item (complete_df) with item_id (items)
    complete_df = complete_df.merge(items, left_on='item', right_on='item_id')
    
    # return merged DF
    return complete_df
    
############ GERMANY DATA FUNCTIONS ############

# function to acquire german power systems data
def get_power():
    """
    No argument needed. Run function to acquire german power systems data.
    """
    # saving data to variable
    power = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    # returning df
    return power

