# newrepo
To invoke, use python 2.7: "python fitblocks.py"
All packages should be available with python 2.7

The test_fit_blocks function should be called with the number of units in the problem, multiplied by ten
So a width of 12 would be 120, and the seams would be located in multiples of 30 or 45

in main(), at top of fitblocks.py, comment out tests you do not want to run, or add tests
def main():

    # examples given in problem
    test_fit_blocks(120, 4) # 120 is equivalent to using 12, and 4 rows
    test_fit_blocks(270, 5) # 270 is equivalent to using 27, and 5 rows

    # the one we're solving
    test_fit_blocks(480, 10)    # 480 is the same as 48, and 10 rows
