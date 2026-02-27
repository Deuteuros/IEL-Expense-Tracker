import pandas as pd
import os
from datetime import datetime

DATA_FILE = "expense.csv"
COLUMNS = ['date', 'categorie_flux', 'item', 'quantite', 'unite', 'prix_unitaire_mga', 'montant_total_mga', 'fournisseur_client']

def init_db():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)

def get_df():
    if not os.path.exists(DATA_FILE):
        init_db()
    return pd.read_csv(DATA_FILE)

def get_summary_data():
    df = get_df()
    # Assuming 'Miditra' is income and everything else is expense or based on categorie_flux
    income = df[df['categorie_flux'].isin(['Income', 'Miditra'])]['montant_total_mga'].sum()
    expense = df[df['categorie_flux'].isin(['Expense', 'Fandaniana'])]['montant_total_mga'].sum()
    balance = income - expense
    return income, expense, balance

def save_entry(categorie_flux, item, quantite, unite, prix_unitaire, montant_total, fournisseur):
    new_data = [[
        datetime.now().strftime("%Y-%m-%d"),
        categorie_flux,
        item,
        quantite,
        unite,
        prix_unitaire,
        montant_total,
        fournisseur
    ]]
    new_df = pd.DataFrame(new_data, columns=COLUMNS)
    new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)

def delete_entries_by_index(indices):
    df = get_df()
    df = df.drop(indices)
    df.to_csv(DATA_FILE, index=False)
