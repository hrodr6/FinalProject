Final Project Introduction


1. My Final Project will be a cognitive science experiment--similar to the Deese, Roediger and McDermott (DRM) task. It will be a false memory test. The participants will be given a set of words from a random list of semantically related words. They will be shown a list; each word presented for a the same amount of time. Then, the participants will be asked to respond to a set of random words, presented individually, were present in the list or not. A twist to this is that the participants will also rate their confidence level for each response on whether the word was present or not. It will count how many were correct and how many were false, and provide a percentage for false responses. Participants will also be explained what false memories are. A gap in false memory testing that I have seen in the research is the Confidence of answers and its relationship to False Memories. 

This is how my code is organized (which is taken from the experiment_13 we learned in class):
The experiment will be broken down into multiple python files and txt files. 
2.a. run_memory_test.py is the main python script that will be ran in the terminal. The function runs other python scripts in order to present words based on a random selection of the four folders provided with semantically-related words. 
2.b. The window which prompts the responses and shows the list of words is created from the gui.py. This uses tkinter to display the stimuli and to take the key responses from the participants. 
2.c. Another aspect of my code is config.py. This script is important because it defines many key aspects to the experiment that are constant. For example, this is where we define "u" and "i" to be the yes or no responses. 
2.d. exp.py is the knitty gritty of the logic of the code. This is where we put the code such as presenting the stimulus and saving the responses in the correct order! I use this file to randomize and to create the stimuli. I also import time into this python script in order to record reaction times relative to the responses provided.


3. The experiment will provide data for the response of the time, the individual confidence level for each response of whether or not they were originally presented. 

This project was worked on by myself only.

Sources: 
https://pmc.ncbi.nlm.nih.gov/articles/PMC5407674/ 
