# This version of the program is compatible with the SuperMemo Plan format!
# It still lacks a lot of the features (which I absolutely love and use every day) that come
# with Plan (e.g., new schedule for each day, alarm clock, analysis, export to HTML, delay
# calculations, adjust, begin an activity, terminating the schedule, splitting an activity and many more!).
# I am not planning to make it a SuperMemo Plan clone. Its sole purpose is to be used on Linux / phone
# by long-time SuperMemo Plan users (who, already have a more-or-less optimised schedule) to quickly
# create a daily plan using some SuperMemo magic.

import os
import sys
import datetime

SCHEDULE_FILE = os.path.join(sys.path[0],"SMdata.txt")
DEFAULT_HOURS = 11
DEFAULT_SCHEDULE_START_TIME_STR = "00:00"
RIGID_MARKER = "\x01R,"
REFERENCE_DATE = datetime.date(2000, 1, 1)

g_schedule_total_hours = DEFAULT_HOURS
g_schedule_start_time_str = DEFAULT_SCHEDULE_START_TIME_STR
g_activities = []

def parse_time_to_datetime_obj(time_str, base_date=REFERENCE_DATE):
	"""Parses HH:MM string to datetime.datetime object, returns None on error."""
	if not time_str:
		return None
	try:
		time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
		return datetime.datetime.combine(base_date, time_obj)
	except ValueError:
		return None

def format_datetime_to_hhmm(dt_obj):
	"""Formats datetime.datetime object to HH:MM string."""
	if not dt_obj:
		return "N/A"
	return dt_obj.strftime("%H:%M")

def clean_name_part(name_str):
	"""Cleans the activity name part."""
	name_str = name_str.strip()
	if name_str.startswith("-"):
		name_str = name_str[1:].strip()
	return name_str

def parse_activity_line_manually(line):
	"""
	Manually parses a lines using the SuperMemo format "Activity1=0 00:00 ActivityName"
	Returns a dictionary with 'key', 'duration_str', 'fixed_time_str', 'name_and_marker_part' or None if parse fails.
	"""
	if '=' not in line:
		return None

	key_part, value_part = line.split('=', 1)
	value_part = value_part.strip()

	duration_str = ""
	fixed_time_str = None
	name_and_marker_part = ""

	parts = value_part.split(None, 1)
	if not parts:
		return None

	duration_str = parts[0]
	if not duration_str.isdigit():
		return None

	remaining_part = parts[1] if len(parts) > 1 else ""

	potential_time_parts = remaining_part.split(None, 1)
	if potential_time_parts:
		pt = potential_time_parts[0]
		if len(pt) == 5 and pt[2] == ':' and pt[0:2].isdigit() and pt[3:5].isdigit():
			try:
				datetime.datetime.strptime(pt, "%H:%M")
				fixed_time_str = pt
				name_and_marker_part = potential_time_parts[1] if len(potential_time_parts) > 1 else ""
			except ValueError:
				name_and_marker_part = remaining_part
		else:
			name_and_marker_part = remaining_part
	else:
		name_and_marker_part = ""

	return {
		'key': key_part.strip(),
		'duration_str': duration_str,
		'fixed_time_str': fixed_time_str,
		'name_and_marker_part': name_and_marker_part.strip()
	}

