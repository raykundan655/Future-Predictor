import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


splits = {'train': 'train.csv', 'validation': 'validation.csv', 'test': 'test.csv'}
df = pd.read_csv("hf://datasets/jquigl/imdb-genres/" + splits['test'])

# print(df.shape)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
# print(df.head(2))

# print(df.info())

# print(df.columns)

# print(df.duplicated().sum())

# print(df.isnull().sum())

# print(df['movie title - year'].head(2))

df["year"]=df['movie title - year'].str.extract(r'(\d{4})')

df['movie_title']=df['movie title - year'].str.replace(r'-\s*\d{4}'," ",regex=True).str.strip()

df.drop(columns=['rating','movie title - year',"year"],inplace=True)

# print(df.head(2))

# print(df.isnull().sum())


# pd.set_option("display.max_columns",None)
# pd.set_option("display.width",200)
# print(df.head(2))

tfidf=TfidfVectorizer(stop_words="english")
#  makes a tool that converts text into useful numerical features for machine learning, while ignoring common English words.

tfidf_matrix=tfidf.fit_transform(df["expanded-genres"])

# --------------------------------------------
# Step 1: TF-IDF (turn text into vectors)
# TF 
# How often a word appears in a document (movie’s genres, description, etc).
# IDF
# How unique or rare the word is across the whole dataset.
# Common words (like the, and, of) → low weight
# Rare words (like sci-fi, thriller) → high weight

# You have expanded-genres column like:
# Movie A → "action adventure sci-fi"
# Movie B → "comedy romance"
# Movie C → "adventure comedy"

# TfidfVectorizer will:
# Collect all unique words across all movies. Example: ["action", "adventure", "sci", "comedy", "romance"]
# For each movie, make a row vector with TF-IDF values for those words.
# # Movie	  action	adventure	sci	comedy	romance
# # Movie A  	0.7	    0.5	         0.7    0	    0
# # Movie B	    0	     0	         0	    0.7	  0.7
# # Movie C     0	    0.7	         0	     0.7	0   #0 means that not appear into that rows
# IT create row value of all features based on dataset
# TfidfVectorizer gives you a sparse matrix->for make a dataframe-> df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out()  # Get feature names (words))

#  -----------------------------------------------

cosine_sim=cosine_similarity(tfidf_matrix,tfidf_matrix)

# It compares every movie vector with every other movie vector to measure how similar they are.
# Output = a square matrix (N_movies × N_movies).

# 	   Movie A	Movie B	Movie C
# Movie A	 1.0	0.0	     0.6     how movie A is similar to other moves
# Movie B	 0.0	1.0	     0.5
# Movie C	 0.6	0.5	     1.0

def recommend_movie(title,n=5):

    matched=df[df["movie_title"].str.lower()==title.lower()]
    # df[ ... ] → selects only the rows where the mask is True.

    if matched.empty:
        return {"error":f" Movie '{title}' not found in dataset!"}
    
    ind=matched.index[0]

    sim_score=list(enumerate(cosine_sim[ind]))

# enumerate(cosine_sim[idx])
# Pairs each similarity score with its index (movie ID).
# So instead of just scores, you get (index, score).

    sim_score=sorted(sim_score,key=lambda x:x[1],reverse=True)
    # key=lambda x:x[1]-> sorted based on score 

# Skip the first one (itself) and take top-n
    sim_score=sim_score[1:n+1]

    movie_index = [i[0] for i in sim_score]
    # i[0]->movie indexx that is similar 

    return  df["movie_title"].iloc[movie_index].tolist()
   
print(recommend_movie("Bin Badal Barsaat"))















