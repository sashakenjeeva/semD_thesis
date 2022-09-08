from tqdm import tqdm #to monitor time progress
import os #to interact with directories
from numpy import log #to apply log to semD
import sklearn 
from sklearn import metrics #for calculating cosine similarity
import numpy as np #for taking mean of cosine similarities
import gensim 
from gensim.models import KeyedVectors, Word2Vec #for loading the model
import statistics #for calculation of mean
import pandas #to integrate data from database

vecs=KeyedVectors.load_word2vec_format(".../GoogleNews-vectors-negative300.bin.gz", binary=True) #loading the google word2vec model

print("loaded model") #just to see progress in the terminal (this model takes less than the itwac to load, but still a few minutes)

stimuli = [x for x in os.listdir(".../contexts_of_database_stimuli")] #make a list of stimuli from the contexts we made

dict_database={}

def sem_d(word):
    '''A function that takes a word and returns its semantic diversity, 
    mean length of contexts in which it appears, and number of contexts 
    in which it appears'''
    vector_doc_list = [] #empty list that we'll populate with vector representations of the contexts in which the word appears
    len_list = [] #empty list that we'll populate with the lengths of context files in which a word appears
    perc_model = [] #empty list that we'll populate with mean number of words in the document present in the google w2v model
    if word in os.listdir(f".../contexts_of_database_stimuli"): #check if the word has a folder with its contexts
        word_dir = os.listdir(f".../contexts_of_database_stimuli/{word}") #make list of its contexts
        for context in tqdm(word_dir): #for each context file
            vector_list=[] #empty list that we'll populate with vectors for each word in the context document
            i=0 #set counter
            context_os = f".../contexts_of_database_stimuli/{word}/{context}" #path to the context file
            with open(context_os, encoding="utf-8") as f: #open the context file
                read = f.read().split("\n") #read and make the context into a list of words it contains
                len_cont = len(read) #length of the context, in order to later calculate the mean of all the lengths of the contexts in which a word appears
                len_list.append(len_cont) #append the length to the empty list
                for word in read: #for each word in the context list
                    try: #if it's in the word2vec model
                        vector = vecs[word] #take the vector of that word
                        vector_list.append(vector) #append the vector of the word to the list of word vectors
                        i+=1 #add count if the word is in the model
                    except KeyError: #if the word is not in the model
                        continue #just continue with the loop
            perc=(i*100)/len(read) #percentage of words present in the model
            perc_model.append(perc) #append it to the list of percentages to later take the mean
            vector_doc = np.mean(vector_list, axis=0) #give the document a vector representation by averaging out the vectors of the context words that we collected earlier
            vector_doc_list.append(vector_doc) #append the document vector representation to the document vector list, which we'll use later to calculate cosine similarity and thus semantic diversity
        mean_len = statistics.mean(len_list) #mean length of contexts in which the word appears
        cos = sklearn.metrics.pairwise.cosine_similarity(vector_doc_list) #calculates pairwise cosine similarity between all the vectors of contexts in which a word appears
        np.fill_diagonal(cos,0) #since the output of the sklearn pairwise cos similarity function repeats similarities and also includes self-similarity, we fill the diagonal with 0, thus removing self-similarities
        length=len(cos) #taking the length of the array
        mean_cos=(np.mean(cos))*(length/(length-1)) #calculating the numpy mean of the numpy array of cosine similarities, but manipulating the mean so that we get rid of influence of zero
        sem_d=log(mean_cos)*-1 #semD calculation following Hoffman
        dict_database[word] = [sem_d, len(vector_doc_list), mean_len, mean_perc_model] #adding the word entry to the dictionary, with a list of the following values: sem_d, contextual numerosity (how many documents), mean length of contexts, mean percentage of words present in the model

if __name__ == "__main__":
    p = Pool(15) #15 workers to speed up the process

    # map list to target function
    p.map(sem_d, database_stimuli)


word_prevalence=pandas.read_csv(".../word_prevalence.csv", encoding='latin-1', sep=';') #the word prevalence csv file
word_prevalence_RT=dict(zip(word_prevalence.Lemma, word_prevalence.I_Mean_RT)) #make dictionary with lemmas as keys and RT as value
word_prevalence_RT={k:float(v.replace(",", ".")) for k,v in word_prevalence_RT.items()} #replace comma with dot for RTs to make it possible to be a float 

for k in dict_database.keys(): #for each word in our semd dictionary
    dict_database[k].append(word_prevalence_RT[k]) #append also the RT to the word

df = pandas.DataFrame.from_dict(sem_d_perc, orient="index") #make dataframe out of dictionary for csv exportation

df.to_csv(".../sem_d_database.csv") #export to csv

#maybe add concreteness here too? To decide










