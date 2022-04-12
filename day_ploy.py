# This is an Open-source SuperMemo Plan alternative
# To learn more about SuperMemo Plan, please visit: https://help.supermemo.org/wiki/Plan
# The program is pretty easy to use:
## Enter the list of the activities which you want to do today
## Enter the desired number of minutes which you would like to spend on each of these activities
## Let the program give you a more realistic number of minutes for each of your activities

# * Start

import time
import pandas
import csv
import os
import sys

# * Initialise

daily_mins = int(16*60)

# * Main

# This is a function for adding new tasks to your CSV
def adding():
	while True: # This is just a loop that asks the user to enter the activity name and desired length
		activity_name = input("Enter the name of your activity (enter . to quit adding): ")
		if activity_name == ".":
			break
		else:
			length = int(input("Enter length (in minutes): ")) # This will ask the user for the number of minutes
			
            # TODO might need to make the name of the CSV file change according to the date. But this can be done later: "data.csv" should do for now.
			with open(os.path.join(sys.path[0], 'data.csv'), mode='a', newline='') as csv_file:
				fieldnames = [ # TODO another fieldname which is needed is the start time of each activity (make sure you add it in writer.writerow!)
				'Activity',
				'length',
				'ActLen',
				]
                
				writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

				writer.writerow({
				'Activity': activity_name,
				'length': length,
                		'ActLen': 0
				})
                
def view_and_update():
    MyDataFrame = pandas.read_csv(os.path.join(sys.path[0],'data.csv'))

    length_column_total = MyDataFrame['length'].sum() # This will add up all of the values in the length column
    ratio_multiplier = int(daily_mins/length_column_total) # This calculates the value of the multiplier which we will use in order to calculate the actual length
    
    for i in MyDataFrame.index: # Iterates over the dataset
        ActLen_cell_new = ratio_multiplier * MyDataFrame.at[i,'length'] # Calculates the actual length using the user input and the multiplier
        MyDataFrame.at[i,'ActLen'] = ActLen_cell_new # Selects the corresponding ActLen cell, and refreshes it with the new value (ActLen_cell_new)
                                                     # TODO this value does not get added to the data.csv file, I need to make the program add it.
        
    print(MyDataFrame) # Prints the new updated table

def repeater():
    repeat = input("What do you want to do now?\n1. Add tasks\n2. Open the table menu\n3. Close the application\n")
    if repeat == "1":
        adding()
        repeater()
        
    elif repeat == "2":
        view_and_update()
        repeater()

repeater() # My primitive method of looping the program :)