def load_schedule():
	global g_schedule_total_hours, g_schedule_start_time_str, g_activities
	g_activities = []
	g_schedule_total_hours = DEFAULT_HOURS
	g_schedule_start_time_str = DEFAULT_SCHEDULE_START_TIME_STR

	if not os.path.exists(SCHEDULE_FILE):
		print(f"Schedule file '{SCHEDULE_FILE}' not found. Using defaults.")
		reset_to_default_schedule()
		return

	try:
		with open(SCHEDULE_FILE, 'r') as f:
			lines = f.readlines()

		section = None
		for line_num, line_content in enumerate(lines):
			line_content = line_content.strip()
			if not line_content or line_content.startswith('#'):
				continue

			if line_content == "[Length]":
				section = "Length"
				continue
			elif line_content == "[Schedule]":
				section = "Schedule"
				continue

			if section == "Length":
				if line_content.startswith("Hours="):
					try:
						g_schedule_total_hours = float(line_content.split('=')[1])
					except ValueError:
						print(f"Warning: Invalid Hours format in line {line_num+1}. Using default hours.")
						g_schedule_total_hours = DEFAULT_HOURS
			elif section == "Schedule":
				parsed_line = parse_activity_line_manually(line_content)
				if parsed_line:
					key = parsed_line['key']
					duration_str = parsed_line['duration_str']
					fixed_time_str_from_file = parsed_line['fixed_time_str']
					name_and_marker = parsed_line['name_and_marker_part']

					user_duration = int(duration_str)
					name_part = name_and_marker
					is_rigid = False

					if name_and_marker.endswith(RIGID_MARKER):
						name_part = name_and_marker[:-len(RIGID_MARKER)].strip()
						is_rigid = True

					name_part = clean_name_part(name_part)

					if not g_activities and fixed_time_str_from_file:
						 g_schedule_start_time_str = fixed_time_str_from_file

					activity = {
						'id_key': key,
						'user_duration': user_duration,
						'name_part': name_part,
						'is_rigid': is_rigid,
						'raw_fixed_start_time': fixed_time_str_from_file,
						'parsed_fixed_start_datetime': parse_time_to_datetime_obj(fixed_time_str_from_file),
						'calculated_start_datetime': None,
						'calculated_act_len_minutes': 0,
						'calculated_end_datetime': None
					}
					g_activities.append(activity)
				else:
					print(f"Warning: Could not parse activity line {line_num+1}: {line_content}")

		if not g_activities:
			print("No activities found in file. Resetting to default schedule.")
			reset_to_default_schedule()
		elif g_activities and g_activities[0]['raw_fixed_start_time']:

			g_schedule_start_time_str = g_activities[0]['raw_fixed_start_time']


	except Exception as e:
		print(f"Error loading schedule file: {e}. Resetting to defaults.")
		reset_to_default_schedule()

def reset_to_default_schedule():
	global g_schedule_total_hours, g_schedule_start_time_str, g_activities
	g_schedule_total_hours = DEFAULT_HOURS
	g_schedule_start_time_str = DEFAULT_SCHEDULE_START_TIME_STR
	g_activities = [{
		'id_key': "Activity1",
		'user_duration': 0,
		'name_part': "Start of day",
		'is_rigid': False,
		'raw_fixed_start_time': g_schedule_start_time_str,
		'parsed_fixed_start_datetime': parse_time_to_datetime_obj(g_schedule_start_time_str),
		'calculated_start_datetime': None,
		'calculated_act_len_minutes': 0,
		'calculated_end_datetime': None
	}]

def save_schedule():
	global g_schedule_start_time_str

	if g_activities and g_activities[0]['name_part'] == "Start of day":
		g_activities[0]['raw_fixed_start_time'] = g_schedule_start_time_str
		g_activities[0]['parsed_fixed_start_datetime'] = parse_time_to_datetime_obj(g_schedule_start_time_str)

	try:
		with open(SCHEDULE_FILE, 'w') as f:
			f.write("[Length]\n")
			f.write(f"Hours={g_schedule_total_hours}\n")
			f.write("\n[Schedule]\n")
			for i, act in enumerate(g_activities):
				id_key = f"Activity{i+1}"
				line = f"{id_key}={act['user_duration']}"
				if act['raw_fixed_start_time']:
					line += f" {act['raw_fixed_start_time']}"

				name_display = act['name_part']
				if not name_display and not act['raw_fixed_start_time']:
					pass
				elif name_display :
					 line += f" - {name_display}"
				elif act['raw_fixed_start_time'] and not name_display:
					pass

				if act['is_rigid']:
					line += f" {RIGID_MARKER}"
				f.write(line.strip() + "\n")
		print(f"Schedule saved to {SCHEDULE_FILE}")
	except Exception as e:
		print(f"Error saving schedule: {e}")


