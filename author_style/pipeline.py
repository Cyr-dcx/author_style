from sklearn.naive_bayes import MultinomialNB
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from author_style.preprocessing import features
from sklearn.preprocessing import LabelEncoder

df = features(df)

#selection de X et y dans le dataframe df
X = df.drop(["text","author"])
y = df["author"]

# Encode categorical variables
cat_transformer = LabelEncoder()
y = cat_transformer.fit_transform(y)

# transform X features
column_trans = ColumnTransformer(
    [('vec', TfidfVectorizer(), 'preprocess_text')], remainder='passthrough')

X_combined = column_trans.fit_transform(X[['preprocess_text','vocab_richness',
                                           "word_count", "unique_word_count",
                                           "sentences_count", "stopwords_count"]])

#model

nb_model = MultinomialNB()
nb_model.fit(X_combined, y)
