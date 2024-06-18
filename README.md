# Informatik2Projekt
## Beschreibung:

Erstellung eines Tansport Management Software (TMS) Prototypen, zum planen von Touren.

### Anforderungen:

- Bei verwendung sollen Startpunkt und Zielpunkt eingebbar sein.


1. Die Software soll es dem Nutzer ermöglichen Koordinaten einzugeben.

    1.1 Die Software soll über eine Eingabe durch das Terminal verfügen
 
   1.2 Sie Software soll die Koordinaten durch eine CSV-Datei einlesen.

       1.2.1 Die Software soll CSV-Datei aus dem Directory ziehen und auflisten.
       1.2.2. Panda Bibliothek importieren
       1.2.3. CSV-Dateiformat: Die CSV-Datei muss mindestens zwei Spalten enthalten: Longitude und Latitude.
       1.2.4. Implementiere eine Funktion zum Lesen von Koordinaten aus einer angegebenen CSV-Datei.
            1.2.4.1. Die Funktion sollte die Datei öffnen, die Daten lesen und die Koordinaten in eine Liste von Tupeln extrahieren.
            1.2.4.2. Bei Erfolg einen DataFrame zurückgeben, der die Daten enthält.
            1.2.4.3. Eine Fehlermeldung ausgeben und einen leeren DataFrame zurückgeben, wenn die Datei nicht gefunden wird.
       1.2.5. Eine Funktion erstellen, die es dem Benutzer ermöglicht, Longitude und Latitude manuell einzugeben.
            1.2.5.1. Die Eingaben werden bestätigt, um sicherzustellen, dass sie numerisch sind und innerhalb der gültigen Bereiche liegen (Longitude: -180 bis 180 und
            Latitude: -90 bis 90)
       1.2.6. Kontinuierliche Aufforderung an den Benutzer, bis er "Stop" eingibt.


   1.3 Die Software soll eine Auswahl-Prompt geben

       1.3.1 Die Auswahl soll über individuelle Eingabe, Koordinateneinzeichnung in Karte und Tourenplanung verfügen.
           1.3.1.1. Visualisierung von Streudiagrammen: Eine Funktion soll entwickelt werden, um die angegebenen Koordinaten in einem Streudiagramm darzustellen.
                    i. Die x-Achse steht für den Longitude und die y-Achse für den Latitude.
                    ii. Das Diagramm soll mit Matplotlib dargestellt werden.
           1.3.2. Gib die Auswahl des Benutzers als String zurück.


   1.4 Die Software soll nach der Auswahl  des Benutzers ein Return-Statement geben.

       1.4.1 Das Return-Statement soll angemessene Beschreibung enthalten.

   1.5 Die Software soll eine HTML Datei im Directory erstellen.

       1.5.1 Die HTML Datei sollte eine Karte nach Auswahl des Benutzers zeigen.
       1.5.1.1. Entwicklung einer Funktion zur Erstellung einer Foliumkarte mit Markierungen für jede Koordinate.
       1.5.1.2. Die Karte soll auf der Grundlage des Mittelwerts der Longitude und Latitude zentriert werden.
       1.5.1.3. Die Markierungen sollen für jede Koordinate hinzugefügt werden und die Karte wird als HTML-Datei mit dem Namen "mapp.html" gespeichert.


   1.6 Die Software soll zum berechnen einer Tourenplanung den Savings Algorythmus verwenden.

3. Der Code der Softare sollte Teil-Beschreibungen beinhalten.


## Description

Creation of a Transport Management Software (TMS) Prototype, that is able to plan tours.

### Requests:

1. The software should let the user input coordinates.

   1.1 The software should receive the input through the terminal.

   1.2 The software should read the coordinates from a CSV-File.

       1.2.1 The software should pull the CSV-File from the directory and list the given Values.
       1.2.2. Import panda library
       1.2.3. CSV File Format: The CSV file must contain at least two columns: Longitude and Latitude.
       1.2.4. Implement a function to read coordinates from a specified CSV file.
            1.2.4.1. The function should open the file, read the data, and extract the coordinates into a list of tuples.
            1.2.4.2. Return a DataFrame containing the data if successful.
            1.2.4.3. Print an error message and return an empty DataFrame if the file is not found.
       1.2.5. Create a function that allows users to input longitude and latitude values manually.
            1.2.5.1. Validate the inputs to ensure they are numerical and within the valid ranges (Longitude: -180 to 180 and
            Latitude: -90 to 90)
       1.2.6. Continuously prompt the user until they type 'stop'.

    1.3 The software should give a user choice-prompt.

       1.3.1 The user choice-prompt should include individual input by user, viualization of CSV-File coordinates in a Map, calculation of ideal route with visualization in 
             a Map.
           

    1.4 The software should give a return statement based upon user-selection.

       1.4.1 the return-statement should include a statement of what it did.

    1.5 The software should create an HTML-file in the directory.

       1.5.1 The HTML-file should direct the user to a map with the values and criteria previously chosen by the user.
           1.5.1.1. Develop a function to create a folium map with markers for each coordinate.
           1.5.1.2. Center the map based on the mean of the latitude and longitude values.
           1.5.1.3. Add markers for each coordinate and save the map as an HTML file named 'mapp.html'.

   1.6 The software should use the Savings-Algorythm to calculate the ideal route between the coordinates given.

3. The softwares code should inlude documentation and description of the segments within.
