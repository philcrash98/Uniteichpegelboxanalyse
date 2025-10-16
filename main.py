import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Daten einlesen
gboxdf = pd.read_csv('gboxdata.csv', sep=';')
weatherdf = pd.read_csv('weatherdata3.csv', sep=',', skiprows=3)

# Konvertierung der Zeitstempel in datetime-Objekte
gboxdf['Timestamp'] = pd.to_datetime(gboxdf['Timestamp'])
weatherdf["date"] = pd.to_datetime(weatherdf["time"])

# Korrekte Spalte für die Werte
value_column = 'Value'

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
combined_df = pd.merge(sensor_101_df, sensor_102_df, on='Timestamp', how='outer')
combined_df = pd.merge(combined_df, sensor_103_df, on='Timestamp', how='outer')
combined_df = pd.merge(combined_df, sensor_104_df, on='Timestamp', how='outer')
combined_df = pd.merge(combined_df, sensor_105_df, on='Timestamp', how='outer')

# Sortieren nach Timestamp
combined_df = combined_df.sort_values('Timestamp')

# Delta-Werte berechnen für alle Sensoren
combined_df['Delta101'] = combined_df['Sensorwert101'].diff()
combined_df['Delta102'] = combined_df['Sensorwert102'].diff()
combined_df['Delta103'] = combined_df['Sensorwert103'].diff()
combined_df['Delta104'] = combined_df['Sensorwert104'].diff()
combined_df['Delta105'] = combined_df['Sensorwert105'].diff()

# Wetterdaten vorbereiten - stündliche Daten in die gleiche Zeitskala bringen
# Umbenennen für bessere Klarheit
weatherdf = weatherdf.rename(columns={'date': 'Timestamp'})



# Positionen der Sensoren auf dem Strahl (prozentual, von links nach rechts)
sensor_positions = {
    'Sensor 101': 15,  # nahe am Wasser (15% von links)
    'Sensor 102': 30,  # etwas weiter
    'Sensor 103': 50,  # in der Mitte
    'Sensor 104': 70,  # weiter entfernt
    'Sensor 105': 85   # weit entfernt vom Wasser
}




# Beispiel für Bild-Zeitpunkte
start_date = combined_df['Timestamp'].min()
end_date = combined_df['Timestamp'].max()

# Bildnamen (Dateien liegen im assets-Ordner)
image_files = ["Uniteichbox13_10_25", "Uniteichbox13_10_25", "Uniteichbox13_10_25"]  # ohne Endung
image_extensions = [".jpeg", ".jpeg", ".jpeg"]  # Endungen
image_timestamps = [
    datetime(2025, 8, 29, 11, 30),
    datetime(2025, 9, 19, 0, 0),
    datetime(2025, 10, 13, 0, 0)
]

# DataFrame erstellen
image_df = pd.DataFrame({
    "Bildname": ["Uniteichbox29_08_25", "Uniteichbox19_09_25", "Uniteichbox13_10_25"],
    "Timestamp": image_timestamps,
    "Pfad": ["/assets/Uniteichbox29_08_25.jpeg", "/assets/Uniteichbox19_09_25.jpeg", "/assets/Uniteichbox13_10_25.jpeg"]
})



# App erstellen
app = Dash(__name__, assets_folder='assets')

