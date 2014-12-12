#!/usr/bin/env python

import random
import pdb
import numpy

def log(s, verbose=False):
    if verbose:
        print s

# ========
# GAME
# ========

class Word():
    def __init__(self, indices, desc):
        self.indices = indices
        self.desc = desc
        self.filled = [0]*len(self.indices)
        self.pick_score = 0
        
    def length(self):
        return len(self.indices)
        
    def unfilled_indices(self):
        unfilled_indices = [self.indices[i] for i,j in enumerate(self.filled) if j == 0]
        return unfilled_indices
        
    def n_unfilled(self):
        return len(self.unfilled_indices())
        
    def summary(self):
        return self.desc + \
        ", Indices: " + ",".join([str(x) for x in self.indices]) + \
        ", Filled: " + ",".join([str(x) for x in self.filled]) + \
        ", Score: " + str(self.pick_score)
        
    def update_word(self, indices_for_update, picker):
        self.filled = [int((self.filled[i] == 1) | (self.indices[i] in indices_for_update)) for i in range(self.length())]
        self.update_score(picker)
        #log("- update word: " + self.summary())

    def update_score(self, picker):
        log("before:" + self.summary())
        self.pick_score = picker.score(self)
        log("after:" + self.summary())

class Board():
    def __init__(self, n_rows, n_cols):
        self.board = [0]*n_cols*n_rows
        self.words = []
        self.n_rows = n_rows
        self.n_cols = n_cols
        for i in range(n_rows):
            self.words.append(Word([j + i*n_cols for j in range(n_cols)], "Row"+str(i)+"Word"))
        for j in range(n_cols):
            self.words.append(Word([j + i*n_cols for i in range(n_rows)], "Col"+str(j)+"Word"))
        self.refs = [(i/n_cols, i % n_cols + n_rows) for i in range(n_rows*n_cols)]

    def fill_word(self, i_word, picker):
        indices_for_update = self.words[i_word].unfilled_indices()
        for ix in indices_for_update: # update board
            self.board[ix] = 1
        i_words_affected = set([i for pair in [[a,b] for (a,b) in [self.refs[ix] for ix in indices_for_update]] for i in pair])
        for i in i_words_affected:
            self.words[i].update_word(indices_for_update, picker)

    def print_board(self):
        for i in range(self.n_rows):
            row = self.board[self.n_cols*i:(self.n_cols*(i+1))]
            log(",".join([str(elem) for elem in row]))
    
    def print_words(self):
        for word in self.words:
            print word.summary()

    def squares_left(self):
        return len(self.board) - sum(self.board)
    
    
class Xword():
    def __init__(self, board, picker, guesser, day_of_week):
        self.board = board
        self.picker = picker
        self.guesser = guesser
        self.day_of_week = day_of_week
        self.time_elapsed = 0
        self.turns = 0
        
    def play(self):
        self.set_initial_scores()
        while self.board.squares_left() > 0:
            self.print_status()
            self.turns += 1
            word, i_word = self.picker.pick_word(self.board)
            answered, time = self.guesser.guess(word, self.day_of_week)
            self.time_elapsed += time
            if answered:
                self.board.fill_word(i_word, self.picker)
        self.print_status()
        return (self.time_elapsed, self.turns)
        
    def set_initial_scores(self):
        for word in self.board.words:
            word.update_score(self.picker)
            
    def print_status(self):
        log("Board Status @ Turn " + str(self.turns) + \
        ": Squares Left: " + str(self.board.squares_left()) + \
        ", Time Elapsed: " + str(self.time_elapsed))
        self.board.print_board()

# ========
# PICKER
# ========

class Picker():            
    def pick_word(self, board):
        pick_scores = map(lambda x: x.pick_score, board.words)
        top_score = max(pick_scores)
        i_top_scores = [i for i, score in enumerate(pick_scores) if score == top_score]
        i_pick = random.choice(i_top_scores)
        word = board.words[i_pick]
        log("> pick word: " + word.summary())
        return (word, i_pick)
    
    def set_params(self, w_done, w_length, w_unfilled):
        self.w_done = w_done
        self.w_length = w_length
        self.w_unfilled = w_unfilled
        
    def score(self, word):
        return(self.w_done * (word.n_unfilled() == 0) + self.w_length * word.length() + self.w_unfilled * word.n_unfilled())
        
class PickRandom(Picker):
    def __init__(self):
        self.set_params(-999,0,0)