def recalculate_schedule():
	if not g_activities:
		return

	master_schedule_start_dt = parse_time_to_datetime_obj(g_schedule_start_time_str)
	if not master_schedule_start_dt:
		print(f"Error: Invalid master schedule start time: {g_schedule_start_time_str}. Using 00:00.")
		master_schedule_start_dt = parse_time_to_datetime_obj("00:00")

	total_day_minutes = g_schedule_total_hours * 60
	schedule_overall_end_dt = master_schedule_start_dt + datetime.timedelta(minutes=total_day_minutes)

	for act in g_activities:
		act['parsed_fixed_start_datetime'] = parse_time_to_datetime_obj(act['raw_fixed_start_time'])
		act['calculated_start_datetime'] = None
		act['calculated_act_len_minutes'] = 0
		act['calculated_end_datetime'] = None
		act['is_fixed_by_segment_ends'] = False

	current_block_start_dt = master_schedule_start_dt
	activity_idx = 0

	while activity_idx < len(g_activities):

		block_end_dt = schedule_overall_end_dt
		activities_in_block = []

		temp_idx = activity_idx
		first_activity_in_block_fixed_start = g_activities[activity_idx]['parsed_fixed_start_datetime']


		if first_activity_in_block_fixed_start:
			current_block_start_dt = max(current_block_start_dt, first_activity_in_block_fixed_start)

		while temp_idx < len(g_activities):
			act_being_considered = g_activities[temp_idx]

			if temp_idx > activity_idx and act_being_considered['parsed_fixed_start_datetime']:
				block_end_dt = act_being_considered['parsed_fixed_start_datetime']
				break
			activities_in_block.append(act_being_considered)
			temp_idx += 1


		block_end_dt = max(block_end_dt, current_block_start_dt)

		block_available_minutes = (block_end_dt - current_block_start_dt).total_seconds() / 60
		if block_available_minutes < 0: block_available_minutes = 0

		elif len(activities_in_block) == 1:
			act = activities_in_block[0]
			if act['parsed_fixed_start_datetime'] and \
			   temp_idx < len(g_activities) and g_activities[temp_idx]['parsed_fixed_start_datetime'] and \
			   g_activities[temp_idx]['parsed_fixed_start_datetime'] == block_end_dt:
				act['calculated_act_len_minutes'] = int(block_available_minutes)
				act['is_fixed_by_segment_ends'] = True

		elif not activities_in_block[0]['is_fixed_by_segment_ends']:

			time_needed_for_rigid_in_block = 0
			for act in activities_in_block:
				if act['is_rigid']:
					time_needed_for_rigid_in_block += act['user_duration']

			time_for_flexible_in_block = block_available_minutes - time_needed_for_rigid_in_block
			if time_for_flexible_in_block < 0: time_for_flexible_in_block = 0

			total_user_duration_flexible_in_block = 0
			for act in activities_in_block:
				if not act['is_rigid']:
					total_user_duration_flexible_in_block += act['user_duration']

			ratio = 0
			if total_user_duration_flexible_in_block > 0:
				ratio = time_for_flexible_in_block / total_user_duration_flexible_in_block
			if ratio < 0: ratio = 0

			calculated_flexible_minutes_in_block = 0
			for act in activities_in_block:
				if act['is_rigid']:
					act['calculated_act_len_minutes'] = act['user_duration']
				else:
					act['calculated_act_len_minutes'] = int(act['user_duration'] * ratio)
					calculated_flexible_minutes_in_block += act['calculated_act_len_minutes']

			truncation_error = int(time_for_flexible_in_block - calculated_flexible_minutes_in_block)

			flexible_activities_in_block = [act for act in activities_in_block if not act['is_rigid'] and act['user_duration'] > 0]
			if flexible_activities_in_block:
				idx_to_adjust = 0
				while truncation_error != 0:
					if not flexible_activities_in_block: break
					adj_act = flexible_activities_in_block[idx_to_adjust % len(flexible_activities_in_block)]
					if truncation_error > 0:
						adj_act['calculated_act_len_minutes'] += 1
						truncation_error -= 1
					elif truncation_error < 0 and adj_act['calculated_act_len_minutes'] > 0:
						adj_act['calculated_act_len_minutes'] -= 1
						truncation_error += 1
					elif truncation_error < 0 and adj_act['calculated_act_len_minutes'] == 0:

						all_zero = all(fa['calculated_act_len_minutes'] == 0 for fa in flexible_activities_in_block)
						if all_zero: break
					idx_to_adjust +=1
					if idx_to_adjust > 2 * len(flexible_activities_in_block) and truncation_error !=0 :
						break

		running_time_in_block_dt = current_block_start_dt

		for act in activities_in_block:
			if act['parsed_fixed_start_datetime']:
				running_time_in_block_dt = max(running_time_in_block_dt, act['parsed_fixed_start_datetime'])

			act['calculated_start_datetime'] = running_time_in_block_dt
			act['calculated_end_datetime'] = running_time_in_block_dt + \
											 datetime.timedelta(minutes=act['calculated_act_len_minutes'])
			running_time_in_block_dt = act['calculated_end_datetime']

		activity_idx = temp_idx
		current_block_start_dt = block_end_dt

