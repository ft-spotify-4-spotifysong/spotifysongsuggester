'''graph generation'''

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns
import pandas as pd


def plot_correlation():
    '''
    plot correlation's matrix to explore dependency between features 
    '''
    # init figure size
    data = pd.read_csv('spotifysong/correlation.csv').drop(columns=['Unnamed: 0'])
    #data = pd.read_csv('correlation.csv').drop(columns=['Unnamed: 0'])
    rcParams['figure.figsize'] = 15, 20
    fig = plt.figure()
    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    fig.savefig('static/corr.png')


def plot_distance():
    df = pd.read_csv('spotifysong/output.csv').iloc[1:11,:]
    #df = pd.read_csv('output.csv').iloc[1:11,:]
    df = df.drop(columns='Unnamed: 0')
    print('df--------', df)
    fig, ax = plt.subplots(figsize=(8,8))
    ax = sns.set_theme(style='darkgrid')
    snsf = sns.catplot(x='distance', y='name', data=df)
    snsf.figure.savefig('static/distance.png')
    #canvas = FigureCanvas(fig)
    #fig.savefig('static/distance.png')

