import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import seaborn as sns

import japanize_matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib
matplotlib.use('Agg')

time_grouped = pd.read_csv('data/time_grouped.csv').set_index('市区町丁')

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
    ax.set_xlabel('時間', fontsize=12)
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
