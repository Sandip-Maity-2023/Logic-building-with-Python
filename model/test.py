import numpy as np #library support for working with arrays,matrices,wide range of mathematical functions
import pandas as pd #library for data manipulation and analysis
from sklearn.model_selection import train_test_split #module for splitting data into training and testing sets
from sklearn.metrics import accuracy_score #module for evaluating the performance of machine learning models
from sklearn import svm #module for support vector machines
from sklearn.preprocessing import StandardScaler #module for standardizing features by removing the mean and scaling to unit variance
import streamlit as st #library for building web applications in Python
from PIL import Image




# load the diabetes dataset
diabetes_df = pd.read_csv('diabetes.csv')
print(diabetes_df.head()) # Display the first few rows of the dataset


# group the data by outcome to get a sense of the distribution
diabetes_mean_df = diabetes_df.groupby('Outcome').mean()

# split the data into input and target variables
X = diabetes_df.drop('Outcome', axis=1) # drop the target variable from the input data

y = diabetes_df['Outcome'] # target variable

# scale the input variables using StandardScaler
scaler = StandardScaler()
scaler.fit(X) # fit the scaler to the data
X = scaler.transform(X) # transform the data using the fitted scaler

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# create an SVM model with a linear kernel
model = svm.SVC(kernel='linear')

# train the model on the training set
model.fit(X_train, y_train)

# make predictions on the training and testing sets
train_y_pred = model.predict(X_train)
test_y_pred = model.predict(X_test)

# calculate the accuracy of the model on the training and testing sets
train_acc = accuracy_score(train_y_pred, y_train)
test_acc = accuracy_score(test_y_pred, y_test)

# create the Streamlit app
def app():

    img = Image.open(r"img.jpeg")
    img = img.resize((200,200)) # resize the image to 200x200 pixels
    st.title("Diabetes Prediction App")
    st.image(img,caption="Diabetes Image",width=200)


    st.title('Diabetes Prediction')

    # create the input form for the user to input new data
    st.sidebar.title('Input Features')

#Minimum Value (0): The smallest value the slider can select (here it represents 0 pregnancies).
#Maximum Value (17): The largest value the slider can select (here it represents 17 pregnancies).
#Default Value (3): The value the slider is initially set to when the application starts (here it represents 3 pregnancies).
    preg = st.sidebar.slider('Pregnancies', 0, 17, 3) # slider for number of pregnancies

    glucose = st.sidebar.slider('Glucose', 0, 199, 117) # slider for glucose level
    bp = st.sidebar.slider('Blood Pressure', 0, 122, 72) # slider for blood pressure
    skinthickness = st.sidebar.slider('Skin Thickness', 0, 99, 23) # slider for skin thickness
    insulin = st.sidebar.slider('Insulin', 0, 846, 30) # slider for insulin level
    bmi = st.sidebar.slider('BMI', 0.0, 67.1, 32.0) # slider for body mass index
    dpf = st.sidebar.slider('Diabetes Pedigree Function', 0.078, 2.42, 0.3725, 0.001) # slider for diabetes pedigree function
    age = st.sidebar.slider('Age', 21, 81, 29) # slider for age

    # make a prediction based on the user input
    input_data = [preg, glucose, bp, skinthickness, insulin, bmi, dpf, age] # create a list of input features
    input_data_nparray = np.asarray(input_data) # convert the list to a numpy array
    reshaped_input_data = input_data_nparray.reshape(1, -1) # reshape the array to match the input shape of the model
    prediction = model.predict(reshaped_input_data) # make a prediction using the model

    # display the prediction to the user
    st.write('Based on the input features, the model predicts:') # display the prediction message
    if prediction == 1: 
        st.warning('This person has diabetes.')
    else:
        st.success('This person does not have diabetes.')

    # display some summary statistics about the dataset
    st.header('Dataset Summary')
    st.write(diabetes_df.describe()) # display the summary statistics of the dataset

    st.header('Distribution by Outcome') # display the distribution of the dataset by outcome
    st.write(diabetes_mean_df) # display the mean values of the input features grouped by outcome

    # display the model accuracy
    st.header('Model Accuracy')
    st.write(f'Train set accuracy: {train_acc:.2f}') # display the training accuracy
    st.write(f'Test set accuracy: {test_acc:.2f}')  # display the testing accuracy
    st.write('The model was trained using a linear SVM algorithm.')

if __name__ == '__main__':
    app()

