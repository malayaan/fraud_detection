import os
import pandas as pd
import numpy as np

# Définir la taille du jeu de données
DATASET_SIZE = 8000

# Créer les dossiers s'ils n'existent pas
folders = ['Folder1', 'Folder2', 'Folder3', 'Folder4', 'Folder5']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Fonctions auxiliaires pour la manipulation des données
def introduce_missing_values(df, fraction=0.01):
    """Introduit des valeurs manquantes (NaN) aléatoirement dans le DataFrame"""
    for col in df.columns:
        df.loc[df.sample(frac=fraction).index, col] = np.nan
    return df

def duplicate_rows(df, fraction=0.1):
    """Duplique des lignes aléatoirement dans le DataFrame"""
    duplicates = df.sample(frac=fraction, replace=False)
    return pd.concat([df, duplicates], ignore_index=True)

def insert_outliers(df, column, fraction=0.001, scale=10):
    """Insère des valeurs aberrantes dans une colonne spécifique du DataFrame"""
    indices = df.sample(frac=fraction).index
    max_val = df[column].max()
    df.loc[indices, column] = max_val * scale
    return df

# Génération des données de transaction
transaction_records = pd.DataFrame({
    'TransactionID': range(1, DATASET_SIZE + 1),
    'Amount': np.random.uniform(10, 100, DATASET_SIZE),
    'CustomerID': np.random.randint(1001, 1001 + DATASET_SIZE, DATASET_SIZE)
})
transaction_records = duplicate_rows(transaction_records, fraction=0.02)
transaction_records = introduce_missing_values(transaction_records, fraction=0.05)
transaction_records = insert_outliers(transaction_records, 'Amount', fraction=0.01, scale=20)

transaction_metadata = pd.DataFrame({
    'TransactionID': range(1, DATASET_SIZE + 1),
    'Timestamp': pd.date_range('2022-01-01', periods=DATASET_SIZE, freq='H'),
    'MerchantID': np.random.randint(2001, 2001 + DATASET_SIZE, DATASET_SIZE)
})
transaction_metadata = introduce_missing_values(transaction_metadata, fraction=0.05)

# Génération des profils clients
customer_data = pd.DataFrame({
    'CustomerID': range(1001, 1001 + DATASET_SIZE),
    'Name': ['Customer ' + str(i) for i in range(1001, 1001 + DATASET_SIZE)],
    'Age': np.random.randint(18, 65, DATASET_SIZE),
    'Address': ['Address ' + str(i) for i in range(1001, 1001 + DATASET_SIZE)]
})
customer_data = introduce_missing_values(customer_data, fraction=0.1)

account_activity = pd.DataFrame({
    'CustomerID': range(1001, 1001 + DATASET_SIZE),
    'AccountBalance': np.random.uniform(1000, 10000, DATASET_SIZE),
    'LastLogin': pd.date_range('2022-01-01', periods=DATASET_SIZE, freq='D')
})
account_activity = insert_outliers(account_activity, 'AccountBalance', fraction=0.02, scale=5)


suspicious_activity = pd.DataFrame({
    'CustomerID': range(1001, 1001 + DATASET_SIZE),
    'SuspiciousFlag': np.random.choice([0, 1], DATASET_SIZE, p=[0.98, 0.02])
})

# Génération des montants de transaction
amount_data = pd.DataFrame({
    'TransactionID': range(1, DATASET_SIZE + 1),
    'TransactionAmount': np.random.uniform(10, 100, DATASET_SIZE)
})
amount_data = introduce_missing_values(amount_data, fraction=0.05)
amount_data = insert_outliers(amount_data, 'TransactionAmount', fraction=0.01, scale=15)

anomaly_scores = pd.DataFrame({
    'TransactionID': range(1, DATASET_SIZE + 1),
    'AnomalyScore': np.random.uniform(0, 1, DATASET_SIZE)
})

# Génération des informations sur les marchands
merchant_data = pd.DataFrame({
    'MerchantID': range(2001, 2001 + DATASET_SIZE),
    'MerchantName': ['Merchant ' + str(i) for i in range(2001, 2001 + DATASET_SIZE)],
    'Location': ['Location ' + str(i) for i in range(2001, 2001 + DATASET_SIZE)]
})

transaction_category_labels = pd.DataFrame({
    'TransactionID': range(1, DATASET_SIZE + 1),
    'Category': np.random.choice(['Food', 'Retail', 'Travel', 'Online', 'Other'], DATASET_SIZE)
})

# Sauvegarde des données générées dans des fichiers CSV
transaction_records.to_csv('Folder1/transaction_records.csv', index=False)
transaction_metadata.to_csv('Folder1/transaction_metadata.csv', index=False)
customer_data.to_csv('Folder2/customer_data.csv', index=False)
account_activity.to_csv('Folder2/account_activity.csv', index=False)
suspicious_activity.to_csv('Folder3/suspicious_activity.csv', index=False)
amount_data.to_csv('Folder4/amount_data.csv', index=False)
anomaly_scores.to_csv('Folder4/anomaly_scores.csv', index=False)
merchant_data.to_csv('Folder5/merchant_data.csv', index=False)
transaction_category_labels.to_csv('Folder5/transaction_category_labels.csv', index=False)
