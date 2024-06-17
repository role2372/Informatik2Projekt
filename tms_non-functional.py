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
    """
    Reads coordinates from a CSV file.
    
    Parameters:
    file (str): The path to the CSV file.
    
    Returns:
    list: A list of tuples containing coordinates.
    """
    df = pd.read_csv(file, sep=',', header=0)
    coordinates = list(zip(df['Longitude'], df['Latitude']))    
    return coordinates

def input_coordinates():
    """
    Prompts the user to input coordinates manually.
    
    Returns:
    list: A list of tuples containing coordinates.
    """
    coordinates = []
    while True:
        x_input = input("Enter x coordinate (or type 'stop' to finish):")
        if x_input.lower() == 'stop':
            break
        
        y_input = input("Enter y coordinate (or type 'stop' to finish):")
        if y_input.lower() == 'stop':
            break
        
        try:
            x = float(x_input)
            y = float(y_input)
            
            if x < -180 or x > 180 or y < -90 or y > 90:
                print("Invalid coordinates.")
                continue
                
            coordinates.append((x, y))
             
        except ValueError:
           print("Invalid input. Please enter numerical values or type 'stop' to finish")
    
    return coordinates

def plot_coordinates(coordinates):
    """
    Plots the coordinates on a scatter plot.
    
    Parameters:
    coordinates (list): A list of tuples containing coordinates.
    """
    x_values = [coord[0] for coord in coordinates]
    y_values = [coord[1] for coord in coordinates]
    
    plt.scatter(x_values, y_values)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Visualization of Coordinates')
    plt.show()

def read_legend():
    """
    Reads coordinates from the 'lieferorte.csv' file.
    
    Returns:
    DataFrame: A pandas DataFrame containing the coordinates.
    """
    try:
        lieferorte_dok = pd.read_csv('lieferorte.csv', sep=',')
        return lieferorte_dok
    except FileNotFoundError:
        print("The file 'lieferorte.csv' was not found.")
        return pd.DataFrame()

def create_map():
    """
    Creates a folium map with coordinates from the 'lieferorte.csv' file.
    """
    lieferorte_dok = read_legend()
    if not lieferorte_dok.empty:
        coordinates = list(zip(lieferorte_dok['Longitude'], lieferorte_dok['Latitude']))
        plot_coordinates(coordinates)
        
        # folium map centered around the mean of the coordinates
        map_center = [lieferorte_dok['Latitude'].mean(), lieferorte_dok['Longitude'].mean()]
        map = folium.Map(location=map_center, zoom_start=12)
        
        for coord in coordinates:
            folium.Marker(location=[coord[1], coord[0]]).add_to(map)  # Note: folium uses (lat, lon)
        
        # Save the map to an HTML file
        map.save('mapp.html')
        print("Map has been created and saved as 'mapp.html'.")
    else:
        print("No coordinates to display.")

def calculate_distance_matrix(coords):
    """
    Calculates the distance matrix for given coordinates.
    
    Parameters:
    coords (list): A list of tuples containing coordinates.
    
    Returns:
    list: A 2D list representing the distance matrix.
    """
    n = len(coords)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = geodesic(coords[i], coords[j]).kilometers
    return distance_matrix

def savings_algorithm(coords):
    """
    Calculates the ideal route using the Savings Algorithm.
    
    Parameters:
    coords (list): A list of tuples containing coordinates.
    
    Returns:
    list: A list representing the order of coordinates in the optimal route.
    """
    distance_matrix = calculate_distance_matrix(coords)
    n = len(coords)
    savings = []
    
    # Calculate savings
    for i in range(1, n):
        for j in range(i + 1, n):
            savings.append((distance_matrix[0][i] + distance_matrix[0][j] - distance_matrix[i][j], i, j))
    
    # Sort savings in descending order
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
    """
    Visualizes the coordinates on a folium map and saves it to an HTML file.
    
    Parameters:
    coords (list): A list of tuples containing coordinates.
    route (list): A list representing the order of coordinates in the optimal route.
    file_name (str): The name of the HTML file to save the map.
    """
    m = folium.Map(location=[coords[0][1], coords[0][0]], zoom_start=12)
    
    # Add markers
    for coord in coords:
        folium.Marker(location=[coord[1], coord[0]]).add_to(m)
    
    # If route is provided, draw the route
    if route:
        route_coords = [coords[i] for i in route]
        route_coords.append(route_coords[0])  # To make it a round trip
        folium.PolyLine(route_coords, color="red", weight=5, opacity=0.8).add_to(m)
    
    m.save(file_name)
    print(f"Map with route has been created and saved as '{file_name}'.")

def user_choice_prompt():
    """
    Displays the user choice prompt.
    
    Returns:
    str: The user's choice.
    """
    print("User Choice Prompt:")
    print("1. Read coordinates from CSV file")
    print("2. Insert your coordinates")
    print("3. Visualize coordinates on a map")
    print("4. Calculate and visualize ideal route")
    choice = input("Enter your choice (1, 2, 3, or 4):")
    return choice

# Main loop
while True:
    choice = user_choice_prompt()
    
    if choice == '1':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file, sep=',')
        df.columns = df.columns.str.strip()

        # Display the DataFrame
        print(df.to_string(index=False))
        plot_coordinates(coordinates)
        print("Read coordinates from CSV file")
    
    elif choice == '2':
        coordinates = input_coordinates()
        print("Entered coordinates:", coordinates)
        plot_coordinates(coordinates)
        print("Inserted your coordinates")
        
    elif choice == '3':
        create_map()
        print("Visualized coordinates on a map")
    
    elif choice == '4':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        route = savings_algorithm(coordinates)
        visualize_map(coordinates, route, file_name="route_map.html")
        print("Calculated and visualized ideal route")
    
    else:
        print("Invalid choice. Please enter a valid option.")
