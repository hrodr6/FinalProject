import csv
import os
import random
import datetime
import config.config
import Config
ftfcrtctrctyrcyt
class Exp: 
	def __init__(self, the_gui):
	   self.the_gui = the_gui #presents info on screen

	   self.participant_id = None #each participant will get a number
	   self.instruction_list = None #string containing data in the instruction file
	   self.full_stimulus_list = None
	   self.familiarization_list = None #the words presented that are the actual list
	   self.test_list = None #words presented which contain the false, or rather misleading word

		self.data_list = [] #list to keep track of data for each trial

		self.create_participant_id()
		self.create_instruction_list()
		self.create_stimulus_list()
		self.create_stimulus_list()
		self.run_experiment()

	def create_participant_id():
		current_datetime = datetime.datetime.now() #to get current time
		formatted_dateline = current_datetime.strftime("%Y%m%d%H%M%S%f")
		random_number = random.randint(100000, 999999) #random six digit number 
		self.participant_id = f"{formatted_datetime}_{random_number}"

	def create_instruction_list():
		self.create_full_stimulus_list()  # call a function to create the full stimulus list
        self.create_familiarization_list() # call a function to create the full stimulus list
        self.create_test_list() # call a function to create the full stimulus list
        random.shuffle(self.familiarization_list) # randomize the order of the stimuli
        random.shuffle(self.test_list) # randomize the order of the stimuli

	def create_stimulus_list():
		directory_list = os.listdir('stimuli/images/')  # get a list of all the files in the images directory
        self.full_stimulus_list = []  # create the empy stimulus list
        for thing in directory_list:  # loop through the list of files in the images directory
            if not thing.startswith("."):  # if the current item is not a hidden file (hidden files start with ".")
                self.full_stimulus_list.append(thing[:-4])  # append its name to the stimulus list, minus the file ending


        # if this experiment uses images, call the Gui's preload images method, passing it the list of stimulus names
        if Config.condition == 1:
            self.the_gui.preload_images(self.full_stimulus_list)


    def create_familiarization_list(self):
        random.shuffle(self.full_stimulus_list) # randomize the stimulus list

 		# select teh first num_familiarization_trials items from the randomized list
        self.familiarization_list = self.full_stimulus_list[:Config.num_familiarization_trials]


 	def create_test_list(self):
	# determine how many test trials should come from the familiarization list
        num_old_test_trials = Config.num_test_trials//2

        # get half of our test items from the familiarization list.
        # this is why we have to remember to shuffle the order of our familiarization and test lists in the
        # create_stimuli_lists() method, since we don't want the participant to experience the first half of the test
        # list as old items, or the first half of the familiarization list as test items
        self.test_list = self.familiarization_list[:num_old_test_trials]

        # to get our new items, we need to create an index corresponding to the num of fam trials, where we left off
        # when we took items from the full stimulus list when we generated the familiarization list
        start = Config.num_familiarization_trials

        # the position in the full stimulus list where we will stop drawing new stimuli for the test list
        stop = start + Config.num_test_trials//2

        # get the rest of our test list using those two indexes
        self.test_list += self.full_stimulus_list[start:stop]



	def run_experiment(self):
        self.the_gui.show_instructions(self.instruction_list[0], True)
        self.present_stimulus_list(self.familiarization_list, Config.familiarization_key_list, False)
        self.the_gui.show_instructions(self.instruction_list[1], False, Config.test_delay)
        self.the_gui.show_instructions(self.instruction_list[2], False)
        self.the_gui.show_instructions(self.instruction_list[3], False)
        self.the_gui.show_instructions(self.instruction_list[4], False)
        self.present_stimulus_list(self.test_list, Config.test_key_list, True)
        self.the_gui.show_instructions(self.instruction_list[5], True)
        self.save_data()
        self.the_gui.root.destroy()


	def present_stimulus_list(self, stimulus_list, key_list, record_data):
        for stimulus_name in stimulus_list:
            key_pressed, rt = self.the_gui.show_stimulus(stimulus_name, key_list)
            if record_data:
                trial_data = [stimulus_name, key_pressed, rt]
                self.data_list.append(trial_data)   
        final_data_list = [] # an empty list where we will put the combined data we aleady had plus the new data
    def save_data(self):
        final_data_list = [] # an empty list where we will put the combined data we aleady had plus the new data

        # insert a new list into our data_list, a list of strings specified what data is stored in each list element
        final_data_list.append(["participant_id",
                                "stimulus_type",
                                "trial_number",
                                "stimulus",
                                "old_or_new",
                                "response",
                                "correct",
                                "rt"])

        # now we need to go through each trial, and create a list with those 8 items listed above
        for i, trial_data in enumerate(self.data_list):  # for each trial in self.data_list

            final_trial_data = [] # create a new empty list for this trial
             # add the participant id to the trial
            final_trial_data.append(self.participant_id)

            # add "words" or "images" to this trial, depending on the value in the Config file specifying the condition
            if Config.condition == 0:
                final_trial_data.append("words")
            else:
                final_trial_data.append("images")

            # add the trial number to the trial data, starting count at 1 instead of 0
            final_trial_data.append(i+1)

            # add the current stimulus name to the trial data
            final_trial_data.append(trial_data[0])

            # add "old" or "new" depending on whether this test item was in the familiarization list
            if trial_data[0] in self.familiarization_list:
                old_or_new = "old"
            else:
                old_or_new = "new"
            final_trial_data.append(old_or_new)

            # add the key that was pressed
            final_trial_data.append(trial_data[1])

            # add whether the key that was pressed was the correct key
            if old_or_new == "old":
                if trial_data[1] == "j":
                    correct = 1
                else:
                    correct = 0
            else:
                if trial_data[1] == "k":
                    correct = 1
                else:
                    correct = 0
            final_trial_data.append(correct)

            # add the reaction time to the trial data
            final_trial_data.append(trial_data[2])

            # add the data for the current trial to the full final data list
            final_data_list.append(final_trial_data)

        # create a file with the participant's id number as the file_name, ending with .csv
        filename = f'data/{self.participant_id}.csv'

        # use the csv module to write the full list of lists to the file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(final_data_list)