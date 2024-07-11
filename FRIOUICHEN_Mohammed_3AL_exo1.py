#FRIOUICHEN Mohammed 3AL
import pandas as pd

# Chargement du fichier CSV
filename = 'base-des-lieux-et-des-equipements-culturels.csv'
data = pd.read_csv(filename, delimiter=';', encoding='utf-8', dtype=str)

# Filtrage des lignes où le type d'équipement est "Cinéma"
cinemas = data[data['type_equipement_ou_lieu'] == 'Cinéma'].copy()  # Utilisation de .copy() pour éviter les avertissements

# Fonction pour convertir en numérique avec gestion des erreurs
def convert_to_numeric(value):
    try:
        # Tentative de conversion en float
        return float(value.replace(',', '.'))  # Remplacer ',' par '.' pour gérer les décimales
    except (TypeError, ValueError):
        return 0  # Retourner 0 si la conversion échoue

# Application de la conversion à la colonne nombre_fauteuils_de_cinema
cinemas.loc[:, 'nombre_fauteuils_de_cinema'] = cinemas['nombre_fauteuils_de_cinema'].apply(convert_to_numeric)

# Groupement et calcul du nombre total de fauteuils par département
cinemas_by_dept = cinemas.groupby(['n_departement', 'departement'])['nombre_fauteuils_de_cinema'].sum().reset_index()

# Affichage de l'en-tête
print("Département - Nombre de place de ciné")

# Affichage des résultats triés par numéro de département croissant
for index, row in cinemas_by_dept.iterrows():
    print(f"{row['n_departement']} ({row['departement']}) : {int(row['nombre_fauteuils_de_cinema'])}")
