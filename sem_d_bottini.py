from tqdm import tqdm #to monitor time progress
import os #to interact with directories
from numpy import log #to apply log to semD
import sklearn 
from sklearn import metrics #for calculating cosine similarity
import numpy as np #for taking mean of cosine similarities
import gensim 
from gensim.models import KeyedVectors, Word2Vec #for loading the model
import statistics #for calculation of mean
import pandas #to integrate data from Bottini

vecs=KeyedVectors.load_word2vec_format(".../word2vec.txt.gz", binary=False) #loading the itwac word2vec model

print("loaded model") #just to see progress in the terminal (this model takes around 15 minutes to load...)

with open(".../stimuli_bottini.txt", "r") as f: #open file that contains bottini's stimuli
    read=f.read()
    stimuli=read.split("\n") #make a list of stimuli

dict_bottini={}

def sem_d(word):
    '''A function that takes a word and returns its semantic diversity, 
    mean length of contexts in which it appears, and number of contexts 
    in which it appears'''
    vector_doc_list = [] #empty list that we'll populate with vector representations of the contexts in which the word appears
    len_list = [] #empty list that we'll populate with the lengths of context files in which a word appears
    if word in os.listdir(f".../contexts_of_bottini_stimuli/"): #check if the word has a folder with its contexts
        word_dir = os.listdir(f".../contexts_of_bottini_stimuli/{word}") #make list of its contexts
        for context in tqdm(word_dir): #for each context file
            vector_list=[] #empty list that we'll populate with vectors for each word in the context document
            context_os = f".../contexts_of_bottini_stimuli/{word}/{context}" #path to the context file
            with open(context_os, encoding="utf-8") as f: #open the context file
                read = f.read().split("\n") #read and make the context into a list of words it contains
                len_cont = len(read) #length of the context, in order to later calculate the mean of all the lengths of the contexts in which a word appears
                len_list.append(len_cont) #append the length to the empty list
                for word in read: #for each word in the context list
                    try: #if it's in the word2vec model
                        vector = vecs[word] #take the vector of that word
                        vector_list.append(vector) #append the vector of the word to the list of word vectors
                    except KeyError: #if the word is not in the model
                        continue #just continue with the loop
            vector_doc = np.mean(vector_list, axis=0) #give the document a vector representation by averaging out the vectors of the context words that we collected earlier
            vector_doc_list.append(vector_doc) #append the document vector representation to the document vector list, which we'll use later to calculate cosine similarity and thus semantic diversity
        mean_len = statistics.mean(len_list) #mean length of contexts in which the word appears
        cos = sklearn.metrics.pairwise.cosine_similarity(vector_doc_list) #calculates pairwise cosine similarity between all the vectors of contexts in which a word appears
        np.fill_diagonal(cos,0) #since the output of the sklearn pairwise cos similarity function repeats similarities and also includes self-similarity, we fill the diagonal with 0, thus removing self-similarities
        length=len(cos) #taking the length of the array
        mean_cos=(np.mean(cos))*(length/(length-1)) #calculating the numpy mean of the numpy array of cosine similarities, but manipulating the mean so that we get rid of influence of zero
        sem_d=log(mean_cos)*-1 #semD calculation following Hoffman
        dict_bottini[word] = [sem_d, len(vector_doc_list), mean_len] #adding the word entry to the dictionary, with a list of the following values: sem_d, contextual numerosity (how many documents), mean length of contexts


for stimulus in tqdm(stimuli): #for each stimulus in Bottini's stimuli
    sem_d(stimulus) #plug in the stimulus in the sem_d function, so that at the end we have the dictionary with scores for all the stimuli

col_list = ["Stimulus","Type"] #pre-enter the list of columns
type_words=pandas.read_csv(".../all_runs_no_pw.csv", sep=';', usecols=col_list) #read Bottini's csv
type_words = type_words.drop_duplicates("Stimulus") #remove duplicates
df=type_words[~type_words.Type.str.contains('pseudow')] #filter to have only real words
stim_dict=dict(zip(df.Stimulus, df.Type)) #dictionary that has as keys the stimuli and as values the concreteness label (vis/multi/abs)

for k in dict_bottini.keys(): #for each stimulus in the dictionary
    dict_bottini[k].append(stim_dict[k]) #append to the list of values the concreteness label

df = pandas.DataFrame.from_dict(dict_bottini, orient="index") #making a dataframe out of the dictionary

df.to_csv(".../sem_d_bottini.csv") #creating a csv file with all the information












