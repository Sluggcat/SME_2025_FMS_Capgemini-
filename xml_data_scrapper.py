"""
data_scrapper.py

    M2 SME
        Mohamed ELKOUMI
        Erwann JAMIN
        Christopher RAKOTONDRATSIMA
        Reda TAIBI
        Imane ZAHIRI
"""
from bs4 import BeautifulSoup
import json

def get_station_id(file_path):
    """
    Cette fonction analyse le fichier XMI donné pour trouver la classe 'Station'
    et renvoie son identifiant 'xmi:id' ainsi que l'élément station.
    
    Paramètres:
    - file_path (str): Le chemin vers le fichier XMI
    
    Remarque:
    Cette fonction peut être adaptée pour trouver n'importe quelle classe
    Changer 'Station' par le nom de la nouvelle classe cible (name='Station' ligne 28)
    Adapter les print.
    
    Retourne:
    - str: Le 'xmi:id' de la classe 'station' si trouvé, ou None si non trouvé
    - Tag: L'élément XML représentant la classe 'station'
    """
    # Charger et analyser le fichier XMI
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Analyser le fichier avec BeautifulSoup
    soup = BeautifulSoup(content, 'xml')

    # Trouver la classe avec name="Station"
    station = soup.find('packagedElement', {'xmi:type': 'uml:Class', 'name': ['Station']})

    # Retourner le 'xmi:id' et l'élément station si une classe station est trouvée
    if station:
        return station['xmi:id'], station
    else:
        return None, None

def get_station_attributes(station_element):
    """
    Cette fonction extrait tous les identifiants d'attributs de la classe station.
    
    Paramètres:
    - station_element (Tag): L'élément XML représentant la classe station
    
    Retourne:
    - Liste des identifiants d'attributs
    """
    # Trouver tous les attributs possédés au sein de la classe station
    attributes = station_element.find_all('ownedAttribute')
    
    # Extraire le 'xmi:id' de chaque attribut
    attribute_ids = [attribute['xmi:id'] for attribute in attributes]
    
    return attribute_ids

def get_station_instances(soup, station_classifier_id):
    """
    Cette fonction récupère toutes les instances de la classe 'Station' à partir du fichier XMI.
    
    Paramètres:
    - soup (BeautifulSoup): Contenu XML analysé
    - station_classifier_id (str): Identifiant du classificateur pour la classe 'Station'
    
    Retourne:
    - Liste des instances de station (éléments packagedElement)
    """
    return soup.find_all('packagedElement', {'xmi:type': 'uml:InstanceSpecification', 'classifier': station_classifier_id})

def print_station_details(station_instances, soup):
    """
    Cette fonction imprime le nom, les attributs et leurs valeurs pour chaque instance de station
    et retourne un dictionnaire structuré pour l'exportation JSON.
    
    Paramètres:
    - station_instances (List[Tag]): Les éléments XML représentant les instances de station
    - soup (BeautifulSoup): Contenu XML analysé
    
    Retourne:
    - Liste de dictionnaires contenant les détails de la station
    """
    station_details = []
    
    for station_instance in station_instances:
        station_name = station_instance['name']
        station_data = {'station_name': station_name, 'attributes': []}
        
        # Obtenir tous les slots (attributs)
        slots = station_instance.find_all('slot')
        
        for slot in slots:
            defining_feature_id = slot['definingFeature']
            
            # Trouver l'élément d'attribut correspondant dans la classe 'Station' par ID
            attribute = soup.find('ownedAttribute', {'xmi:id': defining_feature_id})
            
            if attribute:
                attribute_name = attribute['name']
                # Obtenir la valeur à partir du slot
                value = slot.find('value')
                attribute_value = value['symbol'] if value else 'Aucune valeur'
                
                # Ajouter les détails de l'attribut aux données de la station
                station_data['attributes'].append({
                    'attribute_name': attribute_name,
                    'attribute_value': attribute_value
                })
        
        station_details.append(station_data)
        print(f"\nStation: {station_name}")
        for attr in station_data['attributes']:
            print(f"  - {attr['attribute_name']} : {attr['attribute_value']}")
    
    return station_details

def save_station_details_to_json(station_details, output_file):
    """
    Enregistre les détails des stations trouvées dans un fichier JSON.
    
    Paramètres:
    - station_details (List[Dict]): La liste de dictionnaires contenant les détails de la station
    - output_file (str): Le chemin vers le fichier JSON de sortie
    """
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(station_details, json_file, ensure_ascii=False, indent=4)
    print(f"Détails de la station enregistrés dans {output_file}")

def main():
    """
    Fonction principale 
    """
    # Chemin vers votre fichier XMI
    file_path = 'UPS1.xmi'
    output_file = 'station_details.json'
    
    # Étape 1: Obtenir l'ID de la station et l'élément station
    station_id, station_element = get_station_id(file_path)
            
    if not station_id:
        print("Aucune classe 'station' trouvée dans le fichier.")
    else:
        print(f"L'ID de la classe 'station' est:\n  {station_id}\n")
        
        # Étape 2: Obtenir et imprimer tous les ID d'attributs de la classe station
        attribute_ids = get_station_attributes(station_element)
        
        if not attribute_ids:
            print("Aucun attribut trouvé pour la classe 'station'.")
        else:
            print("  ID des attributs de la classe 'station' :")
            for attr_id in attribute_ids:
                print(f"    {attr_id}")
            
            # Étape 3: Analyser le fichier à nouveau pour obtenir les instances
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'xml')
                
            # Étape 4: Obtenir toutes les instances de station
            station_instances = get_station_instances(soup, station_id)
            
            if not station_instances:
                print("Aucune instance de la classe 'Station' trouvée dans le fichier.")
            else:
                # Étape 5: Imprimer et enregistrer les détails de la station
                station_details = print_station_details(station_instances, soup)
                save_station_details_to_json(station_details, output_file)
                
# Point d'entrée du script
if __name__ == '__main__':
    main()
