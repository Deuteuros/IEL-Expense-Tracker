import pandas as pd
import os
from datetime import datetime

DATA_FILE = "expenses.csv"

def init_db():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount'])
        df.to_csv(DATA_FILE, index=False)

def get_df():
    return pd.read_csv(DATA_FILE)

def get_summary_data():
    df = get_df()
    income = df[df['Type'].isin(['Income', 'Miditra'])]['Amount'].sum()
    expense = df[df['Type'].isin(['Expense', 'Fandaniana'])]['Amount'].sum()
    balance = income - expense
    return income, expense, balance

def save_entry(type_val, category, amount):
    new_data = [[datetime.now().strftime("%Y-%m-%d"), type_val, category, amount]]
    new_df = pd.DataFrame(new_data, columns=['Date', 'Type', 'Category', 'Amount'])
    new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)

def delete_entries_by_index(indices):
    df = get_df()
    df = df.drop(indices)
    df.to_csv(DATA_FILE, index=False)
