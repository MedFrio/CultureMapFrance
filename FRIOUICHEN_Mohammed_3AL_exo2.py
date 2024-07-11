#FRIOUICHEN Mohammed 3AL
import pandas as pd
import matplotlib.pyplot as plt

# Chargement du fichier CSV
filename = 'base-des-lieux-et-des-equipements-culturels.csv'
data = pd.read_csv(filename, delimiter=';', encoding='utf-8', dtype=str)

# Compter le nombre de BaLEC par région
region_counts = data['region'].value_counts()

# Préparer les données pour le graphique
regions = region_counts.index
counts = region_counts.values

# Création du graphique à barres
plt.figure(figsize=(10, 6))
plt.bar(regions, counts, color='skyblue')

# Ajouter des titres et des étiquettes
plt.title('Nombre de BaLEC par région')
plt.xlabel('Région')
plt.ylabel('Nombre de BaLEC')
plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes pour une meilleure lisibilité

# Affichage du graphique
plt.tight_layout()
plt.show()
