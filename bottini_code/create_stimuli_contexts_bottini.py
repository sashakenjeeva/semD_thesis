from tqdm import tqdm #to monitor time progress
import os #to interact with directories
import pandas #to import the word prevalence data
from nltk.corpus import stopwords #to remove stopwords from the database
from multiprocessing import Pool #to speed up process
import shutil #to copy paste files from one folder to another

stimuli = [x for x in os.listdir(".../contexts_of_bottini_stimuli.txt")] #take the stimuli 

contexts = os.listdir(".../contexts_itwac.txt") #list of context files that were extracted from the itwac corpus

for word in tqdm(stimuli): #for each word in the stimuli
    os.mkdir(f".../contexts_of_bottini_stimuli/{word}") #create a folder for that word, that we will later populate with contexts in which this word appears

def create_files(context): #
    '''function that checks if a word is in a context, and copies the context file into the word folder, if that's the case'''
    with open(f".../contexts_itwac/{context}") as f: #open context file
        str_context = f.read() #read the context file
        lst_context = str_context.split("\n") #make a list of words out of the file
        for x in stimuli: #for each word in Bottini's stimuli
            if x in lst_context: #if the word is in the list of words from the corpus
                shutil.copyfile(f".../contexts_itwac/{context}", f".../contexts_of_bottini_stimuli/{x}/{context}") #copy the context file from the itwac folder of contexts to the word folder

if __name__ == "__main__": #speeding up with multiprocessing
    p = Pool(80)

    # map list to target function
    p.map(create_files, contexts) #apply the create_files function to every context that we have in the itwac folder of contexts 
