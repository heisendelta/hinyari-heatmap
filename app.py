from flask import Flask, request, jsonify, render_template, render_template_string, redirect, url_for
import folium
import geopandas as gpd
import pandas as pd
from datetime import datetime

import pickle
from heatmap import *
from graphs import *

influenced_series_df = pd.read_csv('data/influenced_series.csv')
with open('data/graph.pkl', 'rb') as f:
    G_filtered = pickle.load(f)


app = Flask(__name__)

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('info', date=datetime.today().strftime('%m-%d'))) # redirects to today's date

@app.route('/info')
def info():
    date = request.args.get('date', '01-01')

    map = HeatmapBase(influenced_series_df, weight_col=f'2022-{date}', zoom_start=13).render()
    map_html = map._repr_html_()
    month, day = str(int(date.split('-')[0])), str(int(date.split('-')[1]))

    return render_template('info.html', map_html=map_html, date=date, month=month, day=day)

@app.route('/region_info')
def region_info():
    region = request.args.get('region', '')
    date = request.args.get('date', '01-01') # 01-01

    if date == '':
        date = '01-01'
    if len(date.split('-')) > 2:
        date = '-'.join(date.split('-')[-2:])
    if region == '':
        return redirect(url_for('info', date=date))
    
    map = HeatmapNode(region, weight_col=f'2022-{date}', zoom_start=15).render()
    map_html = map._repr_html_()
    month, day = str(int(date.split('-')[0])), str(int(date.split('-')[1]))

    return render_template('region_info.html', 
                           region=region, 
                           map_html=map_html, 
                           date=date, month=month, day=day,
                           graph1_plot_url=case_count_bar_chart(region),
                           graph2_plot_url=case_density_function(region),
                           ranking=top_n_influenced(region, date, n=3),
                           graph3_plot_url=horizontal_stacked_bar(region))

if __name__ == '__main__':
    app.run(debug=True)
