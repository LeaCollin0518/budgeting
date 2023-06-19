#!/usr/bin/env python

import pandas as pd
import numpy as np

transactions = pd.read_csv('transactions.csv')

curr_year = 2023
curr_month = 5

# don't need to keep track of credit card payments
transactions = transactions.loc[(transactions.Category != 'Credit Card Payment')                                 & (transactions.Description != 'ALLY BANK $TRANSFER')]
non_misc_categories = ['Public Transportation', 'Groceries', 'Private Transportation', 'Eating Out', 'Food Delivery',                        'Clothing', 'Gym', 'Utilities', 'Going Out']

transactions['budget_category'] = transactions['Category']
transactions.loc[transactions.Category == 'Paycheck', 'budget_category'] = 'Income'
transactions.loc[transactions.Category == 'Interest Income', 'budget_category'] = 'Income'
transactions.loc[(transactions.Category == 'Transfer')     & (transactions['Account Name'] == 'Savings Account'), 'budget_category'] = 'Savings'
transactions.loc[(transactions.Category == 'Transfer')     & (transactions.Amount.isin([2500, 350])), 'budget_category'] = 'Rent'
transactions.loc[transactions.Category.isin(['Ride Share', 'Rental Car & Taxi']), 'budget_category'] = 'Private Transportation'
transactions.loc[transactions.Category == 'Alcohol & Bars', 'budget_category'] = 'Going Out'
transactions.loc[transactions.Category.isin(['Fast Food', 'Restaurants', 'Food & Dining', 'Coffee Shops']),                  'budget_category'] = 'Eating Out'
transactions.loc[~transactions.budget_category.isin(non_misc_categories), 'budget_category'] = 'Misc Expenses'

month_df = transactions.loc[(pd.DatetimeIndex(transactions['Date']).year == curr_year) \
    & (pd.DatetimeIndex(transactions['Date']).month == curr_month)]


summary_spending = month_df.groupby(by = 'budget_category').agg({'Amount' : 'sum'}).reset_index()
print(summary_spending)