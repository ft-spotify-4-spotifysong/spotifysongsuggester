#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('spotify/output.csv')
df = df.drop(columns='Unnamed: 0')


def plot_1():
    sns.set_theme(style='darkgrid')
    sns_plot = sns.catplot(x='distance', y='name', data=df)
    sns_plot.figure.savefig("spotify/static/output1.png")


def plot_2():
    sns.set_theme(style='darkgrid')
    sns_plot = sns.barplot(x='distance', y='name', data=df)
    sns_plot.figure.savefig("spotify/static/output2.png")
