import os #to work with directories
from multiprocessing import Pool #to speed up
import random #for selection of random 100k contexts

stimuli = [x for x in os.listdir(".../contexts_of_database_stimuli")] #make a list of stimuli from the contexts we made

def shrink(stimulus): #defining a function that will take a random 100k contexts for those words that have more contexts than that
    stimulus_path = f".../contexts_of_database_stimuli/{stimulus}" #path to the stimulus where the contexts are stored
    stimulus_dir = os.listdir(stimulus_path) #list of contexts
    if len(stimolo_dir) > 100000: #if there are more than 100k contexts in the stimulus folder
        random_file_lst = [] #create an empty random file list where we'll later put the names of the randomly selected 100k contexts
        i=0 #set the counter to 0, and we'll increase it each time we select a random context file
        while i < 100000: #while i is less than 100k (at 100k we stop)
            random_file=random.choice(stimulus_dir) #choose a random context file in the stimulus 
            if random_file not in random_file_lst: #if the randomly selected context file is not in the random files list
                random_file_lst.append(random_file) #append the randomly selected context file to the random files list
                i+=1 #increase the count by one, so that we get closer to the 100k files
            else: #if the randomly selected context files is already in the random files list
                continue #we don't want it twice, so we just go back to the while loop without increasing the count by 1
        for file in stimulus_dir: #for each context file in the stimulus directory
                file_os = os.path.join(stimulus_path, file) #join path and file name
                if file not in random_file_lst: #if the context file name is not in the randomly selected 100k list
                    os.remove(file_os) #remove that context file, so then in the folder we're left only with the 100k contexts that were randomly selected
        print(stimulus + " shrinked") #printing it to the terminal just to check progress

if __name__ == "__main__": #run the function using several CPUs for speeding up performance
    p = Pool(80)

    # map list to target function
    p.map(shrink, stimuli) #this applies the shrink function recursively to all the stimuli 