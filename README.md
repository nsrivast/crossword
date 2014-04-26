crossword
=========

goal
-------
explore optimal crossword strategy, assuming solving clues is a function of:
- word length 
- word completed
and returns correct answer after finite time (dependent variable) or nothing

steps
-------
1. model 2 functions with dictionary data (2.5h=2.5h)
1a. find, import words + definitions (15=20)
1b. build tester program with arbitrary # of fills (30=25)
1c. design testing sequence (15=15)
1d. run self-test (60=60)
> not realistic enough clues ...

*1. model 2 functions with real clues (2.5h=3.5h)
*1a. explore .puz format, .puz readers (20=20 w help)
*1b. find, download corpus of nytimes crossword puzzles (15=30)
*1c. store all clues into database (20=30)
*1d. incorporate real clues into tester program (30=60)
*1e. run self-test (60=60)
*1f. crowdsource model data (ongoing)

2. design board data structure (1h)
3. model word GUESSER using above data, with passes but no errors (1h)
4. design word PICKER (1h)
5. build xword SOLVER (2h)
6. produce results for n*m grid for various PICKERs and GUESSERs (1h)
7. analysis