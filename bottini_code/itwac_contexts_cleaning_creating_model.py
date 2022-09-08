from tqdm import tqdm #to check times
import re #for regex
import nltk #for natural language tools
import string #for string manipulations
from nltk.tokenize import word_tokenize #to extract words from the corpus
from nltk.corpus import stopwords #to remove stopwords later for the cleaning and model training
punct = string.punctuation + '«»' + '``' #adding punctuation that is not present in the predefined list
import gensim #for training
from gensim.models import Word2Vec #for training the model
from gensim.test.utils import get_tmpfile

def read_lines_from_big_file(path): #to deal with huge files such as our corpus
    with open(path, 'r', encoding='latin-1') as fp:
        for line in tqdm(fp): #each line is a context, that's how the corpus has been devised, so we iterate over each
            if len(line) > 1: #if it's longer than 1 word
                parts = word_tokenize(line) #tokenize it
                yield parts #give the tokenized object

contexts =[] #this is the list we'll populate with the contexts that we'll use to train the w2v model
i=0 #set counter to 1 so we can name the context files later correctly
for split_line in tqdm(read_lines_from_big_file('.../itwac_corpus.txt')):
    if 'CURRENT' not in split_line: #take away those lines with "CURRENT LINK" in it, so that we only get the contexts, not the 'dividers'
        tmp = [re.sub(r'\x93|\x94|\x92|l\'|un\'|http\S+|\d+|\n|www\S+', '', x.strip(punct).lower()) for x in split_line] #remove weird characters, articles, websites, numbers, newlines
        clean = [x for x in tmp
            if x not in stopwords.words('italian') #remove stopwords
                and x != " " #remove empty spaces
                and x not in punct #remove punctuation
                and len(x) > 1 #only take words that are longer than one word (remove random letters)
        ]
        contexts.append(clean) #append the cleaned context to the contexts list
        with open(f".../contexts_itwac/context_{i}.txt", "w") as f: #this is to create the file text for the context, which we'll put in a contexts file to later retrieve from there contexts in which a stimulus appears
            f.write("\n".join(clean))

model = Word2Vec(sentences=contexts, vector_size=200, window=5,min_count=1) #training model
model.save("word2vec.model") #saving the model
model = Word2Vec.load("word2vec.model") #loading the model
path = get_tmpfile(".../word2vec.model") #getting the file from where we saved it
model.wv.save_word2vec_format(".../word2vec.txt") #saving it in w2v format so it can be easily used later (and loaded with KeyedVectors)