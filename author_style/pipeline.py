from sklearn.compose import ColumnTransformer
from author_style.preprocessing import *
from sklearn.naive_bayes import MultinomialNB, TfidfVectorizer()



column_trans = ColumnTransformer([('vec', TfidfVectorizer(), 'text')],
                                 remainder='passthrough')

X_combined = column_trans.fit_transform(df[['text']])



y = df["author"]

nb_model = MultinomialNB()
nb_model.fit(X, y)
nb_model.score(X, y)
