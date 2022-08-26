'''
This is an open-source SuperMemo Plan alternative
To learn more about SuperMemo Plan, please visit: https://help.supermemo.org/wiki/Plan
The program is still a massive work-in-progress. If you would like to contribute, then please do so!
You can fork this project and build something pretty :).
Not sure what you should be aiming for? Read [[https://drive.google.com/folderview?id=11RUZw8MVdKXdb8HpuYR5epiktKPhkoOO][this guide]] to
find out about how the original SuperMemo Plan is supposed to work. Then simply transform
those concepts into Python letters and numbers to bring it to life.
Feel free to contact me if you get stuck, I will be more than happy to help!
The program is pretty easy to use:
- Enter the list of the activities which you want to do today
- Enter the desired number of minutes which you would like to spend on each of these activities
- Let the program give you a more realistic number of minutes for each of your activities
'''

# * Start

import datetime
from datetime import datetime, timedelta
import json
import os
import sys


# * Initialise

data_file = os.path.join(sys.path[0],'data.txt') # This sets data_file variable to the location of data.txt (to speed up the process of pointing to the file)
												 # TODO let the user choose the file name. You might want to use something like this? https://www.py4e.com/html3/07-files.

time_file = os.path.join(sys.path[0],'time.txt') # This sets time_file variable to the location of time.txt (this file contains the current work hours which the user has chosen)

# Function that helps us append "$$END$$" to the end of the activity list
def end_appender():
	fixed.append("-")
	rigid.append("R")
	start_time.append("00:00")
	name.append("$$END$$")
	length.append(0)
	ActLen.append(0)


# Function that adds let's us decide whether or not we want to delete the last activity on the list (which must be "$$END$$")
def the_end(deletion=True): # Normally, if we call this function, it will delete the preceding activity

	if not list_length: # If data.txt doesn't have anything in it, nothing will happen
		return

	elif (deletion == False) or (name[-1] != "$$END$$"): # If these conditions are met, then there will be no deletion of the previous activity (otherwise, we will end up deleting the actual user activity rather than "$$END$$")
		end_appender() # Calls the end_appender() function

	elif deletion == "start of adding": # If this condition is met, then deletion WILL take place (because we know for sure that the last activity on that list is "$$END$$")
		for l in list_of_stats: # Loops around list_of_stats, and deletes the "$$END$$" activity
			del l[-1] # "-1" denotes the last activity in the list

	elif deletion == True: # If this condition is met, then deletion WILL take place (because we know for sure that the last activity on that list is "$$END$$")
		for l in list_of_stats: # Loops around list_of_stats, and deletes the "$$END$$" activity
			del l[-1] # "-1" denotes the last activity in the list
		# Now we have to write out a new "$$END$$" activity at the end of the activity list
		end_appender() # Calls the end_appender() function


# This is a file validator function which checks whether or not data.txt is in the correct format
def validator():
	global activity_obj, fixed, rigid, start_time, name, length, ActLen, time_obj, daily_mins, list_of_stats

	with open(data_file, 'r') as json_file: # Opens up data.txt as json_file in read mode
		activity_obj = json.load(json_file) # Loads the JSON file and assigns it to the variable activity_obj
		fixed = activity_obj["fixed"]
		rigid = activity_obj["rigid"]
		start_time = activity_obj["start_time"]
		name = activity_obj["name"]
		length = activity_obj["length"]
		ActLen = activity_obj["ActLen"]

	with open(time_file, 'r') as json_time_file:
		time_obj = json.load(json_time_file)
		daily_mins = time_obj["daily_mins"]

	list_of_stats = [fixed,rigid,start_time,name,length,ActLen] # Essentially, this list-ifies the data.txt content, and therefore we are able to loop around the file


# This function is dangerous, because it resets data.txt as soon as the data.txt validation check fails!
def resetter():
	tasks_dict = {
	"fixed": [],
	"rigid": [],
	"start_time": [],
	"name": [],
	"length": [],
	"ActLen": []}

	time_dict = {
	"daily_mins": [959.99]
	}

	with open(data_file, 'w') as json_file:
		json.dump(tasks_dict, json_file, indent=1)

	with open(time_file, 'w') as json_time_file:
		json.dump(time_dict, json_time_file, indent=1)

	validator()

	return

# * Main

