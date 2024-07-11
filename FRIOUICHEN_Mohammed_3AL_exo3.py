#FRIOUICHEN Mohammed 3AL
import sys
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Vérification du nombre d'arguments
if len(sys.argv) != 2:
    print("Usage: python exo3.py <numéro_département>")
    sys.exit(1)

# Récupération du numéro de département depuis les arguments de la ligne de commande
num_departement = sys.argv[1]

# Chargement du fichier CSV BaLEC
filename = 'base-des-lieux-et-des-equipements-culturels.csv'
data = pd.read_csv(filename, delimiter=';', encoding='utf-8', dtype=str)

# Filtrage des données pour le département spécifié et les monuments
filtered_data = data[(data['n_departement'] == num_departement) & (data['type_equipement_ou_lieu'] == 'Monument')]

# Création de la carte folium centrée sur le département spécifié
if not filtered_data.empty:
    # Initialisation de la carte folium centrée sur le premier monument trouvé
    first_monument = filtered_data.iloc[0]
    map_center = [float(first_monument['coordonnees_gps_lat_lon'].split(',')[0]), float(first_monument['coordonnees_gps_lat_lon'].split(',')[1])]
    
    my_map = folium.Map(location=map_center, zoom_start=12)  # Zoom ajusté pour le département

    # Variables pour calculer les limites de la carte
    max_lat, min_lat = None, None
    max_lon, min_lon = None, None

    # Définition des couleurs pour chaque type de monument
    type_colors = {
        'Monument historique': 'blue',
        'Musée': 'green',
        'Édifice religieux': 'red',
        'Site archéologique': 'purple',
        'Parc et jardin': 'orange',
        'Château': 'darkred',
        'Théâtre': 'lightblue',
        'Site naturel': 'darkblue',
        'Cinéma': 'cadetblue',
        'Bibliothèque': 'pink',
        'Équipement sportif': 'lightgreen',
        'Autre lieu de culture': 'gray'
    }

    # Création d'un cluster de marqueurs
    marker_cluster = MarkerCluster().add_to(my_map)

    # Ajout des marqueurs pour chaque monument avec couleur et popup
    for index, monument in filtered_data.iterrows():
        name = monument['nom']
        lat_lon = monument['coordonnees_gps_lat_lon']
        monument_type = monument['label_et_appellation']
        
        if pd.notna(lat_lon):
            lat, lon = map(float, lat_lon.split(','))
            # Sélection de la couleur en fonction du type de monument
            if monument_type in type_colors:
                color = type_colors[monument_type]
            else:
                color = 'gray'  # Couleur par défaut pour les types non spécifiés

            folium.Marker([lat, lon], popup=name, icon=folium.Icon(color=color)).add_to(marker_cluster)

            # Mise à jour des limites de la carte
            if max_lat is None or lat > max_lat:
                max_lat = lat
            if min_lat is None or lat < min_lat:
                min_lat = lat
            if max_lon is None or lon > max_lon:
                max_lon = lon
            if min_lon is None or lon < min_lon:
                min_lon = lon

    # Ajustement de la carte aux limites des marqueurs
    if max_lat is not None and min_lat is not None and max_lon is not None and min_lon is not None:
        my_map.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

    # Ajout de la légende à la carte
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index:1000; font-size: 14px; background-color:white; padding: 10px;">
    <b>Légende</b><br>
    <i style="background:blue; padding: 0 5px;"></i> Monument historique<br>
    <i style="background:green; padding: 0 5px;"></i> Musée<br>
    <i style="background:red; padding: 0 5px;"></i> Édifice religieux<br>
    <i style="background:purple; padding: 0 5px;"></i> Site archéologique<br>
    <i style="background:orange; padding: 0 5px;"></i> Parc et jardin<br>
    <i style="background:darkred; padding: 0 5px;"></i> Château<br>
    <i style="background:lightblue; padding: 0 5px;"></i> Théâtre<br>
    <i style="background:darkblue; padding: 0 5px;"></i> Site naturel<br>
    <i style="background:cadetblue; padding: 0 5px;"></i> Cinéma<br>
    <i style="background:pink; padding: 0 5px;"></i> Bibliothèque<br>
    <i style="background:lightgreen; padding: 0 5px;"></i> Équipement sportif<br>
    <i style="background:gray; padding: 0 5px;"></i> Autre lieu de culture<br>
    </div>
    """
    my_map.get_root().html.add_child(folium.Element(legend_html))

    # Sauvegarde de la carte en fichier HTML
    html_file = f'departement_{num_departement}_map.html'
    my_map.save(html_file)
    
    print(f"Carte générée avec succès : {html_file}")
else:
    print(f"Aucun monument trouvé pour le département {num_departement}")