# Layout der App definieren
app.layout = html.Div([
    html.H1('Uniteichpegel-Sensoranalyse', style={'textAlign': 'center'}),

    # Tabs für verschiedene Ansichten
    dcc.Tabs([
        # Tab 1: Sensor-Messwerte mit Delta-Werten
        dcc.Tab(label='Sensormesswerte', children=[
            html.Div([
                html.H2('Feuchtigkeitsdaten der Sensoren mit Delta-Werten'),

                # Steuerelemente
                html.Div([
                    # Linke Seite: Sensor-Auswahl
                    html.Div([

                        # Einfacher Positionsstrahl
                        html.Div([
                            # Linie mit Pfeilen
                            html.Div(style={
                                'width': '100%',
                                'height': '2px',
                                'backgroundColor': '#333',
                                'position': 'relative',
                                'margin': '40px 0',

                            }, children=[
                                # Linker Pfeil
                                html.Div(style={
                                    'position': 'absolute',
                                    'left': '-10px',
                                    'top': '-4px',
                                    'width': '0',
                                    'height': '0',
                                    'borderTop': '5px solid transparent',
                                    'borderBottom': '5px solid transparent',
                                    'borderRight': '10px solid #333'
                                }),

                                # Rechter Pfeil
                                html.Div(style={
                                    'position': 'absolute',
                                    'right': '-10px',
                                    'top': '-4px',
                                    'width': '0',
                                    'height': '0',
                                    'borderTop': '5px solid transparent',
                                    'borderBottom': '5px solid transparent',
                                    'borderLeft': '10px solid #333'
                                }),

                                # Beschriftungen
                                html.Div('nah', style={
                                    'position': 'absolute',
                                    'left': '0px',
                                    'bottom': '-20px',
                                    'fontSize': '12px',
                                    'fontWeight': 'bold'
                                }),

                                html.Div('Nähe zum Wasser', style={
                                    'position': 'absolute',
                                    'left': '50%',
                                    'transform': 'translateX(-50%)',
                                    'bottom': '-20px',
                                    'fontSize': '12px',
                                    'fontWeight': 'bold'
                                }),

                                html.Div('entfernt', style={
                                    'position': 'absolute',
                                    'right': '0px',
                                    'bottom': '-20px',
                                    'fontSize': '12px',
                                    'fontWeight': 'bold'
                                }),

                                # Markierungen für die Sensorpositionen (nur kleine Striche)
                                *[html.Div(style={
                                    'position': 'absolute',
                                    'left': f'{pos}%',
                                    'top': '-5px',
                                    'width': '1px',
                                    'height': '12px',
                                    'backgroundColor': '#333',
                                }) for sensor, pos in sensor_positions.items()],

                                # Sensorlabels
                                *[html.Div(f'S{sensor[-3:]}', style={
                                    'position': 'absolute',
                                    'left': f'{pos}%',
                                    'transform': 'translateX(-50%)',
                                    'top': '-25px',
                                    'fontSize': '11px'
                                }) for sensor, pos in sensor_positions.items()]
                            ]),
                        ], style={'margin': '30px 0 40px 0', 'width': '25%'}),
                    ]),


                ]),

                # Gemeinsames Diagramm
                dcc.Graph(id='combined-sensor-delta-graph',style={'width': '100%', 'height': '800px'}),

                html.H3('Bildaufnahmen im ausgewählten Zeitraum:'),
                html.Div(id='image-gallery', style={
                    'display': 'flex',
                    'flexWrap': 'wrap',
                    'gap': '10px',
                    'justifyContent': 'center',
                    'marginTop': '20px',
                    'height': '540px',
                    'width': 'auto'
                }),


                # Zeitraumauswahl
                html.H3('Zeitraum auswählen:'),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=combined_df['Timestamp'].min().date(),
                    max_date_allowed=combined_df['Timestamp'].max().date(),
                    start_date=combined_df['Timestamp'].min().date(),
                    end_date=combined_df['Timestamp'].max().date()
                ),
            ]),
        ]),

        # Tab 2: Statistische Auswertung
        dcc.Tab(label='Statistische Auswertung', children=[
            html.Div([
                html.H2('Statistische Auswertung der Sensordaten'),

                # Auswahl der statistischen Ansichten
                dcc.Dropdown(
                    id='stats-dropdown',
                    options=[
                        {'label': 'Boxplot - Feuchtigkeitsverteilung', 'value': 'boxplot'},
                        {'label': 'Balkendiagramm - Durchschnittswerte', 'value': 'bar'},
                        {'label': 'Korrelationsmatrix - Sensoren', 'value': 'correlation'}
                    ],
                    value='boxplot'
                ),

                # Zeitraumauswahl für Statistiken
                html.H3('Zeitraum für statistische Auswertung:'),
                dcc.DatePickerRange(
                    id='stats-date-picker-range',
                    min_date_allowed=combined_df['Timestamp'].min().date(),
                    max_date_allowed=combined_df['Timestamp'].max().date(),
                    start_date=combined_df['Timestamp'].min().date(),
                    end_date=combined_df['Timestamp'].max().date()
                ),

                # Graph für statistische Auswertung
                dcc.Graph(id='stats-graph'),

                # Zusammenfassung wichtiger Statistiken
                html.Div([
                    html.H3('Zusammenfassung der Statistiken'),
                    html.Div(id='stats-summary')
                ])
            ])
        ])
    ]),
], style={'padding': '20px', 'fontFamily': 'Arial'})



