
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # it is used to create graph and plots
import seaborn as sns #it is used to more attractive and easier statistical graps

import nltk #NLTK (Natural Language Toolkit) used for text processing
from nltk.stem.porter import PorterStemmer #Stemming reduces words to their root form.
nltk.download('stopwords') #stopwords are common words that don't add meaning
from nltk.corpus import stopwords #loads the stopwords dataset
STOPWORDS = set(stopwords.words('english')) #creates a set of English stopwords

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler              #used to scale numerical features between 0 to 1
from sklearn.feature_extraction.text import CountVectorizer #used to convert text into numbers
from sklearn.model_selection import cross_val_score         #checks model performance by training multiple times on different splits
from sklearn.ensemble import RandomForestClassifier         #powerful classification algorithm
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay #tree like model
from sklearn.model_selection import GridSearchCV         #used to find best parameters for a model automatically
from sklearn.model_selection import StratifiedKFold  #used for stratified cross validation,ensures class distribution stays balanced in each fold
from sklearn.metrics import accuracy_score
from wordcloud import WordCloud                 #Creates a word cloud visualization.
from sklearn.tree import DecisionTreeClassifier #its tree like model
from xgboost import XGBClassifier #XGBoost is an advanced boosting algorithm
import pickle #used to save trained machine learning models
import re    #regular expression library and used for cleaning text

#Load the data

data = pd.read_csv(r"/content/amazon_alexa.tsv", delimiter = '\t', quoting = 3)  #Data is separeated by commas

print(f"Dataset shape : {data.shape}") #rows and cols ignore the quotation marks in the file

print(f"Feature names : {data.columns.values}")

#Check for null values

data.isnull().sum()

#Getting the record where 'verified_reviews' is null

data[data['verified_reviews'].isna() == True]  #if it finds rows where review text is missing(NULL)

#We will drop the null record

data.dropna(inplace=True)

print(f"Dataset shape after dropping null values : {data.shape}")
#Creating a new column 'length' that will contain the length of the string in 'verified_reviews' column

data['length'] = data['verified_reviews'].apply(len)
#Randomly checking for 10th record

print(f"'verified_reviews' column value: {data.iloc[10]['verified_reviews']}") #Original value
print(f"Length of review : {len(data.iloc[10]['verified_reviews'])}") #Length of review using len()
print(f"'length' column value : {data.iloc[10]['length']}") #Value of the column 'length'

#Distinct values of 'rating' and its count

print(f"Rating value count: \n{data['rating'].value_counts()}")
#Bar plot to visualize the total counts of each rating

data['rating'].value_counts().plot.bar(color = 'red')
plt.title('Rating distribution count')
plt.xlabel('Ratings')
plt.ylabel('Count')
plt.show()

#Finding the percentage distribution of each rating - we'll divide the number of records for each rating by total number of records

print(f"Rating value count - percentage distribution: \n{round(data['rating'].value_counts()/data.shape[0]*100,2)}") #value_counts → count of each rating

#data.shape[0] → total rows

fig = plt.figure(figsize=(7,7))

colors = ('red', 'green', 'blue','orange','yellow') #Each rating gets a color.

wp = {'linewidth':1, "edgecolor":'black'}  #Adds black border around pie slices.

tags = data['rating'].value_counts()/data.shape[0]  #Stores percentage distribution.

explode=(0.1,0.1,0.1,0.1,0.1) #This slightly separates slices from the center.

tags.plot(kind='pie', autopct="%1.1f%%", shadow=True, colors=colors, startangle=90, wedgeprops=wp, explode=explode, label='Percentage wise distrubution of rating') #separate slices ,start chart at 90,autopct show percentage

from io import  BytesIO  #Used for temporary memory storage.

graph = BytesIO() #Creates an in-memory file.

fig.savefig(graph, format="png")  #Saves the plot as a PNG image inside memory.


#Distinct values of 'feedback' and its count

print(f"Feedback value count: \n{data['feedback'].value_counts()}")

#Extracting the 'verified_reviews' value for one record with feedback = 0

