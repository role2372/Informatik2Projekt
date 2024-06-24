# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:47:46 2024

@author: ACER
"""

import matplotlib.pyplot as plt
import pandas as pd
import folium
from geopy.distance import geodesic

def read_coordinates_from_csv(file):
    try:
        df = pd.read_csv(file, sep=',', header=0)
        coordinates = list(zip(df['Longitude'], df['Latitude']))
        return coordinates
    except FileNotFoundError:
        print(f"Die Datei '{file}' wurde nicht gefunden.")
        return []

def input_coordinates():
    coordinates = []
    while True:
        print("\nAktuelle Koordinatenliste:")
        for i in range(len(coordinates)):
            x, y = coordinates[i]
            print(f"{i}: ({x}, {y})")
        
        
        print("\nOptionen:")
        print("1. Neue Koordinaten hinzufuegen")
        print("2. Vorhandene Koordinaten bearbeiten")
        print("3. Vorhandene Koordinaten loeschen")
        print("4. Eingabe beenden")
        
        option = input("Waehlen Sie eine Option (1-4): ")
        
        if option == '1':
            while True:
                x_input = input("Geben Sie die x Koordinate (oder 'ok' zum Beenden): ")
                if x_input.lower() == 'ok':
                    break
                y_input = input("Geben Sie die y Koordinate (oder 'ok' zum Beenden): ")
                if y_input.lower() == 'ok':
                    break
                
                try:
                    x = float(x_input)
                    y = float(y_input)
                    
                    if x < -180 or x > 180 or y < -90 or y > 90:
                        print("Ungültige Koordinaten")
                        continue
                        
                    coordinates.append((y, x))
                 
                except ValueError:
                   print("Ungültige Eingabe. Bitte geben Sie einen numerischen Wert ein.")
         
        elif option == '2':
            idx = input("Geben Sie den Index der zu bearbeitenden Koordinate ein: ")
            try:
                idx = int(idx)
                if 0 <= idx < len(coordinates):
                    x_input = input(f"Neue x Koordinate fuer Index {idx} (aktuell {coordinates[idx][0]}): ")
                    y_input = input(f"Neue y Koordinate fuer Index {idx} (aktuell {coordinates[idx][1]}): ")
                    try:
                        x = float(x_input)
                        y = float(y_input)
                        
                        if x < -180 or x > 180 or y < -90 or y > 90:
                            print("Ungültige Koordinaten")
                            continue
                        
                        coordinates[idx] = (float(y_input), float(x_input))
                        print(f"Koordinate bei Index {idx} zu ({x}, {y}) geändert.")
                     
                    except ValueError:
                       print("Ungültige Eingabe. Bitte geben Sie einen numerischen Wert ein.")
                       
                else:
                    print ("Ungültiger Index.")
                    
            except ValueError:
                print("Ungültiger Index. Bitte geben Sie eine Zahl ein.")
        
        elif option == '3':
            idx = input("Geben Sie den Index der zu löschenden Koordinate ein: ")
            try:
                idx = int(idx)
                if 0 <= idx < len(coordinates):
                    del coordinates[idx]
                else:
                    print("Ungültiger Index.")
                    
            except ValueError:
                 print("Ungültiger Index. Bitte geben Sie eine Zahl ein.")
                 
        elif option == '4':
            print("Eingabe beendet.")
            break
        
        else:
            print("Ungültige Option. Bitte wählen Sie eine Option zwischen 1 und 4.")
    
    if coordinates:
        plot_coordinates(coordinates)
        create_map(coordinates) # create_map mit der Koordinatenliste aufrufen
            
            
    return coordinates

def create_map(csv_coordinates=None, manual_coordinates=None):
   
    if csv_coordinates is None:
        csv_coordinates = read_coordinates_from_csv('lieferorte.csv')
        if not csv_coordinates:
            print("Keine Koordinaten zum Zeigen vorhanden.")
            return
    
    
    if manual_coordinates:
        all_coordinates = csv_coordinates + manual_coordinates
    else:
        all_coordinates = csv_coordinates
    
    plot_coordinates(all_coordinates)
    
    visualize_map(all_coordinates, file_name="map_with_manual.html")
    print("Karte wurde erstellt und als 'map_with_manual.html' gespeichert.")
    
    map_center = [sum(coord[0] for coord in all_coordinates) / len(all_coordinates),
                  sum(coord[1] for coord in all_coordinates) / len(all_coordinates)]
    
    
                  
   
    m = folium.Map(location=map_center, zoom_start=8)
    
    
    for coord in all_coordinates:
        folium.Marker(location=[coord[0], coord[1]]).add_to(m)  

    # Save the map as 'mapp.html'
    m.save('mapp.html')
    print("Karte wurde erstellt und als 'mapp.html' gespeichert.")

def plot_coordinates(coordinates):
    x_values = [coord[0] for coord in coordinates]
    y_values = [coord[1] for coord in coordinates]
    
    plt.scatter(x_values, y_values)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Visualization of Coordinates')
    plt.show()
    
    


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
        folium.Marker(location=[coord[1], coord[0]]).add_to(m)
    
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
        create_map(manual_coordinates=coordinates)
        print("Koordinaten eingefügt")
        
    elif choice == '3':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        if coordinates:
            create_map(coordinates)
            print("Koordinaten auf Karte eingezeichnet")
        else:
            print("Die CSV-Datei enthaelt keine Koordinaten.")
    
    elif choice == '4':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        print(coordinates)
        if coordinates:
            route = nearest_neighbor_algorithm(coordinates)
            visualize_map(coordinates, route, file_name="route_map.html")
            print("Ideale Route berechnet und auf Karte eingezeichnet")
            print("ideale Route:", route)
        else:
            print("Die CSV Datei enthaelt keine Koordinaten.")
   
    elif choice == '5' or choice.lower()=='stop':
        break
    
    #elif choice == 'stop':
        #break
    
    else:
        print("Ungültige Auswahl. Bitte geben sie eine gelistete Option.")  

