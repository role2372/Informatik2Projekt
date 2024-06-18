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

def savings_algorithm(coords):
   
    distance_matrix = calculate_distance_matrix(coords)
    n = len(coords)
    savings = []
    

    for i in range(1, n):
        for j in range(i + 1, n):
            savings.append((distance_matrix[0][i] + distance_matrix[0][j] - distance_matrix[i][j], i, j))
    

    savings.sort(reverse=True, key=lambda x: x[0])
    
    routes = [[i] for i in range(n)]
    for saving, i, j in savings:
        route_i = route_j = None
        for route in routes:
            if i in route:
                route_i = route
            if j in route:
                route_j = route
        if route_i is not None and route_j is not None and route_i != route_j:
            routes.remove(route_i)
            routes.remove(route_j)
            routes.append(route_i + route_j)
    
    optimal_route = routes[0]
    return optimal_route
    

def visualize_map(coords, route=None, file_name="map.html"):
 
    m = folium.Map(location=[coords[0][0], coords[0][1]], zoom_start=12)

    for coord in coords:
        folium.Marker(location=[coord[0], coord[1]]).add_to(m)
    

    if route:
        route_coords = [coords[i] for i in route]
        route_coords.append(route_coords[0])  
        folium.PolyLine(route_coords, color='red', weight=10, opacity=1).add_to(m)
    
    m.save(file_name)
    print(f"Karte mit Route wurde erstellt und als '{file_name}' gespeichert.")

def user_choice_prompt():
    
    print("Aufruf zur Benutzereingabe:")
    print("1. Koordinaten aus CSV-Datei lesen")
    print("2. Koordinaten manuell eingeben")
    print("3. Koordinaten in Karte zeigen")
    print("4. Berechnen idealer Route")
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
        route = savings_algorithm(coordinates)
        visualize_map(coordinates, route, file_name="route_map.html")
        print("Ideale Route berechnet und auf Karte eingezeichnet")
   
    elif choice == '5':
        break
    
    elif choice == 'stop':
        break
    
    else:
        print("Ungültige Auswahl. Bitte geben sie eine gelistete Option.")