review_0 = data[data['feedback'] == 0].iloc[1]['verified_reviews']
print(review_0)

#Extracting the 'verified_reviews' value for one record with feedback = 1

review_1 = data[data['feedback'] == 1].iloc[1]['verified_reviews']
print(review_1)


#Bar graph to visualize the total counts of each feedback

data['feedback'].value_counts().plot.bar(color = 'blue')
plt.title('Feedback distribution count')
plt.xlabel('Feedback')
plt.ylabel('Count')
plt.show()


#Finding the percentage distribution of each feedback - we'll divide the number of records for each feedback by total number of records

print(f"Feedback value count - percentage distribution: \n{round(data['feedback'].value_counts()/data.shape[0]*100,2)}")

fig = plt.figure(figsize=(7,7))

colors = ('red', 'green')

wp = {'linewidth':1, "edgecolor":'black'}

tags = data['feedback'].value_counts()/data.shape[0]

explode=(0.1,0.1)

tags.plot(kind='pie', autopct="%1.1f%%", shadow=True, colors=colors, startangle=90, wedgeprops=wp, explode=explode, label='Percentage wise distrubution of feedback')

#Feedback = 0
data[data['feedback'] == 0]['rating'].value_counts()

#Feedback = 1
data[data['feedback'] == 1]['rating'].value_counts()

#Distinct values of 'variation' and its count

print(f"Variation value count: \n{data['variation'].value_counts()}")

#Bar graph to visualize the total counts of each variation

data['variation'].value_counts().plot.bar(color = 'orange')
plt.title('Variation distribution count')
plt.xlabel('Variation')
plt.ylabel('Count')
plt.show()


#Finding the percentage distribution of each variation - we'll divide the number of records for each variation by total number of records

print(f"Variation value count - percentage distribution: \n{round(data['variation'].value_counts()/data.shape[0]*100,2)}")


data.groupby('variation')['rating'].mean()


data.groupby('variation')['rating'].mean().sort_values().plot.bar(color = 'brown', figsize=(11, 6))
plt.title("Mean rating according to variation")
plt.xlabel('Variation')
plt.ylabel('Mean rating')
plt.show()


data['length'].describe()

sns.histplot(data['length'],color='blue').set(title='Distribution of length of review ')


sns.histplot(data[data['feedback']==0]['length'],color='red').set(title='Distribution of length of review if feedback = 0')

sns.histplot(data[data['feedback']==1]['length'],color='green').set(title='Distribution of length of review if feedback = 1')
data.groupby('length')['rating'].mean().plot.hist(color = 'blue', figsize=(7, 6), bins = 20) #
plt.title(" Review length wise mean ratings")
plt.xlabel('ratings')
plt.ylabel('length')
plt.show()

cv = CountVectorizer(stop_words='english')
words = cv.fit_transform(data.verified_reviews)

# Combine all reviews
reviews = " ".join([review for review in data['verified_reviews']])

# Initialize wordcloud object
wc = WordCloud(background_color='white', max_words=50)

# Generate and plot wordcloud
plt.figure(figsize=(10,10))
plt.imshow(wc.generate(reviews))
plt.title('Wordcloud for all reviews', fontsize=10)
plt.axis('off')
plt.show()



# Combine all reviews for each feedback category and splitting them into individual words
neg_reviews = " ".join([review for review in data[data['feedback'] == 0]['verified_reviews']])
neg_reviews = neg_reviews.lower().split()

pos_reviews = " ".join([review for review in data[data['feedback'] == 1]['verified_reviews']])
pos_reviews = pos_reviews.lower().split()

#Finding words from reviews which are present in that feedback category only
unique_negative = [x for x in neg_reviews if x not in pos_reviews]
unique_negative = " ".join(unique_negative)

unique_positive = [x for x in pos_reviews if x not in neg_reviews]
unique_positive = " ".join(unique_positive)

wc = WordCloud(background_color='white', max_words=50)

