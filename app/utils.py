from .models import *
import datetime
import time
import pandas as pd
from django.utils.timezone import make_aware

pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x))
pd.options.display.float_format = '{:,.2f}'.format

def get_old_metric(dateToday, **kwargs):
    # return row of data of a certain period in the past
    date_back = dateToday - datetime.timedelta(**kwargs)

    try:
        date_back_row = Data.objects.filter(timestamp__gte=date_back).first()
    except:
        date_back_row = None
    return date_back_row

def range_generator(lst):
    output = []
    for i in range(len(lst)-1):
        output.append(str(lst[i]) + "-" + str(lst[i+1]))
    return output

def Summary_table(file = "holders.csv",
                total_supply = 100000000,
                 bins = [0, 100, 1000, 10000, 30000, 100000, 300000, 1000000, 5000000]):
    # Load the csv file into a pandas dataframe
    df = pd.read_csv(file)
    total_supply = total_supply

    # Delete the PendingBalanceUpdate column
    df.drop(columns=["PendingBalanceUpdate"], inplace=True)

    # Create the categories
    labels = range_generator(bins)
    bins = [x * 1e18 for x in bins]

    df["category"] = pd.cut(df["Balance"], bins=bins, labels=labels)

    # Create the summary table
    summary_table = df.groupby("category").agg(
        number_of_addresses=("HolderAddress", "count"),
        sum_of_balances=("Balance", "sum"),
        average_balance=("Balance", "mean")
    ).reset_index()

    summary_table[["sum_of_balances", "average_balance"]] /= 1e18
    summary_table["percent_of_supply"] = summary_table["sum_of_balances"] / total_supply * 100

    return summary_table