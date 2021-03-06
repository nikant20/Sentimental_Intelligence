import os

from nltk.compat import xrange
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from pylab import *



if __name__ == '__main__':
    train = pd.read_csv("labeledTrainData.tsv", header=0, \
                        delimiter="\t", quoting=3)
    test = pd.read_csv("testData.tsv", header=0, delimiter="\t", \
                   quoting=3 )

    print ('The first review is:')
    print (train["review"][0])

    raw_input("Press Enter to continue...")


    print ('Download text data sets. If you already have NLTK datasets downloaded, just close the Python download window...')
    #nltk.download()  # Download text data sets, including stop words

    # Initialize an empty list to hold the clean reviews
    clean_train_reviews = []

    # Loop over each review; create an index i that goes from 0 to the length
    # of the movie review list

    print ("Cleaning and parsing the training set movie reviews...\n")
    for i in xrange( 0, len(train["review"])):
        clean_train_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(train["review"][i], True)))


    # ****** Create a bag of words from the training set
    #
    print ("Creating the bag of words...\n")


    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    # ******* Train a random forest using the bag of words
    #
    print ("Training the random forest (this may take a while)...")


    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit( train_data_features, train["sentiment"] )



    # Create an empty list and append the clean reviews one by one
    clean_test_reviews = []

    print ("Cleaning and parsing the test set movie reviews...\n")
    for i in xrange(0,len(test["review"])):
        clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test["review"][i], True)))

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    print ("Predicting test labels...\n")
    result = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe with an "id" column and
    # a "sentiment" column
    output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )

    # Use pandas to write the comma-separated output file
    output.to_csv('Bag_of_Words_model.csv', index=False, quoting=3)
    print ("Wrote results to Bag_of_Words_model.csv")

    # Reading sentiment column from Bag_of_Words_model.csv
    df = pd.read_csv("Bag_of_Words_model.csv", usecols=['sentiment'])

    # Counting the number of values
    counts = df['sentiment'].value_counts()

    # Printing the number of values
    print (counts)

    # Naming the labels in Pie Chart
    labels = 'Negative','Positive'

    # Giving colours to pie chart
    colors = ['lightcoral', 'lightskyblue']

    # Exploding the pie chart
    explode = (0.1, 0)

    # Plotting the values
    plt.pie(counts , labels=labels , explode=explode, colors=colors, shadow = True)

    # Creating the pie chart
    plt.axis('equal')

    # Showing the pie chart
    plt.show()


