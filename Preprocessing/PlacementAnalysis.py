import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle


data=pd.read_csv(r"C:\Users\USER\Downloads\placementdata.csv")

# print(data.head(3))

# print(data.isnull().sum())

# print(data.info())

# print(data.duplicated().sum())

# print(data.columns)

data.drop(columns=['StudentID'],inplace=True)

sns.pairplot(data=data)
# plt.show()

y=data['PlacementStatus']

data.drop(columns=['PlacementStatus'],inplace=True)

x=data

print(x.columns)

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=35,test_size=0.2)

num_feat=data.select_dtypes(exclude=["object"]).columns.tolist()
cat_feat=data.select_dtypes(include=["object"]).columns.to_list()

preprocess=ColumnTransformer(transformers=[("num",StandardScaler(),num_feat),
                                           ("cat",OneHotEncoder(drop="first"),cat_feat)])
# the transformers parameter is a list of tuples, where each tuple tells Python:
# # Name of the step – just a string to identify it
# Transformer object – something that will actually process your data (like StandardScaler(), OneHotEncoder()).
# Columns – which columns of the dataframe this transformer should be applied to.


pip=Pipeline(steps=[("pre",preprocess),
                    ("model",BaggingClassifier(estimator=DecisionTreeClassifier(max_depth=5),n_estimators=300, max_samples=0.8,max_features=0.8,random_state=42))])

pip.fit(x_train,y_train)

# print(pip.score(x_train,y_train))

# print(pip.score(x_test,y_test))


sample = pd.DataFrame([[7.5, 1, 1, 1, 65, 4.4, 'No', 'No', 61, 79]],
                      columns=x.columns)

print(pip.predict(sample))

with open("placementAnalysis.pkl","wb") as fb:
    pickle.dump(pip,fb)










