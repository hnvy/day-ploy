# This is an open-source SuperMemo Plan alternative
# To learn more about SuperMemo Plan, please visit: https://help.supermemo.org/wiki/Plan
# The program is still a massive work-in-progress. If you would like to contribute, then please do so!
# You can fork this project and build something pretty :).
# Not sure what you should be aiming for? Read [[this guide][https://drive.google.com/folderview?id=11RUZw8MVdKXdb8HpuYR5epiktKPhkoOO]] to
# find out about how the original SuperMemo Plan is supposed to work. Then simply transform
# those concepts into Python letters and numbers to bring it to life.
# Feel free to contact me if you get stuck, I will be more than happy to help!
# The program is pretty easy to use:
## - Enter the list of the activities which you want to do today
## - Enter the desired number of minutes which you would like to spend on each of these activities
## - Let the program give you a more realistic number of minutes for each of your activities

# * Start

import datetime
from datetime import datetime
from datetime import timedelta
import json
import os
import sys
'''
import winsound # This is a good library to use in order to create a lightweight alarm clock. Perhaps use something like this:
start_time = "13:00"
start_time_stripped = datetime.strptime(start_time, "%H:%M")
start_time_formatted = datetime.strftime(start_time_stripped, "%H:%M")
while True: # This consumes a lot of CPU, and is therefore not resource-friendly
  if start_time_formatted == datetime.strftime(datetime.now(), "%H:%M"):
  winsound.Beep(1000,1000)
  print("timer!")
  break
'''

# * Initialise

data_file = os.path.join(sys.path[0],'data.txt') # This sets data_file variable to the location of data.txt (to speed up the process of pointing to the file)

daily_mins = 16*60 # TODO Let the user pick an time sleep in order to calculate the day duration

with open(data_file, 'r') as json_file: # Opens up data.txt as json_file in read mode
    activity_obj = json.load(json_file) # Loads the JSON file and assigns it to the variable activity_obj
    fixed = activity_obj["fixed"]
    rigid = activity_obj["rigid"]
    start_time = activity_obj["start_time"]
    name = activity_obj["name"]
    length = activity_obj["length"]
    ActLen = activity_obj["ActLen"]

# * Main

def adding(): # This function is for adding a new activity to the program
    with open(data_file, 'w') as json_file: # Opens up data.txt as json_file in write mode
        while True: # This is a loop which keeps asking the user to enter the activity name and desired number of minutes
            activity_name_input = input("Enter the activity name (type . to exit): ") # Asks the user to enter the activity name

            if activity_name_input == ".": # If the user enters ".", the program will exit this loop
                break
            else:
                length_input = int(input("Enter the number of goal number of desired minutes: ")) # This variable holds the desired number of minutes which the user will supply

            fixed.append("-") # TODO This writes "-" in the fixed field in data.txt. I need to use this later when creating the fixed feature.
            rigid.append("-") # TODO This writes "-" in the rigid field in data.txt. I need to use this later when creating the rigid feature.
            start_time.append("09:42") # This writes the default start time (09:42)
            name.append(activity_name_input) # Same thing as above but for a new variable
            length.append(length_input) # Same thing as above but for a new variable
            ActLen.append(0) # Same thing as above but for a new variable
            json.dump(activity_obj, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects


def view_and_update(): # This function refreshes the columns
    global fixed, rigid, start_time, name, length, ActLen, start_time_input # TODO This globalises the variables so that they can be used in this function. I need to understand why this is needed.

    with open(data_file, 'w') as json_file: # Opens up data.txt as json_file
        start_time_q = input("Do you want to enter a new start time?\n1. Yes\n2. No, set the start time to default (09:42)\n3. Do nothing (you MUST put a start time if this is your first time running the program)\n") # This asks the user whether or not they want to put a new start time
        if start_time_q == "1":
            start_time_input = input("Enter the start time in the format HH:MM: ")
        elif start_time_q == "2":
            start_time_input = "09:42"
        else:
            pass

        list_length = len(name) # This calculates the number of activities in our JSON file (data.txt)

        length_column_total = 0 # This sets the length_column_total to 1, because, otherwise, we will end up dividing by zero (see the definition of ratio_multiplier to understand what I mean)

        for p in range(0,list_length): # This is the loop which will go around the list of activities
            length_column_total += length[p] # This will add the length supplied by the user to the length_column_total

        start_time[0] = start_time_input # TODO This sets the start time of the first activity to whatever the user has chosen. I need to understand WHY this works (I must admit that I accidently got it to work...)

        if length_column_total <= 0: # Just in case the step above has resulted in a negative number or zero...  Maybe making length_column_total = 1 previously is not needed after all.
            length_column_total = 1 # This sets the length_column_total to 1, because, otherwise, we will end up dividing by zero (see the definition of ratio_multiplier to understand what I mean).

        ratio_multiplier = int(daily_mins/length_column_total) # The ratio_multiplier is what we are going to use in order to work out the actual length (ActLen). ActLen is basically the desired length * ratio_multiplier.

        for i in range(0,list_length): # This is the loop which will go around the list of activities

            start_time_format = datetime.strptime(start_time[i], "%H:%M") # This formats the start_time from a string to a proper time. It uses HH:MM format
            ActLen[i] = int(ratio_multiplier * length[i]) # This calculates the actual length for each of the activities

            new_start_time = start_time_format + timedelta(minutes=ActLen[i]) # This will calculate the start time of each of the activities. It basically takes the start_time and adds the corresponding ActLen to it
            new_start_time_format = datetime.strftime(new_start_time, "%H:%M") # This formats the new_start_time into HH:MM

            if i+1 >= list_length: # This prevents the program from giving an error. The error arises because the program will loop, and loop, and loop until eventually there are no more activities to go over.
                break # Stops the program
            else:
                start_time[i+1] = new_start_time_format # Writes the start time of each activity

        json.dump(activity_obj, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects

        print("===================================================================")
        pretty_fmt = "{:<5} {:<5} {:<5} {:<15} {:<10} {:<10} {:<10}" # I've borrowed this idea from kpence (https://github.com/kpence/day-ploy). It basically creates a nice table for us to use
        print (pretty_fmt.format("I", "Fixed", "Rigid", "Start time", "Activity", "Length", "ActLen")) # Prints the column titles
        for x in range(0,list_length): # Loops over data.txt to print each of the values
            print(pretty_fmt.format(f"{x}", fixed[x], rigid[x], start_time[x], name[x], length[x], ActLen[x]))
        print("===================================================================\n")


# * Run, run, run, RUN!
while True: # A simple loop to make the program continuous
    repeat = input("What do you want to do?\n1. Add activity\n2. Delete activity\n3. View current activity list\n")

    if repeat == "1":
        adding()
        view_and_update()

    elif repeat == "2":
        list_of_stats = [fixed,rigid,start_time,name,length,ActLen] # Essentially, this list-ifies the data.txt content, and therefore we are able to loop around the file
        activity_number = int(input("Enter the INDEX of the activity which you want to delete: "))

        if len(name) == 1:
            activitys_dict = {"fixed": [],"rigid": [],"start_time": [],"name": [],"length": [],"ActLen": []} # This resets the entire data.txt file if there is only one activity remaining which needs to be deleted
            with open(data_file, 'w') as json_file:
                json.dump(activitys_dict, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects

        else:
            for l in list_of_stats: # This loops around list_of_stats and deletes the corresponding activity number (which was entered by the user)
                del l[activity_number]

    elif repeat == "3":
        view_and_update()

    else:
        break