class PickLonger(Picker):
    def __init__(self):
        self.set_params(-999, 1, 0)

class PickShortr(Picker):
    def __init__(self):
        self.set_params(-999, -1, 0)

class PickConso(Picker):
    def __init__(self):
        self.set_params(-999, 0, -1)

class PickAggro(Picker):
    def __init__(self):
        self.set_params(-999, 0, 1)


        
# ========
# GUESSER
# ========
        
class Guesser():
    def __init__(self):
        self.score = 0
        
class OneSecondPerfectGuesser(Guesser):
    def guess(self, word, day_of_week):
        return(True, 1)

class OneSecondRandomGuesser(Guesser):
    def guess(self, word, day_of_week):
        answered = (random.random() < 0.5)
        time_elapsed = 1        
        return (answered, time_elapsed)
    
class NikhilGuesser(Guesser):
    def guess(self, word, day_of_week):
        n = word.length()
        x = n - word.n_unfilled()
        d = day_of_week
        
        p_win = 0.728 - 0.054*n + 0.128*x - 0.037*d
        answered = (random.random() < p_win)
        time_elapsed = max(0, 0.473 + 1.142*n - 1.449*x + 0.544*d)
        
        log('> correct: %(answered)s (p=%(p_win)f), time: %(time_elapsed)s' % {"answered" : answered, "p_win": p_win, "time_elapsed": time_elapsed})
#        log("> guess word: " + str(answered) + " (p=)" + " (" + str(time_elapsed) + " time elapsed)")
        return (answered, time_elapsed)
        

# ========
# RUN
# ========
def run_pickers(pickers, guesser):
    pretty = False
    n_tests = 100
    days_of_week = [1,2,3,4,5,6]
    grid_sizes = [(3,6),(3,7),(4,6),(4,7)]
    for day_of_week in days_of_week:
        for grid_size in grid_sizes:
#            print ""
            for picker in pickers:
                if pretty:
                    print(day_name(day_of_week) + " " + str(grid_size[0]) + "x" + str(grid_size[1]) + " " + picker.__class__.__name__ + " : "),
                else:
                    print(day_name(day_of_week) + "," + str(grid_size[0]) + "x" + str(grid_size[1]) + "," + picker.__class__.__name__ + ","),
                run_stats(grid_size, picker, guesser, day_of_week, n_tests, pretty)                 
#        print "---"
        
def run_stats(grid_size, picker, guesser, day_of_week, n_tests, pretty):
    times_turns = [Xword(Board(grid_size[0], grid_size[1]), picker, guesser, day_of_week).play() for i in range(n_tests)]
    times = map(lambda x: x[0], times_turns)
    turns = map(lambda x: x[1], times_turns)
    if pretty:
        print "time = " + str(round(numpy.mean(times), 1)) + " (" + str(round(numpy.std(times), 1)) + ")" + \
        ", turns = " + str(round(numpy.mean(turns), 1)) + " (" + str(round(numpy.std(turns), 1)) + ")"
    else:
        print "" + str(round(numpy.mean(times), 1)) + "," + str(round(numpy.std(times), 1)) + \
        "," + str(round(numpy.mean(turns), 1)) + "," + str(round(numpy.std(turns), 1))
    
def day_name(day_of_week):
    day_names = {1 : '1_mon', 2 : '2_tue', 3 : '3_wed', 4 : '4_thu', 5 : '5_fri', 6 : '6_sat', 0 : '0_sun'}
    return(day_names[day_of_week])
    
        
if __name__ == "__main__":
    pickers = [PickRandom(), PickShortr(), PickLonger(), PickConso(), PickAggro()]
    run_pickers(pickers, NikhilGuesser())

    
# a <- read.csv("model_resultsA.csv", header=F, col.names=c("d","size","picker","t.mean","t.std","n.mean","n.std"))
# ggplot(a, aes(x=paste(size, d), y=t.mean/10, group=picker, color=picker)) + geom_point() + labs(title="Strategy Performance (time) vs Grid Size, Difficulty") + xlab("Grid Size, Difficulty") + ylab("Mean Solve Time")
# ggplot(a, aes(x=paste(size, d), y=n.mean, group=picker, color=picker)) + geom_point() + labs(title="Strategy Performance (# turns) vs Grid Size, Difficulty") + xlab("Grid Size, Difficulty") + ylab("Mean # Turns")