def view_activities():
	recalculate_schedule()
	print(f"Hours: {g_schedule_total_hours}; Start time: {g_schedule_start_time_str}")
	print("-" * 80)

	print(f"{'I':<4} {'F':<3} {'R':<3} {'Start':<6} {'Name':<25} {'Len':<6} {'ActLen':<6}")
	print("=" * 80)
	if not g_activities:
		print("No activities in the schedule.")
	for i, act in enumerate(g_activities):
		is_rigid_str = "R" if act['is_rigid'] else "-"

		fixed_start_str = "F" if act['raw_fixed_start_time'] else "-"

		start_time_str = format_datetime_to_hhmm(act['calculated_start_datetime'])
		end_time_str = format_datetime_to_hhmm(act['calculated_end_datetime'])


		print(f"{i:<4} {fixed_start_str:<3} {is_rigid_str:<3} {start_time_str:<6} {act['name_part'][:25]:<25} {act['user_duration']:<6} {act['calculated_act_len_minutes']:<6}")
	print("-" * 80)

def add_activity():
	name = input("Enter activity name: ").strip()
	if not name:
		print("Activity name cannot be empty.")
		return
	while True:
		try:
			duration = int(input("Enter desired duration (minutes): "))
			if duration < 0: raise ValueError("Duration cannot be negative.")
			break
		except ValueError as e:
			print(f"Invalid duration: {e}. Please enter a non-negative integer.")

	new_activity = {
		'id_key': "",
		'user_duration': duration,
		'name_part': name,
		'is_rigid': False,
		'raw_fixed_start_time': None,
		'parsed_fixed_start_datetime': None,
		'calculated_start_datetime': None,
		'calculated_act_len_minutes': 0,
		'calculated_end_datetime': None
	}
	g_activities.append(new_activity)
	print(f"Activity '{name}' added.")

def delete_activity():
	if not g_activities:
		print("No activities to delete.")
		return
	view_activities()
	choice = input("Enter index of activity to delete, or 'all' to clear schedule: ").strip().lower()
	if choice == 'all':
		confirm = input("Are you sure you want to delete all activities? (yes/no): ").strip().lower()
		if confirm == 'yes':
			reset_to_default_schedule()
			print("All activities cleared. Schedule reset to default.")
		else:
			print("Deletion cancelled.")
		return

	try:
		index = int(choice)
		if 0 <= index < len(g_activities):

			if len(g_activities) == 1 and g_activities[index]['name_part'] == "Start of day":
				print("Cannot delete the last 'Start of day' activity. Reset schedule if needed.")
				return

			deleted_name = g_activities.pop(index)['name_part']
			print(f"Activity '{deleted_name}' at index {index} deleted.")
			if not g_activities:
				 reset_to_default_schedule()
		else:
			print("Invalid index.")
	except ValueError:
		print("Invalid input. Please enter a number or 'all'.")


def modify_activity():
	if not g_activities:
		print("No activities to modify.")
		return
	view_activities()
	try:
		index = int(input("Enter index of activity to modify: "))
		if not (0 <= index < len(g_activities)):
			print("Invalid index.")
			return
	except ValueError:
		print("Invalid input for index.")
		return

	act = g_activities[index]
	print(f"\nModifying: {act['name_part']}")
	print(f"  Current rigid status: {'Yes' if act['is_rigid'] else 'No'}")
	print(f"  Current fixed start time: {act['raw_fixed_start_time'] if act['raw_fixed_start_time'] else 'Not set'}")

	while True:
		mod_choice = input("Toggle rigid (r), set/clear fixed time (f), change duration (d), change name (n), or (b)ack: ").strip().lower()
		if mod_choice == 'r':
			act['is_rigid'] = not act['is_rigid']
			print(f"Rigid status set to: {'Yes' if act['is_rigid'] else 'No'}")
			break
		elif mod_choice == 'f':
			if act['raw_fixed_start_time']:
				if input("Clear fixed time? (y/n): ").lower() == 'y':
					act['raw_fixed_start_time'] = None
					act['parsed_fixed_start_datetime'] = None
					print("Fixed time cleared.")
				else:
					new_time_str = input(f"Enter new fixed time (HH:MM) or press Enter to keep '{act['raw_fixed_start_time']}': ").strip()
					if new_time_str:
						parsed = parse_time_to_datetime_obj(new_time_str)
						if parsed:
							act['raw_fixed_start_time'] = new_time_str
							act['parsed_fixed_start_datetime'] = parsed
							print(f"Fixed time set to {new_time_str}.")
						else:
							print("Invalid time format. Fixed time not changed.")
			else:
				new_time_str = input("Enter fixed start time (HH:MM): ").strip()
				parsed = parse_time_to_datetime_obj(new_time_str)
				if parsed:
					act['raw_fixed_start_time'] = new_time_str
					act['parsed_fixed_start_datetime'] = parsed
					print(f"Fixed time set to {new_time_str}.")
				else:
					print("Invalid time format. Fixed time not set.")
			break
		elif mod_choice == 'd':
			try:
				new_duration = int(input(f"Enter new duration (current: {act['user_duration']}): "))
				if new_duration >=0:
					act['user_duration'] = new_duration
					print(f"Duration set to {new_duration}.")
				else:
					print("Duration must be non-negative.")
			except ValueError:
				print("Invalid duration.")
			break
		elif mod_choice == 'n':
			new_name = input(f"Enter new name (current: {act['name_part']}): ").strip()
			if new_name:
				act['name_part'] = new_name
				print(f"Name set to '{new_name}'.")
			else:
				print("Name cannot be empty. Not changed.")
			break
		elif mod_choice == 'b':
			break
		else:
			print("Invalid choice.")