def adding(): # This function is for adding a new activity to the program
	with open(data_file, 'w') as json_file: # Opens up data.txt as json_file in write mode
		the_end("start of adding")

		while True: # This is a loop which keeps asking the user to enter the activity name and desired number of minutes
			activity_name_input = input("Enter the activity name (type . to exit): ") # Asks the user to enter the activity name

			if activity_name_input == ".": # If the user enters ".", the program will exit this loop
				break

			else:
				length_input = int(input("Enter the goal number of minutes: ")) # This variable holds the desired number of minutes which the user will supply

				fixed.append("-") # TODO This writes "-" in the fixed field in data.txt. I need to use this later when creating the fixed feature.
				rigid.append("-")
				start_time.append("09:42") # This writes the default start time (09:42)
				name.append(activity_name_input) # Same thing as above but for a new variable
				length.append(length_input) # Same thing as above but for a new variable
				ActLen.append(0) # Same thing as above but for a new variable

		the_end(False)

		json.dump(activity_obj, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects


# This function refreshes the columns. It has the parameter "clear_screen" which takes an argument of True or False. False is the default value. When set to True, the screen will be cleared to make the whole thing look a little nicer.
def view_and_update(clear_screen=False):
# clears the screen
	global fixed, rigid, start_time, name, length, ActLen, rigid_surpless, daily_mins # TODO This globalises the variables so that they can be used in this function. I need to understand why this is needed.

	if not list_length:
		print("Sorry, you have zero activities. Please add some so that you can view the current activity list.\n")
		return

	elif clear_screen == True:
		os.system('cls' if os.name == 'nt' else 'clear')

	with open(time_file, 'r') as json_time_file: # operns up time.txt as json_time_file
		number_of_daily_mins = daily_mins[0] # Reads the current number of work hours

	with open(data_file, 'w') as json_file: # Opens up data.txt as json_file
		length_column_total = 1 # This sets the length_column_total to 1, because, otherwise, we will end up dividing by zero (see the definition of ratio_multiplier to understand what I mean)
		rigid_surpless = 0 # rigid_surpless is a new variable. Its whole purpose will become clear later...

		for i in range(list_length): # This is the loop which will go around the list of activities
			length_column_total += length[i] # This will add the length supplied by the user to the length_column_total

		if length_column_total <= 0: # Just in case the step above has resulted in a negative number or zero...  Maybe making length_column_total = 1 previously is not needed after all.
			length_column_total = 1 # This sets the length_column_total to 1, because, otherwise, we will end up dividing by zero (see the definition of ratio_multiplier to understand what I mean).
		else:
			length_column_total -= 1 # Subtracts the safety number "1"

		ratio_multiplier = float(number_of_daily_mins/length_column_total) # The ratio_multiplier is what we are going to use in order to work out the actual length (ActLen). ActLen is basically the desired length * ratio_multiplier.

		for i in range(list_length):
			ActLen[i] = int(ratio_multiplier * length[i]) # This calculates the actual length for each of the activities

		for i in range(list_length):
			# TODO implement a feature that prevents the user from setting length[i] that is higher than the number of daily number of work hours
			if rigid[i] == "R":
				rigid_surpless += abs(ActLen[i] - length[i]) # This rigid_surpless again. Basically, it will calculate the excess minutes that are left over from the subtraction of ActLen and length (it will also be an absolute value, since we don't want any negative numbers)

		rigid_multiplier = float(rigid_surpless/length_column_total) # rigid_multiplier is the new multiplier (compare that to ratio_multiplier)

		the_end()

		for i in range(list_length): # Loops around, again...
			start_time_format = datetime.strptime(start_time[i], "%H:%M") # This formats the start_time from a string to a proper time. It uses HH:MM format

			ActLen[i] += int(rigid_multiplier * length[i]) # This time, we're using rigid_multiplier instead of ratio_multiplier

			if rigid[i] == "R": # This checks if the activity status is rigid. If so, then it will set ActLen to length (because that is the whole purpose of "Rigid")
				ActLen[i] = length[i]

			new_start_time = start_time_format + timedelta(minutes=ActLen[i]) # This will calculate the start time of each of the activities. It basically takes the start_time and adds the corresponding ActLen to it
			new_start_time_format = datetime.strftime(new_start_time, "%H:%M") # This formats the new_start_time into HH:MM

			if i+1 >= list_length: # This prevents the program from giving an error. The error arises because the program will loop, and loop, and loop until eventually there are no more activities to go over.
				break # Stops the program
			else:
				start_time[i+1] = new_start_time_format # Writes the start time of each activity

		json.dump(activity_obj, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects

		print(f"Current data:\n- Start time: {start_time[0]}\n- Number of work hours: {number_of_daily_mins/60}\n")


		# TODO Fix bug that does not show "$$END$$" unless view_and_update() is called twice (this only happens after adding a task to an empty data.txt)
		print("=" * 83) # Prints "=" 83 times!
		pretty_fmt = "{:<2} {:<5} {:<5} {:<10} {:<20} {:<10} {:<10}" # I've borrowed this idea from kpence (https://github.com/kpence/day-ploy). It basically creates a nice table for us to use
		print (pretty_fmt.format("I", "Fixed", "Rigid", "Start time", "Activity", "Length", "ActLen")) # Prints the column titles
		for x in range(list_length): # Loops over data.txt to print each of the values
			print(pretty_fmt.format(f"{x}", fixed[x], rigid[x], start_time[x], name[x], length[x], ActLen[x]))
		print("=" * 83, "\n")

def modify():
# TODO make it so that the length and the ActLen change according to the rigid and fixed status
	#global fixed, rigid, start_time, name, length, ActLen, list_length # TODO I don't think that this is needed.

	with open(data_file, 'w') as json_file: # Opens up data.txt as json_file
		list_length = len(name)
		activity_number = int(input("Enter the INDEX of the activity which you want to modify: "))
		editor = input("Do you want to\n1. Modify its fixation\n2. Modify it rigidity\n3. Exit\n")

		if editor == "1": # This is the fixation modification
			current_fixed_status = fixed[activity_number]
			fixed_mod = input(f"Currently, the fixation status of '{name[activity_number]}' is: {current_fixed_status}, do you want to modify it?\n1. Yes\n2. No\n") # This prints the "fixed" status of the chosen activity
			if fixed_mod == "1": # Switches to the opposite fixed status
				if current_fixed_status == "-":
					current_fixed_status = "F"
				elif current_fixed_status == "F":
					current_fixed_status = "-"
				fixed[activity_number] = current_fixed_status # Writes the fixed value
				# TODO I need to figure out the maths behind the Fixed feature. Or maybe we should make this app different to the original (in the sense that it will not have a fixed feature. We'll see)
			else:
				pass

		elif editor == "2":
			current_rigid_status = rigid[activity_number]
			rigid_mod = input(f"Currently, the rigidity status of '{name[activity_number]}' is: {current_rigid_status}, do you want to modify it?\n1. Yes\n2. No\n")
			if rigid_mod == "1":
				if current_rigid_status == "-":
					current_rigid_status = "R"
				elif current_rigid_status == "R":
					current_rigid_status = "-"
				rigid[activity_number] = current_rigid_status
			else:
				pass

		json.dump(activity_obj, json_file, indent=1)

# A function that moves the position of a chosen task
def move():

	if not list_length:
		return
	else:
		with open(data_file, 'w') as json_file:
			chosen_task = int(input("Enter the INDEX of the activity which you want to move: "))
			new_position = int(input("Enter the INDEX of the new position: "))

			if (name[chosen_task] or name[new_position]) == "$$END$$": # This prevents the user from choosing an index that has $$END$$
				print("Sorry, you are not allowed to choose a position at which $$END$$ is placed\n")
				return

			else:
				# Backup the task that is currently occupying the position chosen by the user
				backup = [] # This is a list to store our backup
				backup_starting_position = 0 # This is the starting position (this will become relevant shortly)

				for old_stat in list_of_stats: # Loop around the list_of_stats
					backup.append(old_stat[new_position]) # Append the old_stat that is currently occupying the position chosen by the user to the backup[] list

				# Write the content of the chosen task to the new position
				for writer in list_of_stats: # Loop around the list_of_stats, again...
					writer[new_position] = writer[chosen_task] # Write the content of the chosen task to the new position

				# Do the reverse to the above. In other words, write the content of the task that is currently occupying the position chosen by the user (i.e., "new_position") to the position that is occupied by "chosen_task"
				for reverse_writer in list_of_stats: # Loop around the list_of_stats (yet again)
					reverse_writer[chosen_task] = backup[backup_starting_position] # Write out the content from our backup to the position that is occupied by "chosen_task"
					backup_starting_position += 1 # Increment backup_starting_position by 1

				json.dump(activity_obj, json_file, indent=1) # Dump the above into the text file


# * Run, run, run, RUN!

try:
	validator()

except:
	print("There was an issue with the file format, I have fixed it.\nNote: in the future, please avoid modifying the file form as this results in issues.")
	resetter()


while True: # A simple loop to make the program continuous

	list_length = len(name) # This calculates the number of activities in our JSON file based on how many names are present in data.txt

	if list_length == 0:
		resetter()

	repeat = input("What do you want to do?\n1. Add activity\n2. Delete activity\n3. Modify activity\n4. Change the start time\n5. Change the number of hours for today\n6. Move an activity\n7. View current activity list\n")

	if repeat == "1":
		view_and_update(True)
		adding()
		view_and_update(True)

	elif repeat == "2":
		view_and_update(True)

		activity_number = int(input("Enter the INDEX of the activity which you want to delete (or type 000 to reset the data): "))

		if (len(name) == 1) or (not len(name)) or (activity_number == 000):
			resetter()

		else:
			for l in list_of_stats: # This loops around list_of_stats and deletes the corresponding activity number (which was entered by the user)
				del l[activity_number]

	elif repeat == "3":
		view_and_update(True)
		modify()
		view_and_update(True)

	elif repeat == "4":
		view_and_update(True)
		try:
			start_time_input = input(f"Current start time is {start_time[0]}\nEnter the start time in the format HH:MM: ")
			start_time[0] = start_time_input # This sets the start time of the first activity to the start_time_input
			view_and_update(True)
		except:
			print("Sorry, you have zero activities, and hence no start time.\n")

	elif repeat == "5":
		view_and_update(True)
		with open(time_file, 'w') as json_time_file:
			hours_input = float(input(f"Current number of work hours is {(daily_mins[0])/60}\nPlease write how many hours would you like to work for today (0 < x < 24): "))
			daily_mins[0] = round((hours_input*60), 2) # Rounds the result to 2 decimal places
			json.dump(time_obj, json_time_file, indent=1) # Writes this info into the time.txt file
		view_and_update(True)

	elif repeat == "6":
		view_and_update(True)
		move()

	else:
		view_and_update(True)
