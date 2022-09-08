from tqdm import tqdm #to check times
import re #for regex
import nltk #for natural language tools
import string #for string manipulations
from nltk.tokenize import word_tokenize #to extract words from the corpus
from nltk.corpus import stopwords #to remove stopwords later for the cleaning and model training
punct = string.punctuation + '«»' + '``' #adding punctuation that is not present in the predefined list

def read_lines_from_big_file(path): #to deal with huge files such as our corpus
    with open(path, 'r', encoding='latin-1') as fp:
        for line in tqdm(fp): #each line is a context, that's how the corpus has been devised, so we iterate over each
            if len(line) > 1: #if it's longer than 1 word
                parts = word_tokenize(line) #tokenize it
                yield parts #give the tokenized object


i=0 #set counter to 1 so we can name the context files later correctly
for split_line in tqdm(read_lines_from_big_file('.../itwac_corpus.txt')):
    if 'CURRENT' not in split_line: #take away those lines with "CURRENT LINK" in it, so that we only get the contexts, not the 'dividers'
        tmp = [re.sub(r'n\'t|http\S+|\n|www\S+|\S*\d+\S*', '', x.strip(punct).lower()) for x in split_line] #remove negation contraction, websites, words with numbers in them
        clean = [x for x in tmp
            if x not in stopwords.words('english') #remove stopwords
                and x != " " #remove empty spaces
                and x not in punct #remove punctuation
                and len(x) > 1 #only take words that are longer than one word (remove random letters)
        ]
        with open(f"..../contexts_ukwac/context_{i}.txt", "w", "w") as f: #this is to create the file text for the context, which we'll put in a contexts file to later retrieve from there contexts in which a stimulus appears
            f.write(" ".join(clean))