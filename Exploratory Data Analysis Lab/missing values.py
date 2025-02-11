import pandas as pd

#Example dataset
data={
    'ID':[101,102,103,104,105,106,107],
    'Name':['Debjit','virat','Jasprit','Rohit','Rahul','Jadeja','Bimal'],
    'Age' :[25,46,43,25,25,100000,46],
    'Salary':[11000,None,45000,56000,45000,None,23000],
    'Department':['ML R&D','IT','IT','YouTuber','SDE2',None,'SDE3'],
    'City':['Mumbai','Delhi','kolkata','pune','bangalore','Hydrabad','kolkata']
}

#create a DataFrame
df=pd.DataFrame(data)
print('\nPrinting the table:\n')
print(df)
print("\nColumn list are:\n")
print(df.Age)

#no of rows and columns
print("\nShape of the data set\n")
print(df.shape)

print("\n1st 5 rows of the data Set\n")  #head always cut 5 values
print(df.head())

print("\nlat 5 rows of the data set\n")
print(df.tail())

print('\n')

#deleting the rows from where have none values

print(df.dropna())

print('\n')

print('Handling the missing value in age 5 is 10,000')
df.loc[5, 'Age']=23
print(df)

df.loc[3, 'Department']='DA'
print(df)

df.loc[1, 'Salary']=9000
print(df)

df.loc[5, 'Department']='HR'
print(df)

#calculating average salary
#average=sum('Salary')/len('Salary')

average=df['Salary'].mean()
print(f"Average Salary: {average}")

"""update={
    None if 'Salary'==average else 'Salary' for 'Salary' in 'Salary'
}
print(update)"""

df['Salary'].fillna(average, inplace=True)
print(df)

#df.loc[5,'Salary']='avg()'
