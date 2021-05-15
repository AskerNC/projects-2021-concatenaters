from IPython.display import display
import ipywidgets as widgets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def eurostat_to_df(dataset_id, params, client):
    """ imports a dataset from eurostat as a dataframe using the eurostatapiclient
        prints dataset title and displays dataframe head

        Args:
            dataset_id (str):   dataset code
            params (list):      list of tuples containing strings of parameter and value pairs
            client:             an initialized client from EurostatAPIClient
            
            
        Returns:
            df (pd.DataFrame):  pandas dataframe
    """

    # a. fetching dataset
    dataset = client.get_dataset(dataset_id, params=params)
    print(f'The dataset title is:\n{dataset.label}')

    # b. converting to dataframe
    df = dataset.to_dataframe()

    # c. display head
    display(df.head())

    return df

def clean_eurostat_df(df, drop_col, rename_val):
    """ cleans up an imported eurostat dataframe by removing columns defined by drop_col
        and rename the 'values' column to rename_val
        displays dataframe head to inspect result

        Args:
            df (pd.DataFrame):  pandas dataframe with a dataset from eurostat
            drop_col (list):    list withs strings of column names to be removed
            rename_val (str):   string with new name for 'values' column
    """

    # a. removing columns
    df.drop(drop_col,axis=1,inplace=True)

    # b. renaming values column
    df.rename(columns = {'values':rename_val},inplace=True)

    # c. display head
    display(df.head())

def code_to_name(code,code_dict):
    """ returns a country name if the given dictionary contains a code for it
        if the code is not in the dictionary it will return an empty string

        Args:
            code (str):         country code
            code_dict (dict):   dictionary with code as key and name as value

        Returns:
            geo_name (str):     name of country
    """

    geo_name = ''

    if code in code_dict:
        geo_name = code_dict[code]

    return geo_name

def merge_dfs(*dfs,on,how):
    """ iterates through the given dataframes and merges them together
        on the given variables ('on') and method ('how')
        also displays the head of returned dataframe

        Args:
            *dfs (pd.DataFrame):    dataframes to be iterated over
            on (list):              list of variables in string format to merge on
            how (str):           merger method (outer, inner, left)
    """

    first=True
    for df in dfs:

        # a. the first dataframe is saved as the full merger
        if first:
            full = df
            first = False

        # b. all following dataframes are merged with full
        else:
            full = full.merge(df,on=on,how=how)
    # c. display the head of the merged dataframe
    display(full.head())

    return full

def plot_gdp_pas_cap(df, geo_name):
    """ plots a figure of gdp_cap and pas_cap from the dataframe 'df'

        Args:
            geo_name (str):     country name
            df (pd.Dataframe):  dataframe containing variables gdp_cap and pas_cap
            
    """

    fig, ax1 = plt.subplots(figsize=(10,6))

    ax2 = ax1.twinx() # second axis on the right that shares the same x-axis

    # a. data for the axes
    x = df.time[df.geo_name == geo_name]
    y1 = df.gdp_cap[df.geo_name == geo_name]
    y2 = df.pas_cap[df.geo_name == geo_name]

    # b. plots
    color1 = 'darkblue'
    ax1.plot(x, y1, color=color1)
    
    color2 = 'darkred'
    ax2.plot(x, y2, color=color2)

    # b. x-axis 
    ax1.set_xlabel('time (year)')
    ax1.tick_params(axis='x',labelrotation=45)
    ax1.set_xticks(ax1.get_xticks()[::2]) # every 2nd year as tick

    # c. left axis
    ax1.set_ylabel('GDP per capita', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    # d. right axis
    ax2.set_ylabel('Air transport passengers per capita', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.show()

<<<<<<< HEAD
def co_var(x, y):
    """ returns the covariance between two pd.Series
        
        Args:
            x (pd.Series):  x values
            y (pd.Series):  y values

        Returns:
            cov (float):    covariance
    """

    tup = ()

    # a. product of x and y differences from their respective means are added to a tuple
    for i in x.index:
        tup += ((x[i] - x.mean())*(y[i] - y.mean()),)

    # b. take the mean
    cov = np.sum(tup)/(len(x)-1)

    return cov

=======
>>>>>>> 60c6d0f58d00db2611918f8805730c294a14fd52
def add_pct_col(df,group,col):
    """ from a column already in the dataframe the function adds
        a percentual growth column within a group
    
        Args:
            df (pd.DataFrame):  dataframe
            group (str):        group variable name
            col (str):          target variable (adds the growth in this)

    """

<<<<<<< HEAD
    df[col + '_pct'] = df.groupby(group)[col].pct_change(fill_method=None) * 100
=======
    df[col + '_pct'] = df.groupby(group)[col].pct_change(fill_method=None) * 100 # fill method sets NaN, when no previous year data
>>>>>>> 60c6d0f58d00db2611918f8805730c294a14fd52
