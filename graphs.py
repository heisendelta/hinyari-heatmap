import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import seaborn as sns
import pickle
import matplotlib.colors as mcolors
import numpy as np

import japanize_matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib
matplotlib.use('Agg')

time_grouped = pd.read_csv('data/time_grouped.csv').set_index('市区町丁')
with open('data/predict_dicts.pkl', 'rb') as f:
    predict_dicts = pickle.load(f)

danger_indices_normalized = pd.read_csv('data/danger_indices.csv')
danger_indices_normalized = danger_indices_normalized.set_index('市区町丁')

proportions = pd.read_csv('data/proportions.csv').set_index('市区町丁')
crime_types = pd.read_csv('data/crime_types.csv').set_index('市区町丁')

def create_img(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def case_count_bar_chart(region):
    fig, ax = plt.subplots()

    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    ax.bar(time_grouped.columns, time_grouped.loc[region].astype(int))
    ax.set_xlabel('時間 (24時制)', fontsize=12)
    ax.set_ylabel('ケース数', fontsize=12)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    return create_img(fig)

def case_density_function(region):
    fig, ax = plt.subplots()

    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    sns.kdeplot(time_grouped.loc[region], bw_adjust=0.5, fill=True, ax=ax)
    ax.set_xlabel('1日のケース数', fontsize=12)
    ax.set_xlim(left=0)
    ax.set_ylabel('密度', fontsize=12)
    ax.grid(True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    return create_img(fig)

def top_n_influenced(region, date, n=3):
    neighbor_keys = list(predict_dicts[region].keys())
    # df = pd.DataFrame([predict_dicts[region][key] for key in neighbor_keys], index=neighbor_keys, columns=pd.date_range('2022-01-01', periods=365, freq='D').strftime('%Y-%m-%d'))
    # df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)
    # df = df.apply(lambda x: x ** 10)
    # df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

    # df = df.fillna(0)
    # return df[f'2022-{date}'].drop(region, axis=0).nlargest(n).index.to_list()
    return danger_indices_normalized.loc[neighbor_keys][f'2022-{date}'].nlargest(n).index.to_list()

# Horizontal stacked bar
def hex_to_rgba(hex_str, alpha=1.0):
    rgba = mcolors.to_rgba(hex_str, alpha=alpha)
    return rgba

def horizontal_stacked_bar(region):
    category_names = crime_types.columns
    results = proportions.loc[[region]].T.to_dict()
    results = {k: list(v.values()) for k, v in results.items()}

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = ['#EA2027', '#F79F1F', '#009432', '#0652DD', '#12CBC4', '#6F1E51', '#1B1464']

    fig, ax = plt.subplots(figsize=(30, 4))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)

        r, g, b, _ = hex_to_rgba(color)
        text_color = 'white' if r * g * b < 0.2 else 'darkgrey'
        for j, (rect, width) in enumerate(zip(rects, widths)):
            if width > 0:
                ax.text(rect.get_x() + rect.get_width() / 2, rect.get_y() + rect.get_height() / 2,
                        f'{crime_types.loc[region, crime_types.columns[i]]}', ha='center', va='center', color=text_color, fontsize=50)

    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1), loc='lower left', fontsize=27)

    # ax.set_xlim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # ax.legend().set_visible(False)
    plt.tight_layout()

    return create_img(fig)
