import random

class XwordGrid():
    
    def __init__(self, n_rows, n_cols):
        self.board = [[' ']*n_cols]*n_rows
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.crosses = map(lambda x: { 'letters' : [' ']*n_cols, \
            'indices' : [i + x*n_cols for i in range(n_cols)]}, range(n_rows) \
            )
        self.downs = map( lambda x: { 'letters' : [' ']*n_rows, \
            'indices' : [x + i*n_cols for i in range(n_rows)]}, range(n_cols))
            
    def print_board(self):
        for row in self.board:
            print row
            
    def print_words(self):
        for word in self.crosses + self.downs:
            print word			

    def pick_word_random(self):
        return random.choice(self.crosses + self.downs)
        
    def guess_word(self, word):
        letters = ['x']*len(word['letters'])
        updates = map(lambda x: (x, 'x'), word['indices'])
        return updates
        
    def update_words(self, updates):
        for update in updates:
            index, letter = update
            print index, letter
            self.update_letter(index, letter)
            
    def update_letter(self, index, letter):
        my_row = index/self.n_cols
        my_col = index % self.n_rows
        print my_row, my_col
        self.crosses[my_row]['letters'][my_col] = letter
        self.downs[my_col]['letters'][my_row] = letter


if __name__ == "__main__":
    x = XwordGrid(2, 4)
    x.print_board()
    x.print_words()
    
    w = x.pick_word_random()
    updates = x.guess_word(w)
    x.update_words(updates)
    
    x.print_board()
    x.print_words()
    