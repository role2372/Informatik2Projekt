# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:25:40 2024

@author: ACER
"""
import matplotlib.pyplot as plt
import pandas as pd
import folium




def read_coordinates_from_csv(file):
    
    df = pd.read_csv(file, sep=',', header=0)
    
    coordinates = list(zip(df['Longitude'], df['Latitude']))    
    return coordinates
    


def input_coordinates():
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
                
            
            coordinates.append((x,y))
             
        except ValueError:
           print("Invalid input. Please enter numerical values or type 'stop' to finish")
            
           
    return coordinates


def getCoordinates(coordinates):
     

    x_values = [coord[0] for coord in coordinates]
    y_values = [coord[1] for coord in coordinates]
    
    plt.scatter(x_values, y_values)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Visualization of Coordinates')
    plt.show()




def user_choice_prompt():
    print("User Choice Prompt:")
    print("1.Read coordinates from CSV file")
    print("2.Insert your coordinates")
    choice = input("Enter your choice (1 or 2):")
    
    return choice


def main():
    choice = user_choice_prompt()
    
    if choice == '1':
        file = 'lieferorte.csv'
        coordinates = read_coordinates_from_csv(file)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv('lieferorte.csv', sep=',')
        df.columns = df.columns.str.strip()


       # Display the DataFrame
        print(df.to_string(index=False))
        getCoordinates(coordinates)
        return "Read coordinates from CSV file"
    
    
        
    elif choice == '2':
        coordinates = input_coordinates()
        print("Enter coordinates:", coordinates)
        getCoordinates(coordinates)
        return "Insert your coordinates"
    
    else:
        print("Invalid choice.")
        return "Invalid choice"
    
if __name__ == "__main__":
    action_taken = main()
    print("Return statement based upon user-selection:")
    
    