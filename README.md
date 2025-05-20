# day-ploy
A Python program that assists you in creating a realistic daily schedule depending on how much you love each activity.

# What is this?
> ploy _(noun)_ a slightly dishonest method used to try to achieve something
> 
> Source: https://dictionary.cambridge.org/dictionary/learner-english/ploy

day-ploy is a Python program that allows you to manipulate the flow of time. It will day-ploy (deploy) a perfect daily plan for you to follow (as best as you can) based on the basic facts you provide.

This program is based on the concept behind [SuperMemo Plan](https://help.supermemo.org/wiki/Plan), which is a game-changing piece of software that will... well, change your life for the better.

This is not intended to be a replacement for SuperMemo Plan (there are a lot of missing features: new schedule for each day, alarm clock, analysis, delay calculations, terminating the schedule, splitting an activity and many, many, many more). This merely attempts to: (1) serve power users when there is no access to Plan; (2) introduce new users to Plan.

# How do you use it?
Very simple:
1. Run the program and enter the list of the activities which you want to do today.
2. Enter the desired number of minutes which you would like to spend on each of these activities
3. Let the program give you a more realistic number of minutes for each of your activities

# Contributing
Not sure what you should be aiming for? Read [this guide](https://drive.google.com/folderview?id=11RUZw8MVdKXdb8HpuYR5epiktKPhkoOO) to find out about how the original SuperMemo Plan is supposed to work.

Feel free to contact me if you get stuck, I will be more than happy to help!

# Changelog
- 19/05/2025 (**final release**)
  - An overdue re-write of the entire program to make it more robust (please see [day-ploy-SM.py](day-ploy-SM.py)).
  - day-ploy now uses the same format as SuperMemo Plan. This will allow users to sync files between day-ploy and SuperMemo Plan.
  - Added the Fixed feature.
  - This will probably be the final release. If you are interested in such an app, I recommend you check out [SuperMemo Plan](https://help.supermemo.org/wiki/Plan)!
- 26/08/2022
  - You can now move tasks up and down.
  - The program now clears the screen to give you a better experience.
- 24/08/2022
  - You can now find out the time at which the day ends (it is printed out as `$$END$$` at the end of the activity list)
- 23/08/2022
  - The program now adds the number of daily work hours to `time.txt`. This means that the program will now remember the number of work hours. I wanted to avoid the use of another text file, but, unfortunately, this turned out to be the easiest way. If you have another idea, let me know!
- 09/08/2022
  - File validation added.
- 06/08/2022
  - Added the Rigid feature.


# TODO list
## Will NOT be done
- [ ] Create timer
- [ ] Create GUI (perhaps use [Gooey](https://github.com/chriskiehl/Gooey) as it is quick and easy)
  - [ ] Or perhaps create a TUI using something like [asciimatics](https://github.com/peterbrittain/asciimatics) (I like this one a lot)
- [ ] Add ability to make the name of the text file change according to the (chosen) date. But this can be done later: "data.txt" should do for now.

## Done
- [X] Add Fixed feature
- [X] Add ability to move activities up and down
- [X] Feature that tells the user the time at which the day ends
- [X] Make the program remember the number of daily working hours. This is added to `time.txt`
- [X] File validation
- [X] Add Rigid feature
- [X] Need to make the program figure out the start time based on ActLen
- [X] Need to make the program add the start time to the CSV
- [X] Let the user enter their own start time
- [X] There is an issue where ActLen is not being written into the CSV file
- [X] Think about whether we should use Pandas or JSON. The reason being is that, currently, Pandas uses about 30 Mb of RAM, whereas JSON uses 2 Mb.
  - [X] Furthermore, Pandas is a somewhat esoteric library, and few people will be comfortable using it. Therefore, this could limit the number of contributors.
- [X] Print the index of each activity to make it easier for the user to delete something
