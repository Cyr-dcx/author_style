from sklearn.naive_bayes import MultinomialNB
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from author_style.preprocessing import features
from sklearn.preprocessing import LabelEncoder
from author_style.utils import csv_to_dataframes
from sklearn.model_selection import train_test_split

df = csv_to_dataframes(output='p')
df = features(df)

#selection de X et y dans le dataframe df
X = df['preprocess_text','vocab_richness',
       "word_count", "unique_word_count",
       "sentences_count", "stopwords_count"]
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

#split date
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.33, random_state=42)

#model

nb_model = MultinomialNB()
model_trained = nb_model.fit(X_train, y_train)

print(model_trained.score(X_test, y_test))
