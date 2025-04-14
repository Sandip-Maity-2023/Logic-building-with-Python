import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
df=pd.read_csv('Feature_Selection_DS[1].csv')
numeric=df.select_dtypes(include=['int64','float64'])
matrix = numeric.corr()
plt.title('Correlation Matrix')
plt.figure(figsize=(10,10))
plt.show(matrix)
