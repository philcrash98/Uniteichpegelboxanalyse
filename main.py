import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from fontTools.misc.testTools import parseXML
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.express as px
from dash import dcc
import plotly.graph_objs as go

# Daten einlesen
gboxdf = pd.read_csv('gboxdata092025.csv', sep=';')
weatherdf = pd.read_csv('openmeteodata.csv', sep=',', skiprows=3)

# Konvertierung der Zeitstempel in datetime-Objekte
gboxdf['Timestamp'] = pd.to_datetime(gboxdf['Timestamp'])

value_column = 'Value'  # Hier den korrekten Spaltennamen eintragen

# Für jeden Sensor einen DataFrame erstellen mit korrekter Filterung
sensor_101_df = gboxdf[(gboxdf['SensorID'] == 101) & (gboxdf['MeasureName'] == 'moisture')][['Timestamp', value_column]]
sensor_102_df = gboxdf[(gboxdf['SensorID'] == 102) & (gboxdf['MeasureName'] == 'moisture')][['Timestamp', value_column]]
sensor_103_df = gboxdf[(gboxdf['SensorID'] == 103) & (gboxdf['MeasureName'] == 'moisture')][['Timestamp', value_column]]
sensor_104_df = gboxdf[(gboxdf['SensorID'] == 104) & (gboxdf['MeasureName'] == 'moisture')][['Timestamp', value_column]]
sensor_105_df = gboxdf[(gboxdf['SensorID'] == 105) & (gboxdf['MeasureName'] == 'moisture')][['Timestamp', value_column]]

# Umbenennung der Value-Spalte für jeden Sensor
sensor_101_df = sensor_101_df.rename(columns={value_column: 'Sensorwert101'})
sensor_102_df = sensor_102_df.rename(columns={value_column: 'Sensorwert102'})
sensor_103_df = sensor_103_df.rename(columns={value_column: 'Sensorwert103'})
sensor_104_df = sensor_104_df.rename(columns={value_column: 'Sensorwert104'})
sensor_105_df = sensor_105_df.rename(columns={value_column: 'Sensorwert105'})


# Zusammenführen der DataFrames über den Timestamp
# Zuerst 101 und 102 zusammenführen
combined_df = pd.merge(sensor_101_df, sensor_102_df, on='Timestamp', how='outer')

# Dann die restlichen nacheinander hinzufügen
combined_df = pd.merge(combined_df, sensor_103_df, on='Timestamp', how='outer')
combined_df = pd.merge(combined_df, sensor_104_df, on='Timestamp', how='outer')
combined_df = pd.merge(combined_df, sensor_105_df, on='Timestamp', how='outer')

# Sortieren nach Timestamp
combined_df = combined_df.sort_values('Timestamp')

# Anzeigen des resultierenden DataFrames
print(combined_df.head())

# Korrektur: Überprüfen der tatsächlichen Spaltennamen
# Nutzen der ersten Spalte als Datum (angenommen, es ist die Zeitangabe)
  # Erste Spalte als Datumsspalte nehmen
weatherdf["date"] = pd.to_datetime(weatherdf["date"]).copy()


sensor_101_delta = sensor_101_df.copy()
sensor_101_delta['Delta'] = sensor_101_df['Value'].diff()
# Ersten Wert entfernen, da hier kein Delta berechnet werden kann
sensor_101_delta = sensor_101_delta.dropna()


