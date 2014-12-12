import random
import time
import csv

dict_file = open("dict_common.csv", "r")
lines = dict_file.readlines()
lines = lines[0].split("\r")
DICT = {k:v for (k,v) in [l.split(",") for l in lines]}
WORDS = DICT.keys()

LENDICT = dict()
for word in WORDS:
    n = len(word)
    if LENDICT.has_key(n):
        LENDICT[n] = LENDICT[n] + [word]
    else:
        LENDICT[n] = [word]
        

def prompt_random(n_word, n_fills):
    xword = random.choice(LENDICT[n_word])
    xdef = DICT[xword]
    fills = random.sample(range(0, n_word), n_fills)
    prompt = " ".join([xword[i] if i in fills else "_" for i in range(n_word)])
    print prompt, "(", len(xword), ") :", xdef.split(";", 1)[0]
    return xword, prompt
    
def run_turn():
    ab = random.sample(range(3, 9), 2)
    n_word = max(ab)
    n_fills = max(0, min(ab)-2)
    t1 = time.time()
    xword, prompt = prompt_random(n_word, n_fills)
    guess = raw_input("Guess the word: ")
    print "you win" if (guess == xword) else "you lose, the word was:", xword
    return (n_word, n_fills, xword, guess, guess==xword, time.time()-t1, prompt)
    
    
def run_game(n_prompts, filename):
    f = open(filename, 'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    for i in range(n_prompts):
        print ""
        turn_result = run_turn()
        instr = raw_input("(n) yes, (x) no")
        if (instr == "n"):
            wr.writerow(turn_result)
            

if __name__ == "__main__":
    n_prompts = 50
    fname = "model_data_" + time.strftime("%H%M%S")
    run_game(n_prompts, fname)
