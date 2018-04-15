import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt

dataset = pd.read_csv('piddata.csv', sep=',')
dataset['tempo'] = range(0,879)

style.use("seaborn-colorblind")
dataset.plot(x='tempo', y=['erro', 'potencia direita', 'potencia esquerda'])
plt.show()