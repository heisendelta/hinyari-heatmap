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
danger_indices_normalized = pd.read_csv('data/danger_indices.csv')
danger_indices_normalized = danger_indices_normalized.set_index('市区町丁')

def convert_kanji_to_num(s):
    if pd.isna(s):
        return s
    s = s.replace('〇', '０').replace('一', '１').replace('二', '２').replace('三', '３').replace('四', '４').replace('五', '５').replace('六', '６').replace('七', '７').replace('八', '８').replace('九', '９')
    return s.replace('0', '０').replace('1', '１').replace('2', '２').replace('3', '３').replace('4', '４').replace('5', '５').replace('6', '６').replace('7', '７').replace('8', '８').replace('9', '９')



app = Flask(__name__)

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('info', date=datetime.today().strftime('%m-%d'))) # redirects to today's date

@app.route('/info')
def info():
    date = request.args.get('date', '01-01')

    map = HeatmapBase(influenced_series_df, weight_col=f'2022-{date}', zoom_start=14).render()
    map_html = map._repr_html_()
    month, day = str(int(date.split('-')[0])), str(int(date.split('-')[1]))

    with open(f'templates/info/{date}.html', 'w') as f:
        f.write(render_template('info.html', map_html=map_html, date=date, month=month, day=day))
        print('Saved at', f'templates/info/{date}.html')

    return render_template('info.html', map_html=map_html, date=date, month=month, day=day)

@app.route('/region_info')
def region_info():
    region = request.args.get('region', '')
    date = request.args.get('date', datetime.today().strftime('%m-%d')) # 01-01

    if date == '':
        date = datetime.today().strftime('%m-%d')
    if len(date.split('-')) > 2:
        date = '-'.join(date.split('-')[-2:])
    if region == '':
        return redirect(url_for('info', date=date))
    region = convert_kanji_to_num(region)

    map = HeatmapNode(region, weight_col=f'2022-{date}', zoom_start=15).render()
    map_html = map._repr_html_()
    month, day = str(int(date.split('-')[0])), str(int(date.split('-')[1]))

    with open(f'templates/region_info/{region}_{date}.html', 'w') as f:
        f.write(render_template('region_info.html', 
                           region=region, 
                           map_html=map_html, 
                           date=date, month=month, day=day,
                           graph1_plot_url=case_count_bar_chart(region),
                        #    graph2_plot_url=case_density_function(region),
                           ranking=top_n_influenced(region, date, n=3),
                        #    graph3_plot_url=horizontal_stacked_bar(region)
                            danger_index=round(danger_indices_normalized.loc[region, f'2022-{date}'], 3),
                           ))
        print('Saved at', f'templates/region_info/{region}_{date}.html')

    return render_template('region_info.html', 
                           region=region, 
                           map_html=map_html, 
                           date=date, month=month, day=day,
                           graph1_plot_url=case_count_bar_chart(region),
                        #    graph2_plot_url=case_density_function(region),
                           ranking=top_n_influenced(region, date, n=3),
                        #    graph3_plot_url=horizontal_stacked_bar(region)
                            danger_index=round(danger_indices_normalized.loc[region, f'2022-{date}'], 3),
                           )

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
