import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

DB_FILE = "data/cashew.db"
CSV_FILE = "data/expense.csv"

# Columns matching DATA_SCHEMA.md
COLUMNS = ['date', 'categorie_flux', 'item', 'quantite', 'unite', 'prix_unitaire', 'montant_total_mga', 'fournisseur_client', 'portefeuille']

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initialise la base SQLite et synchronise depuis le CSV si existant."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table Wallets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            balance REAL DEFAULT 0
        )
    ''')
    
    # Ensure default 'Caisse' exists
    cursor.execute("INSERT OR IGNORE INTO wallets (name, balance) VALUES ('Caisse', 0)")
    
    # Table Transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            categorie_flux TEXT NOT NULL,
            item TEXT NOT NULL,
            quantite REAL,
            unite TEXT,
            prix_unitaire REAL,
            montant_total_mga REAL NOT NULL,
            fournisseur_client TEXT,
            portefeuille_id INTEGER,
            FOREIGN KEY (portefeuille_id) REFERENCES wallets(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # First time sync if CSV exists
    if os.path.exists(CSV_FILE):
        sync_from_csv()

def sync_from_csv():
    """Importe les données du CSV vers SQLite (Nettoyage préalable)."""
    if not os.path.exists(CSV_FILE):
        return
    
    df = pd.read_csv(CSV_FILE)
    conn = get_connection()
    
    # Simple sync strategy: Clear and reload (for MVP)
    # Better strategy would be Incremental Sync by ID/Hash
    conn.execute("DELETE FROM transactions")
    
    for _, row in df.iterrows():
        # Get wallet ID (default to 1 'Caisse' for now)
        wallet_name = row.get('portefeuille', 'Caisse')
        
        conn.execute('''
            INSERT INTO transactions (
                date, categorie_flux, item, quantite, unite, prix_unitaire, montant_total_mga, fournisseur_client, portefeuille_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            row['date'], row['categorie_flux'], row['item'], row['quantite'], 
            row['unite'], row['prix_unitaire'], row['montant_total_mga'], row['fournisseur_client']
        ))
    
    conn.commit()
    conn.close()

def get_summary_data(days=30):
    """Calcule le solde sur une fenêtre glissante (Témoin)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate date threshold
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Income (Miditra/Vente)
    cursor.execute("SELECT SUM(montant_total_mga) FROM transactions WHERE date >= ? AND categorie_flux IN ('Miditra', 'Vente')", (cutoff_date,))
    income = cursor.fetchone()[0] or 0
    
    # Expense (Fandaniana/Achat)
    cursor.execute("SELECT SUM(montant_total_mga) FROM transactions WHERE date >= ? AND categorie_flux IN ('Fandaniana', 'Achat')", (cutoff_date,))
    expense = cursor.fetchone()[0] or 0
    
    balance = income - expense
    conn.close()
    return income, expense, balance

def get_months_with_data():
    """Récupère la liste des mois (YYYY-MM) ayant des transactions."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT strftime('%Y-%m', date) as month FROM transactions ORDER BY month DESC")
    months = [row[0] for row in cursor.fetchall()]
    conn.close()
    return months

def get_transactions_by_month(month_str):
    """Récupère les transactions pour un mois donné (ex: '2026-04')."""
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM transactions WHERE date LIKE '{month_str}%' ORDER BY date DESC", conn)
    conn.close()
    return df

