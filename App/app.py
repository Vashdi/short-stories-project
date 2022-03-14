import PyPDF2
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import json
import numpy as np

dirname = os.path.dirname(__file__)

def readFearWords():
    wordsFile = open(os.path.join(dirname,'words.txt'),'r')
    stringWords = wordsFile.read()

    # Converts string into lower case
    lowerCaseWords = stringWords.casefold()
    wordsWithoutCommas = lowerCaseWords.replace(",", " ")
    wordsList = wordsWithoutCommas.split()
    wordsSet = set(wordsList)
    return wordsSet


def readStoriesFromDirectory(directoryPath):

    # Get the list of all files in directory
    allStories = os.listdir(directoryPath)
    allStoriesText = ""
    for story in allStories:

        # creating a pdf file object
        pdfFileObj = open(directoryPath+"\\"+story, 'rb')
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for pageNumber in range(pdfReader.numPages):
            # creating a page object
            pageObj = pdfReader.getPage(pageNumber)

            # extracting text from page
            try:
                pageText = pageObj.extractText()
                # Converts string into lower case
                lowerCaseText = pageText.casefold()
                allStoriesText = allStoriesText + lowerCaseText
            except:
                continue
        # closing the pdf file object
        pdfFileObj.close()
    return allStoriesText

def countWordsInText(words, text):
    counter = 0
    wordsStatistics = {
    }
    for word in words:
        numberOfOccurrences = len([m.start() for m in re.finditer(word, text)])

        counter += numberOfOccurrences
        wordsStatistics[word] = numberOfOccurrences

    result = {
        "wordsStatistics": wordsStatistics,
        "numberOfOccurrencesInAllStories": counter
    }
    return result


def combineTwoSets(A,B):
    result = {
        "words": [],
        "ACount": [],
        "BCount": []
    }
    for word in A.keys():
        if abs(A[word] - B[word] > 2):
            result["words"].append(word)
            result["ACount"].append(A[word])
            result["BCount"].append(B[word])
    return result
        

def main():
    fearWords = readFearWords()
    allOldStoriesText = readStoriesFromDirectory(
        os.path.join(dirname, "old"))
    allModernStoriesText = readStoriesFromDirectory(
        os.path.join(dirname, "modern"))
    numberOfFearWordsInOldStories = countWordsInText(
        fearWords, allOldStoriesText)
    numberOfFearWordsInModernStories = countWordsInText(
        fearWords, allModernStoriesText)
    setOfWords = combineTwoSets(numberOfFearWordsInOldStories["wordsStatistics"],numberOfFearWordsInModernStories["wordsStatistics"])

    # Create a dataframe
    value1 = setOfWords["ACount"]
    value2 = setOfWords["BCount"]
    df = pd.DataFrame({'group': setOfWords["words"], 'value1':value1 , 'value2':value2 })
    
    # Reorder it following the values of the first value:
    ordered_df = df.sort_values(by='value1')
    print(range(1,len(df.index)+1))
    print(df.index)
    my_range=range(1,len(df.index)+1)
    
    # The horizontal plot is made using the hline function
    plt.hlines(y=my_range, xmin=ordered_df['value1'], xmax=ordered_df['value2'], color='grey', alpha=0.4)
    plt.scatter(ordered_df['value1'], my_range, color='skyblue', alpha=1, label='Old Stories')
    plt.scatter(ordered_df['value2'], my_range, color='green', alpha=0.4 , label='Modern Stories')
    plt.legend()
    
    # Add title and axis names
    plt.yticks(my_range, ordered_df['group'])
    plt.title("Comparison between Old and Modern stories", loc='center')
    plt.xlabel('Number of occurrences')
    plt.ylabel('Fear Words')

    # Show the graph
    plt.show()

    # Make a random dataset:
    height = [numberOfFearWordsInModernStories['numberOfOccurrencesInAllStories'], numberOfFearWordsInOldStories['numberOfOccurrencesInAllStories']]
    bars = ('Modern stories', 'Old stories')
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    plt.title("Total number of occurrences in Old and Modern stories", loc='center')
    plt.ylabel('Total number of occurrences')

    # Show graphic
    plt.show()



if __name__ == "__main__":
    main()