@app.callback(
    Output('combined-sensor-delta-graph', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def update_combined_graph(start_date, end_date):
    # Filterung nach Datum
    filtered_df = combined_df[
        (combined_df['Timestamp'].dt.date >= pd.to_datetime(start_date).date()) &
        (combined_df['Timestamp'].dt.date <= pd.to_datetime(end_date).date())
    ]

    fig = go.Figure()

    # --- Sensorwerte ---
    sensor_cols = [c for c in filtered_df.columns if 'Sensorwert' in c]
    for sensor in sensor_cols:
        fig.add_trace(go.Scatter(
            x=filtered_df['Timestamp'],
            y=filtered_df[sensor],
            mode='lines',
            name=sensor.replace('Sensorwert', 'Sensor '),
            visible=True
        ))

    # --- Delta-Werte ---
    delta_cols = [c for c in filtered_df.columns if 'Delta' in c]
    for delta in delta_cols:
        fig.add_trace(go.Scatter(
            x=filtered_df['Timestamp'],
            y=filtered_df[delta],
            mode='lines',
            name=delta.replace('Delta', 'Δ Sensor '),
            line=dict(dash='dot'),
            visible=True
        ))

    # --- Regenbalken ---
    rain_col = next((c for c in weatherdf.columns if 'rain' in c.lower() or 'precipitation' in c.lower()), None)
    if rain_col:
        weather_filtered = weatherdf[
            (weatherdf['Timestamp'].dt.date >= pd.to_datetime(start_date).date()) &
            (weatherdf['Timestamp'].dt.date <= pd.to_datetime(end_date).date())
        ]
        fig.add_trace(go.Bar(
            x=weather_filtered['Timestamp'],
            y=weather_filtered[rain_col],
            name='Regen (mm)',
            yaxis='y2',
            opacity=0.5,
            visible=True
        ))

    # --- Layout ---
    fig.update_layout(
        title='Feuchtigkeits- und Delta-Verläufe',
        xaxis=dict(title='Zeit'),
        yaxis=dict(title='Feuchtigkeit / Delta'),
        yaxis2=dict(
            title='Regen (mm)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(orientation='h', y=1.05, x=0),
        hovermode='x unified'
    )


    # Nach Sensor- und Delta-Traces
    # Y-Min und Y-Max der Sensorwerte bestimmen
    y_min = filtered_df[sensor_cols].min().min()
    y_max = filtered_df[sensor_cols].max().max()

    for idx, row in image_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Timestamp']],  # nur ein Punkt für Text
            y=[y_max],  # oben am Maximalwert
            mode='text',
            text=[row['Bildname']],
            textposition='top center',
            showlegend=False,
            hoverinfo='text+x'
        ))
        # Linie selbst separat hinzufügen
        fig.add_trace(go.Scatter(
            x=[row['Timestamp'], row['Timestamp']],
            y=[y_min, y_max],
            mode='lines',
            line=dict(color='purple', dash='dot', width=2),
            name='Bilder',
            showlegend=(idx == 0),  # Legende nur einmal
            hoverinfo='skip'  # Text kommt nur vom oberen Punkt
        ))

    return fig


@app.callback(
    [Output('stats-graph', 'figure'),
     Output('stats-summary', 'children')],
    [Input('stats-dropdown', 'value'),
     Input('stats-date-picker-range', 'start_date'),
     Input('stats-date-picker-range', 'end_date')]
)
def update_stats_graph(selected_view, start_date, end_date):
    try:
        # Filterung nach Zeitraum
        filtered_df = combined_df[
            (combined_df['Timestamp'].dt.date >= pd.to_datetime(start_date).date()) &
            (combined_df['Timestamp'].dt.date <= pd.to_datetime(end_date).date())
        ].copy()

        # Nur die Sensorwert-Spalten verwenden (keine Deltas, keine Zeit)
        sensor_cols = [c for c in filtered_df.columns if 'Sensorwert' in c]
        delta_cols = [c for c in filtered_df.columns if 'Delta' in c]

        fig = go.Figure()

        # --- BOX PLOT ---
        if selected_view == 'boxplot':
            for col in sensor_cols:
                fig.add_trace(go.Box(y=filtered_df[col], name=col.replace('Sensorwert', 'Sensor ')))
            fig.update_layout(title='Boxplot der Feuchtigkeitsverteilung')

        # --- BALKENDIAGRAMM ---
        elif selected_view == 'bar':
            avg_values = filtered_df[sensor_cols].mean()
            fig.add_trace(go.Bar(
                x=[col.replace('Sensorwert', 'Sensor ') for col in avg_values.index],
                y=avg_values
            ))
            fig.update_layout(title='Durchschnittliche Feuchtigkeitswerte')


        # --- KORRELATIONSMATRIX ---
        elif selected_view == 'correlation':
            corr = filtered_df[sensor_cols].corr()
            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                zmin=-1, zmax=1
            )
            fig.update_layout(title='Korrelationsmatrix der Sensoren')

        # --- Falls keine gültige Auswahl ---
        else:
            fig.update_layout(title='Bitte wählen Sie eine Statistik-Ansicht aus.')

        # === Statistische Zusammenfassung (DataTable) ===
        desc = filtered_df[sensor_cols].describe().round(2).reset_index()

        summary_table = dash_table.DataTable(
            data=desc.to_dict('records'),
            columns=[{"name": i, "id": i} for i in desc.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '5px'},
            style_header={'fontWeight': 'bold'},
            page_size=10
        )

        summary_div = html.Div([
            html.H4('Statistische Kennzahlen (Mittelwert, Std, Min, Max, etc.)'),
            summary_table
        ])

        return fig, summary_div

    except Exception as e:
        # Sicherer Rückgabewert auch bei Fehlern
        fig = go.Figure().update_layout(
            title='Fehler bei der Datenauswertung',
            annotations=[dict(text=str(e), showarrow=False, font=dict(color="red"))]
        )
        error_div = html.Div(f"Fehler in der Statistikberechnung: {e}", style={'color': 'red'})
        return fig, error_div

@app.callback(
    Output('image-gallery', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_image_gallery(start_date, end_date):
    filtered_images = image_df[
        (image_df['Timestamp'].dt.date >= pd.to_datetime(start_date).date()) &
        (image_df['Timestamp'].dt.date <= pd.to_datetime(end_date).date())
    ]
    gallery_items = []
    for _, row in filtered_images.iterrows():
        gallery_items.append(html.Div([
            html.Img(src=row['Pfad'], style={
                'width': '360px',
                'height': 'auto',
                'borderRadius': '8px',
                'cursor': 'pointer'
            }),
            html.P(row['Timestamp'].strftime("%Y-%m-%d %H:%M"), style={'textAlign': 'center', 'fontSize': '12px'})
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}))
    return gallery_items





# App starten
if __name__ == '__main__':
    app.run(debug=True)