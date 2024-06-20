# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 20:59:44 2024

@author: ACER
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:25:40 2024

@author: ACER
"""

import matplotlib.pyplot as plt
import pandas as pd
import folium
from geopy.distance import geodesic
import os

def read_coordinates_from_csv(file):
    df = pd.read_csv(file, sep=',', header=0)
    coordinates = list(zip(df['Longitude'], df['Latitude']))    
    return coordinates

def input_coordinates():
    coordinates = []
    while True:
        x_input = input("Geben Sie die x Koordinate (oder Geben sie 'stop' zum abbrechen):")
        if x_input.lower() == 'stop':
            break
        
        y_input = input("Geben Sie die y Koordinate (oder Geben sie 'stop' zum abbrechen):")
        if y_input.lower() == 'stop':
            break
        
        try:
            x = float(x_input)
            y = float(y_input)
            
            if x < -180 or x > 180 or y < -90 or y > 90:
                print("Ungültige Koordinaten")
                continue
                
            coordinates.append((x, y))
             
        except ValueError:
           print("Ungültige Eingabe. Bitte geben Sie einen numerischen Wert oder 'stop' zum abbrechen")
    
    return coordinates

def plot_coordinates(coordinates):
    x_values = [coord[0] for coord in coordinates]
    y_values = [coord[1] for coord in coordinates]
    
    plt.scatter(x_values, y_values)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Visualization of Coordinates')
    plt.show()

def read_legend():
    try:
        lieferorte_dok = pd.read_csv('lieferorte.csv', sep=',')
        return lieferorte_dok
    except FileNotFoundError:
        print("Die Datei 'lieferorte.csv' wurde nicht gefunden.")
        return pd.DataFrame()

def create_map():
    lieferorte_dok = read_legend()
    if not lieferorte_dok.empty:
        coordinates = list(zip(lieferorte_dok['Longitude'], lieferorte_dok['Latitude']))
        plot_coordinates(coordinates)
        map_center = [lieferorte_dok['Latitude'].mean(), lieferorte_dok['Longitude'].mean()]
        map = folium.Map(location=map_center, zoom_start=12)
        
        for coord in coordinates:
            folium.Marker(location=[coord[0], coord[1]]).add_to(map)  
   
        map.save('mapp.html')
        print("Karte wurde erstellt und als 'mapp.html' gespeichert.")
    else:
        print("Keine Koordinaten zum Zeigen vorhanden.")

def calculate_distance_matrix(coords):
    n = len(coords)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = geodesic(coords[i], coords[j]).kilometers
    return distance_matrix
    print("distance", distance_matrix)



def nearest_neighbor_algorithm(coords):
    # Number of places to visit
    num_places = len(coords)
    
    # List to keep track of the places we need to visit
    unvisited = list(range(1, num_places))
    
    # Start at the first place (index 0)
    route = [0]
    
    while unvisited:
        # Last place we visited
        last_place = route[-1]
        
        # Find the closest place we haven't visited yet
        next_place = unvisited[0]
        min_distance = geodesic(coords[last_place], coords[next_place]).kilometers
        
        for place in unvisited[1:]:
            distance = geodesic(coords[last_place], coords[place]).kilometers
            if distance < min_distance:
                next_place = place
                min_distance = distance
        
        # Add the closest place to the route and remove it from the unvisited list
        route.append(next_place)
        unvisited.remove(next_place)
    
    # Return to the starting place
    route.append(0)
    
    return route
  


def visualize_map(coords, route=None, file_name="map.html"):
    m = folium.Map(location=[coords[0][0], coords[0][1]], zoom_start=12)

    for coord in coords:
        folium.Marker(location=[coord[0], coord[1]]).add_to(m)
    
    if route:
        route_coords = [(coords[i][0], coords[i][1]) for i in route]
        folium.PolyLine(route_coords, color='red', weight=8, opacity=1).add_to(m)
    
    m.save(file_name)
    print(f"Karte mit Route wurde erstellt und als '{file_name}' gespeichert.")

def user_choice_prompt():
    print("Aufruf zur Benutzereingabe:")
    print("1. Koordinaten aus CSV-Datei lesen")
    print("2. Koordinaten manuell eingeben")
    print("3. Koordinaten in Karte zeigen")
    print("4. Berechnen idealer Route (Nächster Nachbar Algorithmus)")
    print("5. Vorgang abbrechen")
    choice = input("Bitte geben sie ihre Auswahl (1, 2, 3, 4 oder 5):")
    return choice

while True:
    choice = user_choice_prompt()
    
    if choice == '1':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        df = pd.read_csv(file, sep=',')
        df.columns = df.columns.str.strip()
        print(df.to_string(index=False))
        plot_coordinates(coordinates)
        print("Koordinaten aus CSV-Datei gelesen")
    
    elif choice == '2':
        coordinates = input_coordinates()
        print("Koordinaten eingegeben:", coordinates)
        plot_coordinates(coordinates)
        print("Koordinaten eingefügt")
        
    elif choice == '3':
        create_map()
        print("Koordinaten auf Karte eingezeichnet")
    
    elif choice == '4':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        print(coordinates)
        route = nearest_neighbor_algorithm(coordinates)
        visualize_map(coordinates, route, file_name="route_map.html")
        print("Ideale Route berechnet und auf Karte eingezeichnet")
        print("ideale Route:", route)
   
    elif choice == '5':
        break
    
    elif choice == 'stop':
        break
    
    else:
        print("Ungültige Auswahl. Bitte geben sie eine gelistete Option.")  
