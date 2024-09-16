import os
import pandas as pd
import numpy as np

# Create folders if they don't exist
folders = ['Folder1', 'Folder2', 'Folder3', 'Folder4', 'Folder5']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Helper functions for data manipulation
def introduce_missing_values(df, fraction=0.01):
    """ Introduce NaN values randomly in the DataFrame """
    for col in df.columns:
        df.loc[df.sample(frac=fraction).index, col] = np.nan
    return df

def duplicate_rows(df, fraction=0.1):
    """ Duplicate random rows in the DataFrame """
    duplicates = df.sample(frac=fraction, replace=False)
    return pd.concat([df, duplicates], ignore_index=True)

def insert_outliers(df, column, fraction=0.001, scale=10):
    """ Insert outliers into a specific column of the DataFrame """
    indices = df.sample(frac=fraction).index
    max_val = df[column].max()
    df.loc[indices, column] = max_val * scale
    return df

# Generate Transaction Data
transaction_records = pd.DataFrame({
    'TransactionID': range(1, 1501),
    'Amount': np.random.uniform(10, 100, 1500),
    'CustomerID': np.random.randint(1001, 2001, 1500)
})
transaction_records = duplicate_rows(transaction_records, fraction=0.02)
transaction_records = introduce_missing_values(transaction_records, fraction=0.05)
transaction_records = insert_outliers(transaction_records, 'Amount', fraction=0.01, scale=20)

transaction_metadata = pd.DataFrame({
    'TransactionID': range(1, 1501),
    'Timestamp': pd.date_range('2022-01-01', periods=1500, freq='H'),
    'MerchantID': np.random.randint(2001, 3001, 1500)
})
transaction_metadata = introduce_missing_values(transaction_metadata, fraction=0.05)

# Generate Customer Profiles
customer_data = pd.DataFrame({
    'CustomerID': range(1001, 2501),
    'Name': ['Customer ' + str(i) for i in range(1001, 2501)],
    'Age': np.random.randint(18, 65, 1500),
    'Address': ['Address ' + str(i) for i in range(1001, 2501)]
})
customer_data = introduce_missing_values(customer_data, fraction=0.1)

account_activity = pd.DataFrame({
    'CustomerID': range(1001, 2501),
    'AccountBalance': np.random.uniform(1000, 10000, 1500),
    'LastLogin': pd.date_range('2022-01-01', periods=1500, freq='D')
})
account_activity = insert_outliers(account_activity, 'AccountBalance', fraction=0.02, scale=5)

# Generate Fraudulent Patterns
fraud_indicators = pd.DataFrame({
    'TransactionID': range(1, 1501),
    'FraudIndicator': np.random.choice([0, 1], 1500, p=[0.95, 0.05])
})

suspicious_activity = pd.DataFrame({
    'CustomerID': range(1001, 2501),
    'SuspiciousFlag': np.random.choice([0, 1], 1500, p=[0.98, 0.02])
})

# Generate Transaction Amounts
amount_data = pd.DataFrame({
    'TransactionID': range(1, 1501),
    'TransactionAmount': np.random.uniform(10, 100, 1500)
})
amount_data = introduce_missing_values(amount_data, fraction=0.05)
amount_data = insert_outliers(amount_data, 'TransactionAmount', fraction=0.01, scale=15)

anomaly_scores = pd.DataFrame({
    'TransactionID': range(1, 1501),
    'AnomalyScore': np.random.uniform(0, 1, 1500)
})

# Generate Merchant Information
merchant_data = pd.DataFrame({
    'MerchantID': range(2001, 3501),
    'MerchantName': ['Merchant ' + str(i) for i in range(2001, 3501)],
    'Location': ['Location ' + str(i) for i in range(2001, 3501)]
})

transaction_category_labels = pd.DataFrame({
    'TransactionID': range(1, 1501),
    'Category': np.random.choice(['Food', 'Retail', 'Travel', 'Online', 'Other'], 1500)
})

# Save the generated data into CSV files
transaction_records.to_csv('Folder1/transaction_records.csv', index=False)
transaction_metadata.to_csv('Folder1/transaction_metadata.csv', index=False)
customer_data.to_csv('Folder2/customer_data.csv', index=False)
account_activity.to_csv('Folder2/account_activity.csv', index=False)
fraud_indicators.to_csv('Folder3/fraud_indicators.csv', index=False)
suspicious_activity.to_csv('Folder3/suspicious_activity.csv', index=False)
amount_data.to_csv('Folder4/amount_data.csv', index=False)
anomaly_scores.to_csv('Folder4/anomaly_scores.csv', index=False)
merchant_data.to_csv('Folder5/merchant_data.csv', index=False)
transaction_category_labels.to_csv('Folder5/transaction_category_labels.csv', index=False)
