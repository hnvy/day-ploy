# This is an open-source SuperMemo Plan alternative
# To learn more about SuperMemo Plan, please visit: https://help.supermemo.org/wiki/Plan
# The program is pretty easy to use:
## Enter the list of the activities which you want to do today
## Enter the desired number of minutes which you would like to spend on each of these activities
## Let the program give you a more realistic number of minutes for each of your activities

import datetime
from datetime import datetime
from datetime import timedelta
import json
import os
import sys

data_file = os.path.join(sys.path[0],'data.txt')

daily_mins = 16*60

with open(data_file, 'r') as json_file:
    activity_obj = json.load(json_file)
    fixed = activity_obj["fixed"]
    rigid = activity_obj["rigid"]
    start_time = activity_obj["start_time"]
    name = activity_obj["name"]
    length = activity_obj["length"]
    ActLen = activity_obj["ActLen"]

def adding():
    with open(data_file, 'w') as json_file:
        while True:
            task_name_input = input("Enter the task name (type . to exit): ")
            if task_name_input == ".":
                break
            else:
                length_input = int(input("Enter the number of goal number of desired minutes: "))
            fixed.append("-")
            rigid.append("-")
            start_time.append("00:00") # TODO Let the user pick their own start time through the program. But, for now, modify this value in order to set the start time of your day (HH:MM)!
            name.append(task_name_input)
            length.append(length_input)
            ActLen.append(0)
            json.dump(activity_obj, json_file, indent=1)

def view_and_update():
    global fixed, rigid, start_time, name, length, ActLen
    with open(data_file, 'w') as json_file:
        list_length = len(name)
        length_column_total = 1
        for i in range(0,list_length):
            length_column_total += length[i]

        length_column_total -= 1
        if length_column_total <= 0:
            length_column_total = 1

        ratio_multiplier = int(daily_mins/length_column_total)

        for i in range(0,list_length):

            start_time_format = datetime.strptime(start_time[i], "%H:%M")
            ActLen[i] = int(ratio_multiplier * length[i])

            new_start_time = start_time_format + timedelta(minutes=ActLen[i])
            new_start_time_format = datetime.strftime(new_start_time, "%H:%M")
            if i+1 >= list_length:
                break
            else:
                start_time[i+1] = new_start_time_format

        json.dump(activity_obj, json_file, indent=1)

        pretty_fmt = "{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}" # I've borrowed this idea from kpence (https://github.com/kpence/day-ploy)
        print (pretty_fmt.format("Fixed", "Rigid", "Start time", "Activity", "Length", "ActLen"))
        for x in range(0,list_length):
            fixed_value = fixed[x]
            rigid_value = rigid[x]
            start_time_value = start_time[x]
            name_value = name[x]
            length_value = length[x]
            ActLen_value = ActLen[x]
            print(pretty_fmt.format(fixed_value, rigid_value, start_time_value, name_value, length_value, ActLen_value))

while 0 < 1:
    repeat = input("What do you want to do?\n1. Add tasks\n2. Delete tasks\n3. View current list\n")
    if repeat == "1":
        adding()
        view_and_update()
    elif repeat == "2":
        list_of_stats = [fixed,rigid,start_time,name,length,ActLen]
        task_number = int(input("Enter the INDEX of the task which you want to delete: "))
        for l in list_of_stats:
            del l[task_number]
            start_time[0] = "00:00"
    elif repeat == "3":
        view_and_update()
    else:
        break
