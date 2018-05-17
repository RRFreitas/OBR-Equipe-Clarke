import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt
import seaborn as sn

sn.set(style='whitegrid')

dataset = pd.read_csv('erro.csv', sep=',')
dataset[''] =  range(0, len(dataset))

style.use("seaborn-colorblind")
dataset.plot(x='', y='erro')
plt.show()
