'''graph generation'''

import matplotlib
matplotlib.use('Agg')
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
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
    #data = pd.read_csv('spotifysong/graph_array.csv').drop(columns=['Unnamed: 0'])
    rcParams['figure.figsize'] = 15, 20
    fig = plt.figure()
    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    fig.savefig('spotifysong/static/corr.png')


def plot_distance():
    df = pd.read_csv('spotifysong/output.csv')
    #df = pd.read_csv('output.csv').head(10)
    df = df.drop(columns='Unnamed: 0')
    fig = plt.figure()
    #ax = sns.set_theme(style='darkgrid')
    sns.catplot(x='distance', y='name', data=df)
    #canvas = FigureCanvas(fig)
    fig.savefig('spotifysong/static/distance.png')