def change_schedule_start_time():
	global g_schedule_start_time_str
	new_time_str = input(f"Enter new schedule start time (HH:MM) (current: {g_schedule_start_time_str}): ").strip()
	parsed = parse_time_to_datetime_obj(new_time_str)
	if parsed:
		g_schedule_start_time_str = new_time_str

		if g_activities and g_activities[0]['name_part'] == "Start of day":
			g_activities[0]['raw_fixed_start_time'] = new_time_str
			g_activities[0]['parsed_fixed_start_datetime'] = parsed
		print(f"Schedule start time updated to {g_schedule_start_time_str}.")
	else:
		print("Invalid time format. Start time not changed.")

def change_total_hours():
	global g_schedule_total_hours
	try:
		new_hours = int(input(f"Enter new total hours for the day (current: {g_schedule_total_hours}): "))
		if new_hours > 0 and new_hours <= 24:
			g_schedule_total_hours = new_hours
			print(f"Total hours updated to {g_schedule_total_hours}.")
		else:
			print("Invalid number of hours (must be >0 and <=24).")
	except ValueError:
		print("Invalid input. Please enter a number.")

def move_activity():
	if len(g_activities) < 2:
		print("Not enough activities to move.")
		return
	view_activities()
	try:
		from_idx = int(input("Enter index of activity to move: "))
		to_idx = int(input("Enter new index for this activity: "))

		if not (0 <= from_idx < len(g_activities) and 0 <= to_idx < len(g_activities)):
			print("Invalid index.")
			return
		if from_idx == to_idx:
			print("Source and destination indices are the same.")
			return

		moved_activity = g_activities.pop(from_idx)
		g_activities.insert(to_idx, moved_activity)
		print("Activity moved.")
	except ValueError:
		print("Invalid input for index.")

load_schedule()

view_activities()
while True:
	print("\nWhat do you want to do?\n1. View current activity list\n2. Add activity\n3. Delete activity\n4. Modify activity\n5. Change schedule start time\n6. Change number of hours for today\n7. Move an activity\n8. Save and Exit\n9. Exit Without Saving")

	choice = input("Enter your choice: ")

	if choice == '1':
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
	elif choice == '2':
		add_activity()
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
		save_schedule()
	elif choice == '3':
		os.system('cls' if os.name == 'nt' else 'clear')
		delete_activity()
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
		save_schedule()
	elif choice == '4':
		os.system('cls' if os.name == 'nt' else 'clear')
		modify_activity()
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
		save_schedule()
	elif choice == '5':
		change_schedule_start_time()
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
		save_schedule()
	elif choice == '6':
		change_total_hours()
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
		save_schedule()
	elif choice == '7':
		os.system('cls' if os.name == 'nt' else 'clear')
		move_activity()
		view_activities()
		save_schedule()
	elif choice == '8':
		save_schedule()
		print("Exiting day-ploy. Goodbye!")
		sys.exit(0)
	elif choice == '9':
		if input("Are you sure you want to exit without saving? (yes/no): ").strip().lower() == 'yes':
			print("Exiting day-ploy without saving. Goodbye!")
			sys.exit(0)
	else:
		os.system('cls' if os.name == 'nt' else 'clear')
		view_activities()
