import pandas as pd
data_cleaned = pd.read_csv('data_cleaned.csv')

import pandas as pd
import numpy as np

# Calcul du seuil pour TransactionAmount
mean_amount = data_cleaned['TransactionAmount'].mean()
std_amount = data_cleaned['TransactionAmount'].std()
seuil = mean_amount + 2 * std_amount

# Calcul du seuil pour AccountBalance
seuil_bas = data_cleaned['AccountBalance'].quantile(0.01)

# Définition des heures inhabituelles
heures_inhabituelles = range(2, 3)

# Définition du seuil pour gap
seuil_gap = 5  # en minutes

def detect_fraud(row):
    if row['AnomalyScore'] > 0.98:
        return 1  # Fraude détectée au Noeud 1
    elif row['TransactionAmount'] > seuil:
        return 1  # Fraude détectée au Noeud 2
    elif row['SuspiciousFlag'] == 1 or row['AccountBalance'] < seuil_bas:
        return 1  # Fraude détectée au Noeud 3
    elif row['Hour'] in heures_inhabituelles:
        return 1  # Fraude détectée au Noeud 4
    elif row['Age'] < 25 and row['gap'] < seuil_gap:
        return 1  # Fraude détectée au Noeud 5
    else:
        return 0  # Pas de fraude

# Application de la fonction pour créer la colonne FraudIndicator
data_cleaned['FraudIndicator'] = data_cleaned.apply(detect_fraud, axis=1)

# Initialisation des compteurs
total_cas = len(data_cleaned)
compteurs = {}

# Noeud 1
condition1 = data_cleaned['AnomalyScore'] > 0.98
compteurs['Noeud1_Fraude'] = condition1.sum()
compteurs['Noeud1_NonFraude'] = (~condition1).sum()

# Noeud 2
condition2 = (data_cleaned['AnomalyScore'] <= 0.98) & (data_cleaned['TransactionAmount'] > seuil)
compteurs['Noeud2_Fraude'] = condition2.sum()
compteurs['Noeud2_NonFraude'] = ((data_cleaned['AnomalyScore'] <= 0.98) & (data_cleaned['TransactionAmount'] <= seuil)).sum()

# Noeud 3
condition3 = (data_cleaned['AnomalyScore'] <= 0.98) & (data_cleaned['TransactionAmount'] <= seuil) & ((data_cleaned['SuspiciousFlag'] == 1) | (data_cleaned['AccountBalance'] < seuil_bas))
compteurs['Noeud3_Fraude'] = condition3.sum()
compteurs['Noeud3_NonFraude'] = ((data_cleaned['AnomalyScore'] <= 0.98) & (data_cleaned['TransactionAmount'] <= seuil) & (data_cleaned['SuspiciousFlag'] != 1) & (data_cleaned['AccountBalance'] >= seuil_bas)).sum()

# Noeud 4
condition4 = (data_cleaned['Hour'].isin(heures_inhabituelles))
compteurs['Noeud4_Fraude'] = condition4.sum()
compteurs['Noeud4_NonFraude'] = (~data_cleaned['Hour'].isin(heures_inhabituelles)).sum()

# Noeud 5
condition5 = (data_cleaned['Age'] < 25) & (data_cleaned['gap'] < seuil_gap)
compteurs['Noeud5_Fraude'] = condition5.sum()
compteurs['Noeud5_NonFraude'] = (~((data_cleaned['Age'] < 25) & (data_cleaned['gap'] < seuil_gap))).sum()

from sklearn.tree import DecisionTreeClassifier, export_graphviz
import matplotlib.pyplot as plt
from sklearn import tree

# Préparation des données pour l'entraînement de l'arbre
features = ['AnomalyScore', 'TransactionAmount', 'SuspiciousFlag', 'AccountBalance', 'Hour', 'Age', 'gap']
X = data_cleaned[features]
y = data_cleaned['FraudIndicator']

# Save y as csv
y.to_csv('label.csv', index=False)

# Entraînement de l'arbre de décision
clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X, y)

# Visualisation de l'arbre
plt.figure(figsize=(20,10))
tree.plot_tree(clf, feature_names=features, class_names=['Non Fraude', 'Fraude'], filled=True)
plt.show()

