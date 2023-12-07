from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 7
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483///6440"""

DEBUG = True

class Hand:

    def __init__(self, data):
        data = data.split()
        self.hand = Counter(data[0])
        self.bid = int(data[1])
        self.five_kind, self.four_kind, self.three_kind = False, False, False
        self.pairs = None
        self.high = max(data, key=lambda x: int(x, 16))

        freqs = self.hand.most_common()
        try:
            most_common_freq = freqs[0][1]
            most_common_card = freqs[0][0]
            sec_most_common_freq = freqs[1][0]
            sec_most_common_card = freqs[1][1]

            if most_common_freq == 4:
                self.four_kind = most_common_card
            elif most_common_freq == 3:
                if sec_most_common_freq == 2:
                    self.full_house = (most_common_card, sec_most_common_card)
                else:
                    self.three_kind = most_common_card
            elif most_common_freq == 2:
                if sec_most_common_freq == 2:
                    self.pairs = (most_common_card, sec_most_common_card)
                else:
                    self.pairs = (most_common_card,)
            
        except IndexError:
            self.five_kind = most_common_card
        

def order(data) -> dict:

    data = [Hand(row) for row in data]

    

    return sorted(data)


def solve(data):
    data = "\n".join(data)

    for orig, hexify in zip("AKQJT", "EDCBA"):
        data = data.replace(orig, hexify)

    data = "\n".join(data)
    
    winnings = 0

    ## order data
    hands = order(data)

    ## calculate 
    for i, hand in enumerate(hands):
        rank = i + 1
        winnings += rank * hand["bid"]

        
    

    return winnings




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
