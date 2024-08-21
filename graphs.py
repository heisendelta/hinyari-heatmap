import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import seaborn as sns
import pickle

import japanize_matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib
matplotlib.use('Agg')

time_grouped = pd.read_csv('data/time_grouped.csv').set_index('市区町丁')
with open('data/predict_dicts.pkl', 'rb') as f:
    predict_dicts = pickle.load(f)

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
    df = pd.DataFrame([predict_dicts[region][key] for key in neighbor_keys], index=neighbor_keys, columns=pd.date_range('2022-01-01', periods=365, freq='D').strftime('%Y-%m-%d'))
    df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)
    df = df.apply(lambda x: x ** 10)
    df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

    df = df.fillna(0)
    return df[f'2022-{date}'].drop(region, axis=0).nlargest(n).index.to_list()
