import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle



data=pd.read_csv(r"C:\Users\USER\Downloads\data.csv")

# print(data.head(3))

# print(data.isnull().sum())

# print(data.duplicated().sum())

# print(data.info())

# print(data.describe())

print(data.columns)

x= data[["Eating_Out", "Entertainment", "Miscellaneous", "Groceries", "Transport",'Desired_Savings',      
       'Disposable_Income']]

scal=StandardScaler()

x_std=scal.fit_transform(x)

with open("BudgetScale.pkl","wb") as fb:
    pickle.dump(scal,fb)


wcss=[]

for i in range(2,10):
    kmm=KMeans(n_clusters=i,init='k-means++')
    kmm.fit(x_std)
    wcss.append(kmm.inertia_)

plt.plot(range(2, 10), wcss, marker='o')
plt.grid(axis='x')
# plt.show()

kmm=KMeans(n_clusters=4,init="k-means++")
kmm.fit(x_std)

with open("BudgetClusterModel.pkl","wb") as fb:
    pickle.dump(kmm,fb)

# In clustering (KMeans, Hierarchical, etc.), the algorithm does not know the meaning of clusters.
# It only groups similar data points together.
# So we (the data scientist) have to interpret each cluster after training.

centroids=scal.inverse_transform(kmm.cluster_centers_) #array
cluster_profiles=pd.DataFrame(centroids,columns=x.columns)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
print(cluster_profiles)

# kmeans.cluster_centers_ → gives you those centroid coordinates, but in the scaled space (because we scaled the data before clustering).
# scaler.inverse_transform(...) → converts them back to original spending units

# ------------------------------------------------------------------------------
# NOTE!!
# Your 4 clusters (the centroids) all show
# Disposable_Income > Desired_Savings(Your data distribution probably had more people with disposable ≥ desired, so the centroids ended up that way.)

# So it looks like everyone is in profit.
# But in reality, clustering works like this:
# Clusters represent the average profile.
# When you add new data (a new user), they will still get assigned to the nearest cluster even if their situation is different (e.g., they are in deficit).

# Eating_Out = 3000
# Entertainment = 2000
# Miscellaneous = 1500
# Groceries = 9000
# Transport = 4000
# Desired_Savings = 10000
# Disposable_Income = 6000

# Disposable_Income (6000) < Desired_Savings (10000) → user is not saving enough .

# Clustering (like KMeans) does not care business rules or conditions (whether Disposable_Income < Desired_Savings )
# >— it just looks at the pattern of all features together.

# So when you feed a new data point:
# It scales the features.
# Finds the nearest cluster centroid (Euclidean distance).
# Assigns that point to that cluster, even if the centroid itself has Disposable > Desired.

# Deep EXPLANATION

# Clustering algorithms look for patterns in the features, like similarity or distance between data points.
# They do NOT enforce any business rules or conditions.
# So, even if a new data point violates a rule (like Disposable_Income < Desired_Savings), 
# it will still be assigned to the cluster whose centroid it is closest to.

# ✅ Example:
# Cluster 2 might have most students with Disposable_Income > Desired_Savings, but a new student with Disposable_Income < Desired_Savings
#  can still end up in Cluster 2 if its other features match that cluster’s pattern.

# 2️⃣ Recommendation on conditions
# To recommend actions or flag rule violations, you cannot rely on clustering alone.
# You can make a custom function to check conditions and give advice.

# ---------------------------------------------------------------------------------------------

# cluster_profiles is a table (usually a DataFrame) that summarizes the average spending behavior of each cluster.
# eg 
# Cluster	Eating_Out	Entertainment	Groceries	Transport	Disposable_Income	Desired_Savings
# 0	      200	         150	        300	       100	            500	            400
# 1	      100	          80	        250	        120	            400              3000
# centriod show average of all feature accordding to that group

def recommend_savings(new_data,scale,model,cluster_profiles):
     # 1. Extract features in the same order as training
    features =new_data[["Eating_Out", "Entertainment", "Miscellaneous",
                         "Groceries", "Transport", "Desired_Savings", "Disposable_Income"]]
    
    scale_x=scale.transform(features)
   
    # cluster_id comes from a model prediction → usually numpy.int64.
    # Flask’s jsonify can only handle native Python types → int, float, str, list, dict.

    cluster_id=int(model.predict(scale_x)[0])
    cluster_profile=cluster_profiles.loc[cluster_id] # it give the details of centriod of that cluster 

    disposable=float(new_data["Disposable_Income"].values[0])
    desired = float(new_data["Desired_Savings"].values[0])

    if disposable>desired:
        return {
            "Cluster": cluster_id,
            "Status": "✅ Already meeting savings goal",
            "Extra_Savings": float(disposable - desired)
        }
    
    shortfall = float(desired - disposable)
    suggestions = []
 
    for col in ["Eating_Out", "Entertainment", "Groceries", "Transport"]:
        if float(new_data[col].values[0]) > float(cluster_profile[col]):
            suggestions.append(f"Cut down {col}")
# 👉 If the cluster centroid (average for that cluster) has equal or larger spending than the user’s values, your condition > will never be true → suggestions = [].
# If no suggestions were added, suggest top 2 biggest expenses
    if not suggestions:
        top_expenses = new_data[["Eating_Out", "Entertainment", "Groceries", "Transport"]].T  #it make transpose  column value convert into row ->row=value
        top_expenses.columns = ["Amount"]
        top_expenses = top_expenses.sort_values("Amount", ascending=False)
        suggestions = [f"Cut down {cat}" for cat in top_expenses.head(2).index]



    return {
        "Cluster": int(cluster_id),
        "Status": "⚠️ Not meeting savings goal",
        "Shortfall": shortfall,
        "Suggestions": suggestions
    }     


new_user = pd.DataFrame([{
    "Eating_Out": 3000,
    "Entertainment": 2000,
    "Miscellaneous": 1500,
    "Groceries": 9000,
    "Transport": 4000,
    "Desired_Savings": 10000,
    "Disposable_Income": 6000
}])

r=recommend_savings(new_user,scal,kmm,cluster_profiles)

print(r)




#Learning (NOTE!!)
# When you send data (like API response) in JSON, Python has to turn objects into a string.
# The json module in Python only knows how to handle:
# int (normal Python int)
# float
# str
# bool
# list
# dict

# But not NumPy types.
# numpy.int, numpy.float, numpy.bool_, etc. come from NumPy’s internal type system.
# They usually appear when:

#.. When you create arrays with NumPy
#.. Even though you gave plain Python integers, pandas stores them as NumPy ints.
#.. When you do mathematical operations
# eg: mean() promotes the result to a numpy.float64.
#.. ML libraries (like scikit-learn, XGBoost, etc.) often return numpy.int64 or numpy.float32 instead of normal Python int or float.

# numpy data store into array