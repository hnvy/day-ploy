# day-ploy
A Python program that assists you in creating a realistic daily schedule depending on how much you love each activity.

# What is this?
> ploy _(noun)_ a slightly dishonest method used to try to achieve something
> 
> Source: https://dictionary.cambridge.org/dictionary/learner-english/ploy

day-ploy is a Python program that allows you to manipulate the flow of time. It will day-ploy (deploy) a perfect daily plan for you to follow (as best as you can) based on the basic facts you provide.

This program is based on the concept behind [SuperMemo Plan](https://help.supermemo.org/wiki/Plan), which is a game-changing piece of software that will... well, change your life for the better.

This Python program is not intended to be a complete replacement for SuperMemo Plan, but rather as a starting point for further development and expansion. I'm hoping for this to serve as a skeleton for something more considerable.

# How do you use it?
Very simple:
1. Put the txt file in the same location as the code
2. Run the program and enter the list of the activities which you want to do today
3. Enter the desired number of minutes which you would like to spend on each of these activities
4. Let the program give you a more realistic number of minutes for each of your activities

# Contributing
The program is still a massive work-in-progress. If you would like to contribute, then please do so!

You can fork this project and build something pretty :).

Not sure what you should be aiming for? Read [this guide](https://drive.google.com/folderview?id=11RUZw8MVdKXdb8HpuYR5epiktKPhkoOO) to find out about how the original SuperMemo Plan is supposed to work. Then simply transform those concepts into Python letters and numbers to bring it to life.

Feel free to contact me if you get stuck, I will be more than happy to help!

# Changelog
- 09/08/2022
  - File validation added.
- 06/08/2022
  - Added the Rigid feature.

# TODO list
## To be done
- [ ] Create timer
- [ ] Create GUI (perhaps use [Gooey](https://github.com/chriskiehl/Gooey) as it is quick and easy)
  - [ ] Or perhaps create a TUI using something like [asciimatics](https://github.com/peterbrittain/asciimatics) (I like this one a lot)
- [ ] Add Fixed feature (I need to first figure out the maths behind it)
- [ ] Add ability to make the name of the text file change according to the (chosen) date. But this can be done later: "data.txt" should do for now.
- [ ] Add ability to move activities up and down

## Done
- [X] File validation
- [X] Add Rigid feature
- [X] Need to make the program figure out the start time based on ActLen
- [X] Need to make the program add the start time to the CSV
- [X] Let the user enter their own start time
- [X] There is an issue where ActLen is not being written into the CSV file
- [X] Think about whether we should use Pandas or JSON. The reason being is that, currently, Pandas uses about 30 Mb of RAM, whereas JSON uses 2 Mb.
  - [X] Furthermore, Pandas is a somewhat esoteric library, and few people will be comfortable using it. Therefore, this could limit the number of contributors.
- [X] Print the index of each activity to make it easier for the user to delete something
