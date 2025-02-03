import pandas as pd
import numpy as np

#Sample dataset
data={
    'customerID':[101,102,103,104,10],
    'Age':[25,np.nan,30,np.nan,40],
    'city':['New york',np.nan,'chicago',np.nan,'New York'],
    'Monthly Spending($)':[200,np.nan,150,120,300]
}
df=pd.DataFrame(data)
print(df)

