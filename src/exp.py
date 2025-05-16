import csv
import os
import random
import datetime
from config.config import Config

class Exp:
   def __init__(self, the_gui):
      self.the_gui = the_gui #shows the info on screen
      self.participant_id = None 
      self.instruction_list = None
      self.stimulus_list = None
      self.familiarization_list = None # words actually contained in list
      self.data_list = []
      
      self.create_participant_id()
      self.create_instruction_list()
      self.create_stimuli_lists()
      self.run_experiment() 

   def create_participant_id(self):
      current_datetime = datetime.datetime.now() #to get current time
      formatted_dateline = current_datetime.strftime("%Y%m%d%H%M%S%f")
      random_number = random.randint(1000, 9999) #random six digit number 
      self.participant_id = f"{formatted_dateline}_{random_number}"

   def create_instruction_list(self):
      self.instruction_list = []  # create the empty list
      current_condition = Config.condition # get the current condition (word or image) from the config file
      instruction_filename = Config.instruction_file_path_list[current_condition]  # get file path from config file

      with open(instruction_filename, 'r') as file:  # open the instruction file in read mode
         for line in file:  # for each line in the file
            line = line.strip('\n')  # strip off the newlines from each line in the file
            line = line.replace(".", ".\n")  # replace every period in the current line with a period followed by \n
            self.instruction_list.append(line) # add the string to the instruction list

   def create_stimuli_lists(self):
      self.create_full_stimulus_list()
          # self.create_familiarization_list()  ← REMOVE THIS LINE
      self.create_test_list()
      random.shuffle(self.familiarization_list)
      random.shuffle(self.test_list)


   def create_full_stimulus_list(self):
      base_path = 'stimuli/images'
      self.full_stimulus_list = []
      folder_list = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

       # Randomly pick a folder
      chosen_folder = random.choice(folder_list)
      full_folder_path = os.path.join(base_path, chosen_folder)

       # Get all .png files
      all_images = [f for f in os.listdir(full_folder_path) if f.endswith('.png') and not f.startswith(".")]

       # Shuffle and pick familiarization images
      random.shuffle(all_images)
      self.familiarization_list = [os.path.splitext(f)[0] for f in all_images[:Config.num_familiarization_trials]]

       # Save the unused images from the same folder
      self.remaining_images = [os.path.splitext(f)[0] for f in all_images[Config.num_familiarization_trials:]]

       # Save full path prefix for use in preload_images
      self.chosen_folder_path = full_folder_path

       # If using images, preload just the ones we'll need
      if Config.condition == 1:
         all_to_preload = self.familiarization_list + self.remaining_images
         self.the_gui.preload_images(all_to_preload, folder=self.chosen_folder_path)

   def create_test_list(self):
      num_old_test_trials = Config.num_test_trials // 2
      num_new_test_trials = Config.num_test_trials - num_old_test_trials

    # Take old from familiarization list
      old_items = random.sample(self.familiarization_list, min(num_old_test_trials, len(self.familiarization_list)))

    # Take new from remaining images
      new_items = random.sample(self.remaining_images, min(num_new_test_trials, len(self.remaining_images)))

      self.test_list = old_items + new_items
      random.shuffle(self.test_list)



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

      self.show_total_wrong_responses()

      self.the_gui.root.destroy()


   def present_stimulus_list(self, stimulus_list, key_list, record_data):
      for stimulus_name in stimulus_list:
         key_pressed, rt = self.the_gui.show_stimulus(stimulus_name, key_list)
         confidence = None
         if record_data:
            confidence = self.the_gui.show_confidence_prompt() 
            trial_data = [stimulus_name, key_pressed, rt, confidence]
            self.data_list.append(trial_data)   

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
                                "rt",
                                "confidence"])

        # now we need to go through each trial, and create a list with those 8 items listed above
      for i, trial_data in enumerate(self.data_list):  # for each trial in self.data_list

         final_trial_data = []

         final_trial_data.append(self.participant_id)
         final_trial_data.append("words" if Config.condition == 0 else "images")
         final_trial_data.append(i + 1)
         final_trial_data.append(trial_data[0])

         old_or_new = "old" if trial_data[0] in self.familiarization_list else "new"
         final_trial_data.append(old_or_new)

         final_trial_data.append(trial_data[1])

         if old_or_new == "old":
            correct = 1 if trial_data[1] == "u" else 0
         else:
            correct = 1 if trial_data[1] == "i" else 0
         final_trial_data.append(correct)

         final_trial_data.append(trial_data[2])  # reaction time

         final_trial_data.append(trial_data[3])  # ✅ confidence rating

         final_data_list.append(final_trial_data)


        # create a file with the participant's id number as the file_name, ending with .csv
         filename = f'data/{self.participant_id}.csv'

        # use the csv module to write the full list of lists to the file
         with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(final_data_list)
   
   def show_total_wrong_responses(self):
      import csv

      filename = f"data/{self.participant_id}.csv"
      total_wrong = 0

      with open(filename, "r") as file:
         reader = csv.DictReader(file)
         for row in reader:
            if row.get("correct") == "0":
               total_wrong += 1

      print(f"Here is the total amount of words you got incorrect: {total_wrong}")