def save_entry(categorie_flux, item, quantite, unite, prix_unitaire, montant_total, fournisseur):
    """Sauvegarde dans SQLite ET Append dans CSV."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. SQLite
    conn = get_connection()
    conn.execute('''
        INSERT INTO transactions (
            date, categorie_flux, item, quantite, unite, prix_unitaire, montant_total_mga, fournisseur_client, portefeuille_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', (date_str, categorie_flux, item, quantite, unite, prix_unitaire, montant_total, fournisseur))
    conn.commit()
    conn.close()
    
    # 2. CSV Persistence
    new_row = [date_str, categorie_flux, item, quantite, unite, prix_unitaire, montant_total, fournisseur, 'Caisse']
    df_new = pd.DataFrame([new_row], columns=COLUMNS)
    df_new.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
def get_evolution_data(days=30):
    """Calcule l'évolution du solde cumulé sur les X derniers jours."""
    conn = get_connection()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    query = """
        SELECT date, 
               SUM(CASE WHEN categorie_flux IN ('Miditra', 'Vente') THEN montant_total_mga ELSE -montant_total_mga END) as daily_net 
        FROM transactions 
        WHERE date >= ? 
        GROUP BY date 
        ORDER BY date ASC
    """
    df = pd.read_sql_query(query, conn, params=(cutoff_date,))
    conn.close()
    
    if df.empty:
        return []
    
    # Calculate cumulative sum
    df['cumulative_balance'] = df['daily_net'].cumsum()
    return df[['date', 'cumulative_balance']].values.tolist()

def get_total_balance():
    """Calcule le solde total depuis le début."""
    conn = get_connection()
    cursor = conn.cursor()
    # Income (Miditra/Vente)
    cursor.execute("SELECT SUM(montant_total_mga) FROM transactions WHERE categorie_flux IN ('Miditra', 'Vente')")
    income = cursor.fetchone()[0] or 0
    # Expense (Fandaniana/Achat)
    cursor.execute("SELECT SUM(montant_total_mga) FROM transactions WHERE categorie_flux IN ('Fandaniana', 'Achat')")
    expense = cursor.fetchone()[0] or 0
    conn.close()
    return income - expense

def get_category_distribution(days=30):
    """Calcule la répartition par catégorie sur les X derniers jours."""
    conn = get_connection()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    query = """
        SELECT categorie_flux, SUM(montant_total_mga) as total 
        FROM transactions 
        WHERE date >= ? 
        GROUP BY categorie_flux
    """
    df = pd.read_sql_query(query, conn, params=(cutoff_date,))
    conn.close()
    return df.values.tolist()

def get_distribution_data(days=30):
    """Calcule la répartition des dépenses par item sur les X derniers jours."""
    conn = get_connection()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    query = """
        SELECT item, SUM(montant_total_mga) as total 
        FROM transactions 
        WHERE date >= ? AND categorie_flux IN ('Fandaniana', 'Achat') 
        GROUP BY item 
        ORDER BY total DESC 
        LIMIT 5
    """
    df = pd.read_sql_query(query, conn, params=(cutoff_date,))
    conn.close()
    return df.values.tolist()

def export_to_csv(filepath):
    """Exporte l'intégralité des transactions vers un fichier CSV externe."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    
    # Map back to CSV format if necessary (e.g. portefeuille name)
    # For now, we use the raw columns
    df.to_csv(filepath, index=False)

def import_from_csv(filepath):
    """Importe des transactions depuis un fichier externe (Ajout uniquement)."""
    if not os.path.exists(filepath):
        return False, "Fichier introuvable."
    
    try:
        new_df = pd.read_csv(filepath)
        
        # Validation minimale des colonnes requises
        required = ['date', 'categorie_flux', 'item', 'montant_total_mga']
        if not all(col in new_df.columns for col in required):
            return False, f"Format invalide. Colonnes requises : {', '.join(required)}"
        
        # Normalisation des colonnes avant l'import (Sécurité)
        for col in COLUMNS:
            if col not in new_df.columns:
                new_df[col] = None
        
        # Réorganiser les colonnes pour correspondre à COLUMNS
        new_df = new_df[COLUMNS]
        
        # Append to main CSV
        new_df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
        
        # Refresh SQLite
        sync_from_csv()
        return True, f"{len(new_df)} hara-mira (transactions) voadika."
    except Exception as e:
        import traceback
        print(traceback.format_exc()) # Log error to terminal
        return False, f"Fahadisoana: {str(e)}"