# Generate and plot wordcloud
plt.figure(figsize=(10,10))
plt.imshow(wc.generate(unique_negative))
plt.title('Wordcloud for negative reviews', fontsize=10)
plt.axis('off')
plt.show()
wc = WordCloud(background_color='white', max_words=50)

# Generate and plot wordcloud
plt.figure(figsize=(10,10))
plt.imshow(wc.generate(unique_positive))
plt.title('Wordcloud for positive reviews', fontsize=10)
plt.axis('off')
plt.show()

corpus = []
stemmer = PorterStemmer()
for i in range(0, data.shape[0]):
  review = re.sub('[^a-zA-Z]', ' ', data.iloc[i]['verified_reviews'])
  review = review.lower().split()
  review = [stemmer.stem(word) for word in review if not word in STOPWORDS]
  review = ' '.join(review)
  corpus.append(review)

  cv = CountVectorizer(max_features = 2500)

#Storing independent and dependent variables in X and y
X = cv.fit_transform(corpus).toarray()
y = data['feedback'].values

#Saving the Count Vectorizer
pickle.dump(cv, open('/content/countVectorizer.pkl', 'wb'))
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 15)

print(f"X train: {X_train.shape}")
print(f"y train: {y_train.shape}")
print(f"X test: {X_test.shape}")
print(f"y test: {y_test.shape}")

print(f"X train max value: {X_train.max()}")
print(f"X test max value: {X_test.max()}")

scaler = MinMaxScaler()

X_train_scl = scaler.fit_transform(X_train)
X_test_scl = scaler.transform(X_test)

#Saving the scaler model
pickle.dump(scaler, open('/content/scaler.pkl', 'wb'))

#Fitting scaled X_train and y_train on Random Forest Classifier
model_rf = RandomForestClassifier()
model_rf.fit(X_train_scl, y_train)

print("Training Accuracy :", model_rf.score(X_train_scl, y_train))
print("Testing Accuracy :", model_rf.score(X_test_scl, y_test))

#Predicting on the test set
y_preds = model_rf.predict(X_test_scl)

#Confusion Matrix
cm = confusion_matrix(y_test, y_preds)
cm_display = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=model_rf.classes_)
cm_display.plot()
plt.show()

accuracies = cross_val_score(estimator = model_rf, X = X_train_scl, y = y_train, cv = 10)

print("Accuracy :", accuracies.mean())
print("Standard Variance :", accuracies.std())


params = {
    'bootstrap': [True],
    'max_depth': [80, 100],
    'min_samples_split': [8, 12],
    'n_estimators': [100, 300]
}

#Getting the best parameters from the grid search


print("Best Parameter Combination : {}".format(grid_search.best_params_))

print("Cross validation mean accuracy on train set : {}".format(grid_search.cv_results_['mean_train_score'].mean()*100))
print("Cross validation mean accuracy on test set : {}".format(grid_search.cv_results_['mean_test_score'].mean()*100))
print("Accuracy score for test set :", accuracy_score(y_test, y_preds))

model_xgb = XGBClassifier()
model_xgb.fit(X_train_scl, y_train)


#Accuracy of the model on training and testing data

print("Training Accuracy :", model_xgb.score(X_train_scl, y_train))
print("Testing Accuracy :", model_xgb.score(X_test_scl, y_test))

y_preds = model_xgb.predict(X_test)

#Confusion Matrix
cm = confusion_matrix(y_test, y_preds)
print(cm)
cm_display = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=model_xgb.classes_)
cm_display.plot()
plt.show()
#Saving the XGBoost classifier
pickle.dump(model_xgb, open('/content/model_xgb.pkl', 'wb'))

model_dt = DecisionTreeClassifier()
model_dt.fit(X_train_scl, y_train)

#Accuracy of the model on training and testing data

print("Training Accuracy :", model_dt.score(X_train_scl, y_train))
print("Testing Accuracy :", model_dt.score(X_test
_scl, y_test))
y_preds = model_dt.predict(X_test)

#Confusion Matrix
cm = confusion_matrix(y_test, y_preds)
print(cm)
