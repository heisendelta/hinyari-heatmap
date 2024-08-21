import folium
from folium.plugins import HeatMap
from folium import Choropleth
from matplotlib import cm, colors, colormaps
from matplotlib.colors import LinearSegmentedColormap

# Get subregions
import geopandas as gpd
import pandas as pd
import pickle

def convert_kanji_to_num(s):
    if pd.isna(s):
        return s
    return s.replace('〇', '０').replace('一', '１').replace('二', '２').replace('三', '３').replace('四', '４').replace('五', '５').replace('六', '６').replace('七', '７').replace('八', '８').replace('九', '９')

subregions = gpd.read_file('data/subregions.geojson')
subregions = subregions.to_crs(epsg=4326)
subregions['市区町丁'] = subregions.apply(lambda row: f"{row['CITY_NAME']}{convert_kanji_to_num(row['S_NAME'])}", axis=1)

# Get predict_dicts
with open('data/predict_dicts.pkl', 'rb') as f:
    predict_dicts = pickle.load(f)

class HeatmapBase:
    def __init__(self, df, weight_col=None, zoom_start=12, colormap=None):
        self.df = pd.merge(df, subregions[['市区町丁', 'geometry']], on='市区町丁', how='left')
        self.df = self.df[~self.df['geometry'].isna()]
        self.weight_col = weight_col
        self.zoom_start = zoom_start

        combined_geometry = gpd.GeoSeries(self.df['geometry']).unary_union
        self.centroid = combined_geometry.centroid
        self.m = folium.Map(location=[self.centroid.y, self.centroid.x], zoom_start=self.zoom_start, tiles='cartodbpositron')
        self.colormap = colormap if colormap is not None else LinearSegmentedColormap.from_list('green_yellow_red', ['green', 'yellow', 'red'])
        # self.m = folium.Map(location=[35.682839, 139.759455], zoom_start=12, tiles='cartodbpositron')

        print(self.centroid)

    def render(self):
        if self.weight_col is not None:
            norm = colors.Normalize(vmin=self.df[self.weight_col].min(), vmax=self.df[self.weight_col].max())
            # cmap = colormaps.get_cmap('viridis')
            cmap = self.colormap

        for _, row in self.df.iterrows():
            if row['geometry'] is not None:
                if self.weight_col is not None:
                    color = colors.to_hex(cmap(norm(row[self.weight_col])))
                else:
                    color = '#3186cc'  # Default color when weight_col is None

                folium.GeoJson(
                    row['geometry'].__geo_interface__,
                    style_function=lambda _, color=color: {
                        'fillColor': color,
                        'color': None,
                        'weight': 0,
                        'fillOpacity': 0.7
                    }
                ).add_to(self.m)

        return self.m

    def reset_map(self):
        self.m = folium.Map(location=[self.centroid.y, self.centroid.x], zoom_start=self.zoom_start, tiles='cartodbpositron')

class HeatmapNode(HeatmapBase):
    def __init__(self, node, weight_col=None, zoom_start=12):
        neighbor_keys = list(predict_dicts[node].keys())
        df = pd.DataFrame([predict_dicts[node][key] for key in neighbor_keys], index=neighbor_keys, columns=pd.date_range('2022-01-01', periods=365, freq='D').strftime('%Y-%m-%d'))
        df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)
        df = df.apply(lambda x: x ** 10)
        df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

        df = df.reset_index(drop=False).rename(columns={ 'index': '市区町丁' })

        self.node = node
        self.colormap = LinearSegmentedColormap.from_list('yellow_to_red', ['#f1c40f', '#e74c3c'])
        super().__init__(df, weight_col=weight_col, zoom_start=zoom_start, colormap=self.colormap)