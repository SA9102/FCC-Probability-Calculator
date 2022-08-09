import copy
import random
# Consider using the modules imported above.

from collections import Counter

# This class contains different coloured balls. It stores the colours
# of the balls and how many balls are there of each colour. The class
# also contains a method to randomly draw a ball from the hat and not
# replace it.
class Hat:

    # When a Hat object is instantiated, the ball colour and number of
    # balls for each colour is passed in.
    def __init__(self, **coloured_balls):
        # 'contents' will return a "list of strings that contains one item
        # for each ball in the hat. Each item in the list should be a
        # color name representing a single ball of that color."

        # This is a string that will contain all the balls which are
        # represented by their colour. Each colour will be separated by a
        # single whitespace.
        colours = ""
        for colour, num in coloured_balls.items():
            colours += (colour + " ") * num

        # We split the 'colours' string on each whitespace, so that each
        # colour is now its own item in a single list, which is stored in
        # the 'contents' instance variable.
        self.contents = colours.split()

        # This method draws a number of random balls from the hat. Each time
        # a ball is taken out, it is not placed back inside.
    def draw(self, ball_num):

        # This will contain a list of all the balls that have been picked
        # out.
        balls_list = list()
        # Keeps track of how many balls have been taken out so far.
        count = 0
        # We keep removing random balls from the hat, either until the
        # required number of balls have been reached, or the hat contains
        # no more balls.
        while count < ball_num and len(self.contents) > 0:
            # Choose a random index from the list.
            ball_index = random.randint(0, len(self.contents) - 1)
            # Use the index to remove the ball from the 'contents' list, and
            # store the colour of this ball in 'ball_removed'.
            ball_removed = self.contents.pop(ball_index)
            # Append the colour of this ball to 'balls_list'.
            balls_list.append(ball_removed)
            # A ball has been taken out so increment the count by one.
            count += 1

        # Return the list of all the balls that have been picked.
        return balls_list
      
    
# This function finds the probability of picking (at least) the
# specified ball colour(s) and its number from the hat. It does this
# by continually repeating the experiment of picking out a specified
# random number of balls from the hat and recording the number of
# successes. The probability is calculated by dividing the number of
# successes by the number of experiments.
def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    # When the 'draw' method is called, the 'contents' instance variable
    # is modified, so we need to continually set this variable to its
    # original value every time the method is called.
    # 'original_contents' contains this original data. We use the
    # 'copy()' functions so that it retrieves a local copy of the data,
    # instead of receiving its reference in memory.
    original_contents = hat.contents.copy()

    # This records the number of times we receieve the expected balls.
    successes = 0
    # 'experiments_left' keeps track of the number of experiments left
    # to perform. We cannot modify the parameter value, so we need to
    # store this initial value in a separate variable.
    experiments_left = num_experiments

    while experiments_left > 0:
        drawn_list = hat.draw(num_balls_drawn)

        # This method of using Counters (to check if a list is a subset
        # of another list) was found on StackOverflow, answered by a user
        # called 'poke'.
        # Link: https://stackoverflow.com/questions/15147751/how-to-check-if-all-items-in-a-list-are-there-in-another-list

        # By converting these to Counters, it will become very easy to
        # check if the items in the 'drawn' list contains all the items
        # in the 'expected' list. These are now essentially stored as
        # dictionaries.
        expected_list = Counter(expected_balls)
        drawn_list = Counter(drawn_list)

        # This flag is set to True when it is found that the amount of
        # balls of a particular colour in 'drawn_list' is less than the
        # amount of balls of the same colour in 'expected_list'.
        failed_flag = False
        # Iterate through 'expected_list' and record the ball colour and
        # its number in each iteration.
        for colour, num in expected_list.items():
            # If 'drawn_list' does not have the required number of balls
            # for a particular colour.
            if num > drawn_list[colour]:
                # Set this flag to True.
                failed_flag = True
                # 'drawn_list' does not contain all the required balls, so
                # we exit the for loop.
                break

        # If 'drawn_list' has all the required ball colours and their
        # numbers.
        if failed_flag == False:
            # We succeeded in the experiment so we increment this variable
            # by one.
            successes += 1

        # 'contents' has been modified as a result of picking out balls,
        # so we set it to its original value so we can repeat the
        # experiment.
        hat.contents = original_contents.copy()
        # An experiment is completed so we decrement this value by one.
        experiments_left -= 1

    # Return the probability.
    return successes / num_experiments



# TESTS

random.seed(95)
hat = Hat(blue=4, red=2, green=6)
print(hat.draw(3))
probability = experiment(
    hat=hat,
    expected_balls={"blue": 2,
                    "red": 1},
    num_balls_drawn=4,
    num_experiments=3000)
print("Probability:", probability)
