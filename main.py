from flask import Flask, request, jsonify, render_template, render_template_string
import folium
import geopandas as gpd
import pandas as pd

import pickle
from heatmap import *

influenced_series_df = pd.read_csv('data/influenced_series.csv')
with open('data/graph.pkl', 'rb') as f:
    G_filtered = pickle.load(f)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/region_info')
def region_info():
    region = request.args.get('region', '豊島区南池袋１丁目')
    date = request.args.get('date', '01-01') # 01-01
    print(region, date)
    if region == '':
        region = '豊島区南池袋１丁目'
    if date == '':
        date = '01-01'
    if len(date.split('-')) > 2:
        date = '-'.join(date.split('-')[-2:])
    print(region, date)
    
    map = HeatmapNode(region, weight_col=f'2022-{date}', zoom_start=15).render()
    map_html = map._repr_html_()

    return render_template_string("""
        <html>
            <head>
                <title>{{ region }} | 情報</title>
                <style>
                    body { padding: 0; margin: 0; }
                    .leaflet-container { font-size: 1rem; }
                    .map-container {
                        position: relative;
                        height: 100vh; /* Full height map container */
                    }
                    .search-container {
                        position: absolute;
                        top: 10px; /* Distance from top */
                        left: 5%; /* Distance from left */
                        z-index: 1000; /* Ensure it sits above the map */
                        display: flex;
                        align-items: center;
                    }
                    .search-bar, .date-input, .search-button {
                        padding: 10px;
                        font-size: 16px;
                        border: 1px solid #ccc;
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
                        border-radius: 5px; /* Smaller border radius */
                        margin: 0;
                        height: 40px;
                    }
                    .search-bar, .date-input {
                        border-right: none; /* Remove right border between inputs */
                    }
                    .date-input {
                        border-left: none; /* Remove left border of date input */
                    }
                    .search-button {
                        background-color: #4285F4;
                        color: white;
                        cursor: pointer;
                        border-radius: 0 5px 5px 0; /* Rounded only on the right */
                    }
                    .search-button:hover {
                        background-color: #357AE8;
                    }

                    #search-container input[type="text"],
                    #search-container input[type="date"],
                    #search-container button {
                        margin: 0;
                    }
                    #search-container input[type="text"] {
                        border-radius: 4px 0 0 4px;
                    }

                    #search-container input[type="date"] {
                        border-radius: 0;
                    }

                    #search-container button {
                        border-radius: 0 4px 4px 0;
                    }
                                  
                    .side-panel {
                        position: absolute;
                        top: 10%;
                        left: 5%;
                        width: 400px;
                        height: 85%;
                        background-color: rgba(255, 255, 255, 0.9);
                        z-index: 1001;
                        padding: 20px;
                        box-shadow: -2px 0 5px rgba(0,0,0,0.3);
                        overflow-y: auto;
                    }
                    .side-panel h2 {
                        font-size: 24px;
                        margin-bottom: 20px;
                    }
                    .side-panel .graph-placeholder {
                        width: 100%;
                        height: 200px;
                        background-color: #e0e0e0;
                        margin-bottom: 20px;
                    }
                    .side-panel p {
                        font-size: 16px;
                        line-height: 1.5;
                    }
                </style>
            </head>
            <body>
                <div class="map-container">
                    <div class="search-container">
                        <form id="search-form" action="/region_info" method="get">
                            <input type="text" name="region" class="search-bar" placeholder="Search for a region...">
                            <input type="date" name="date" class="date-input">
                            <button type="submit" class="search-button">Search</button>
                        </form>
                    </div>
                    <div id="map">
                        {{ map_html | safe }}
                    </div>
                    <div class="side-panel">
                        <h2>{{ region }}</h2>
                        <div class="graph-placeholder">Graph Placeholder</div>
                        <p>This is some placeholder text to give an idea of what the side panel might contain. It can include a summary, analysis, or any other relevant information.</p>
                    </div>
                </div>
            </body>
        </html>
    """, region=region, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
