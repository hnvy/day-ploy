# This is an open-source SuperMemo Plan alternative
# To learn more about SuperMemo Plan, please visit: https://help.supermemo.org/wiki/Plan
# The program is pretty easy to use:
## Enter the list of the activities which you want to do today
## Enter the desired number of minutes which you would like to spend on each of these activities
## Let the program give you a more realistic number of minutes for each of your activities

# * Start

import datetime
from datetime import datetime
from datetime import timedelta
import json
import os
import sys
# import winsound # This is a good library to use in order to create a lightweight alarm clock

# * Initialise

data_file = os.path.join(sys.path[0],'data.txt') # This sets data_file variable to the location of data.txt (to speed up the process of pointing to the file)

daily_mins = 16*60 # TODO Let the user pick an time sleep in order to calculate the day duration
#start_time_input = "00:00" # TODO Let the user pick their own start time through the program. But, for now, modify this value in order to set the start time of your day (HH:MM)!

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
            task_name_input = input("Enter the task name (type . to exit): ") # Asks the user to enter the activity name
            if task_name_input == ".": # If the user enters ".", the program will exit this loop
                break
            else:
                length_input = int(input("Enter the number of goal number of desired minutes: ")) # This variable holds the desired number of minutes which the user will supply
            fixed.append("-") # TODO This writes "-" in the fixed field in data.txt. I need to use this later when creating the fixed feature.
            rigid.append("-") # TODO This writes "-" in the rigid field in data.txt. I need to use this later when creating the rigid feature.
            start_time.append("00:00") # This writes the start time which is supplied by the user in the start_time field in data.txt
            name.append(task_name_input) # Same thing as above but for a new variable
            length.append(length_input) # Same thing as above but for a new variable
            ActLen.append(0) # Same thing as above but for a new variable
            json.dump(activity_obj, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects

def view_and_update(): # This function refreshes the columns
    global fixed, rigid, start_time, name, length, ActLen, start_time_input # This globalises the variables so that they can be used in this function.

    with open(data_file, 'w') as json_file: # Opens up data.txt as json_file
        start_time_q = input("Do you want to enter a new start time?\n1. Yes\n2. No, set the start time to default (09:00)\n3. Do nothing (you MUST put a start time if this is your first time running the program)\n") # This asks the user whether or not they want to put a new start time
        if start_time_q == "1":
            start_time_input = input("Enter the start time in the format HH:MM: ")
        elif start_time_q == "2":
            start_time_input = "09:00"
        else:
            pass

        list_length = len(name) # This calculates the number of activities in our JSON file (data.txt)

        length_column_total = 0 # This sets the length_column_total to 1, because, otherwise, we will end up dividing by zero (see the definition of ratio_multiplier to understand what I mean)

        for p in range(0,list_length): # This is the loop which will go around the list of activities
            length_column_total += length[p] # This will add the length supplied by the user to the length_column_total

        start_time[0] = start_time_input

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
        pretty_fmt = "{:<5} {:<5} {:<15} {:<10} {:<10} {:<10}" # I've borrowed this idea from kpence (https://github.com/kpence/day-ploy). It basically creates a nice table for us to use
        print (pretty_fmt.format("Fixed", "Rigid", "Start time", "Activity", "Length", "ActLen")) # Prints the column titles
        for x in range(0,list_length): # Loops over data.txt to print each of the values
            print(pretty_fmt.format(fixed[x], rigid[x], start_time[x], name[x], length[x], ActLen[x]))
        print("===================================================================\n")

while True: # A simple loop to make the program continuous
    repeat = input("What do you want to do?\n1. Add tasks\n2. Delete tasks\n3. View current list\n")
    if repeat == "1":
        adding()
        view_and_update()
    elif repeat == "2":
        list_of_stats = [fixed,rigid,start_time,name,length,ActLen]
        task_number = int(input("Enter the INDEX of the task which you want to delete: "))
        if len(name) == 1:
            tasks_dict = {"fixed": [],"rigid": [],"start_time": [],"name": [],"length": [],"ActLen": [],}
            with open(data_file, 'w') as json_file:
                json.dump(tasks_dict, json_file, indent=1)
        else:
            for l in list_of_stats:
                del l[task_number]

    elif repeat == "3":
        view_and_update()
    else:
        break
