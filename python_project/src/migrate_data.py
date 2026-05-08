import pandas as pd
import os

OLD_FILE = "expenses.csv"
NEW_FILE = "expense.csv"
COLUMNS = ['date', 'categorie_flux', 'item', 'quantite', 'unite', 'prix_unitaire_mga', 'montant_total_mga', 'fournisseur_client']

def migrate():
    if not os.path.exists(OLD_FILE):
        print(f"Error: {OLD_FILE} not found.")
        return

    print(f"Reading {OLD_FILE}...")
    try:
        old_df = pd.read_csv(OLD_FILE)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print("Mapping columns...")
    # Map old columns to new columns
    # Old: Date,Type,Category,Amount
    # New: date,categorie_flux,item,quantite,unite,prix_unitaire_mga,montant_total_mga,fournisseur_client
    
    new_data = []
    for _, row in old_df.iterrows():
        new_data.append({
            'date': row['Date'],
            'categorie_flux': row['Type'],
            'item': row['Category'],
            'quantite': 1,
            'unite': 'pcs',
            'prix_unitaire_mga': row['Amount'],
            'montant_total_mga': row['Amount'],
            'fournisseur_client': 'Migrated'
        })
    
    new_df = pd.DataFrame(new_data, columns=COLUMNS)
    
    if os.path.exists(NEW_FILE):
        print(f"Reading existing {NEW_FILE} to append...")
        existing_df = pd.read_csv(NEW_FILE)
        # Avoid duplicates if migration is run twice by checking for specific markers?
        # For simplicity, we just append or overwrite. 
        # Requirement #3 says evolution of schema, so we should probably preserve what's in expense.csv if any.
        final_df = pd.concat([existing_df, new_df]).drop_duplicates().reset_index(drop=True)
    else:
        final_df = new_df

    print(f"Saving to {NEW_FILE}...")
    final_df.to_csv(NEW_FILE, index=False)
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
