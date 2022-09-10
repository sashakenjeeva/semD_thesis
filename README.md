These are the Python scripts I created to conduct my work for my Master's Thesis on semantic diversity and the concreteness advantage. Here is a quick guide to the directories I created and the scripts:

1. The code_bottini directory contains all the scripts used for calculations for Bottini et al.'s stimuli, specifically:

- itwac_contexts_cleaning_creating_model.py --> this is the script used to clean the itwac corpus, train the w2v model, and create all the context files
- create_stimuli_contexts_bottini.py --> this is the script used to compile the context files for each stimulus (so for each stimulus we create a directory and we populate it with contexts in which this stimulus was found)
- random_100k_bottini.py --> this is the script used to select random 100k contexts for those stimuli that had more than that
- sem_d_bottini.py --> finally, this is the script used to calculate sem_d (as well as cont_num), including the creation of the final csv file

2. The code_database directory is just the same, but applied to the English data:

- context_files_ukwac.py --> cleaning ukwac and creating the context files (no model training because we used a pretrained model here)
- create_stimuli_contexts_database.py --> making folders of stimuli with their contexts
- random_100k_database.py --> selecting random 100k contexts for stimuli that have more than that
- sem_d_database.py --> calculating sem_d & cont_num + creating csv file

Additionally, the file database_semD makes available the calculated semD scores for the Word Prevalence database (Brysbaert et al., 2014).
