import pandas as pd
import numpy as np

#sample data
data={'Age':[25,np.nan,30,35,np.nan,40]}
df=pd.DataFrame(data)

#Replace missing values with mean
df['Age_Mean']=df['Age'].fillna(df['Age'].mean())

#Replace missing values with median
df['Age_Median']=df['Age'].fillna(df['Age'].median())

#Replace missing values with mode
df['Age_Mode']=df['Age'].fillna(df['Age'].mode()[0])

print(df)

#forward fill
df['Age_Fill_Forward']=df['Age'].ffill()

#Backward fill
df['Age_Fill_Backward']=df['Age'].bfill()

print(df)