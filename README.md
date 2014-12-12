crossword
=========

goal
-------
explore clue selection strategies for solving crosswords, assuming:
- solving clues is a function of:
-- answer length 
-- portion of answer completed
- solving method returns correct answer or no answer after finite time

steps
-------

1. model 2 functions with dictionary data (2.5 hours)
 * find, import words + definitions
 * build tester program with arbitrary # of fills
 * design testing sequence
 * solve large set of clues to gather data

> not realistic enough clues, let's use real clues ...

1. model 2 functions with real clues (4 hours)
 * explore .puz format, .puz readers
 * find, download corpus of nytimes crossword puzzles
 * store all clues into database
 * incorporate real clues into tester program
 * solve large set of clues to gather data
 * crowdsource model data from others
 * correct for answer typing time

2. design board data structure (2 hours)

3. model word GUESSER using above data, with passes but no errors (2 hours)
 * decide inputs: word length, letters completed, day of week
 * decide functional form
 * extract function parameters
 * code up function
 * testing
 
4. design word PICKERs (1 hour)
 * brainstorm picking strategies
 * implement strategies
 * testing

6. produce results for n*m grid for various PICKERs and GUESSERs (15 min)

7. analysis (3 hours)

TOTAL = 12.5 hours

analysis
--------

Q0. Does the model produce approximately correct timing for life-sized crossowrds?

A0. Assume Monday through Saturday crosswords have 75 clues each, with average word lengths of 5 for Mon-Wed and 6 for Thurs-Sat. The first column shows appropriately scaled model times for NikhilGuesser and PickCloser (default strategy), the second column shows actual times.

| Day size | model times (std) | real times (std) | n real |
-----------|-------------------|------------------|---------
| mon  5x5 | 544.1 (155.6)     | 331.7 (87.9)     |  61    |
| tue  5x5 | 663.9 (203.4)     | 543.6 (203.4)    |  59    |
| wed  5x5 | 790.4 (231.5)     | 799.5 (279.4)    |  57    |
| thu  6x6 | 1361.0 (409.7)    | 1479.1 (511.2)   |  41    |
| fri  6x6 | 1619.8 (502.6)    | 1822.0 (529.1)   |  21    |
| sat  6x6 | 1922.4 (638.0)    | 1446.0 (246.1)   |  2     |

Note small sample size for later days. Overall, approximately correct times. This analysis ignores "theme" clues, which presumably account for much of the variance in harder days.

Q1. In general, is it better to play conservatively (selecting words that already have many squares filled it) or aggressively (selecting words that are mostly empty)?

A1. Conservative play is slightly faster than random play and considerably faster than aggressive play, across a range of difficulty ranges and grid sizes. Random is close to conservative, most likely because toward the end of a grid most of the remaining words will already have squares filled in. For example, after filling two ACROSS clues in a 5x5 grid, there are 8 remaining clues, 5 of them have two squares filled in and only 3 are empty.
[perf_times.png]

Aggressive play, however, usually requires fewer total word guesses. This makes sense - with each successful guess, more of the crossword is filled. The effect reverses for larger and more difficult boards, presumably because the probability of a successful guess decreases to the point where it ends up costing more turns and time. Even for smaller and easier grids, conservative play is still faster when adding a reasonable non-zero switching time between word guesses. 
[perf_turns.png]

Q2. In a grid, is it better to go for the shorter or longer words first?

A2. Data indicate selecting shorter words produces faster times than longer words. The pattern is very similar to conservative versus aggressive, with the difference that conservative play beats random play wherease selecting shorter words is inferior to random play. I'm not sure why this is true, it needs further investigation.

to do
-------
- internalize to the model the time variable, i.e. as a part of strategy, choose to invest certain amount of time on a given clue with a variable chance of answering correctly. compare outcomes for different time strategies, for example: slow and steady versus quick guesses. this requires collecting accuracy data given constrained guessing time. it also increases the dimensionality of the model space, may have to eliminate clue difficulty.
