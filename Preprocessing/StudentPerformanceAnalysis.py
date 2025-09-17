import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle 


data=pd.read_csv(r"C:\Users\USER\Downloads\Student_Performance.csv")

# print(data.head(3))

# print(data.info())

# print(data.isnull().sum())

# print(data.duplicated().sum())

data.drop_duplicates(inplace=True)

# print(data.duplicated().sum())

# print(data.describe())

# print(data.columns)

sns.pairplot(data=data)
# plt.show()

y=data["Performance Index"]

data.drop(columns=['Performance Index'],inplace=True)

x=data

print(x.columns)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

num_feature=data.select_dtypes(exclude=["object"]).columns.to_list()
obj_feature=data.select_dtypes(include=["object"]).columns.to_list()

preprocess=ColumnTransformer(transformers=[("std",StandardScaler(),num_feature),
                                           ("enc",OneHotEncoder(),obj_feature)]
)

pip=Pipeline(steps=[("pre",preprocess),
                    ("model",RandomForestRegressor(n_estimators=200, max_depth=7))])

pip.fit(x_train,y_train)

print(pip.score(x_train,y_train))

print(pip.score(x_test,y_test))


with open("StudentPerformance.pkl","wb") as fb:
    pickle.dump(pip,fb)





# ColumnTransformer → handles preprocessing (different transformations on different columns).
# Pipeline → chains preprocessing + model together into one workflow.

# Without Pipeline
# You manually do preprocessing first
# Then fit your model

# With Pipeline
# You don’t have to preprocess separately

# Everything (preprocessing + model) happens in one .fit() and .predict() call
