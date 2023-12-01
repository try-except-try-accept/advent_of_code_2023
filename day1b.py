from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 1
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen///281"""

num_map = list(enumerate("one,two,three,four,five,six,seven,eight,nine".split(",")))
DEBUG = True

NUM_WORDS = "one|two|three|four|five|six|seven|eight|nine"

NUM_WORD_MESS_MAP = {}

for n in NUM_WORDS.split("|"):
    for n2 in NUM_WORDS.split("|"):
        if n[-1] == n2[0]:
            mess = n[:-1]+n2
            NUM_WORD_MESS_MAP[mess] = n + n2
      
def word_to_num(word):    
    if word.isdigit():
        return word    
    else:
        return str(NUM_WORDS.split("|").index(word)+1)
            
def solve(data):
    count = 0
    score = 0
    data = "\n".join(data)
    
 
    for mess, rep in NUM_WORD_MESS_MAP.items():
        data = data.replace(mess, rep)
                
    
    for row in data.splitlines():
        
        a = findall("[1-9]{1}|" + NUM_WORDS, row)       
        this = int(word_to_num(a[0]) + word_to_num(a[-1]))
        score += int(this)
        
    return score


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
