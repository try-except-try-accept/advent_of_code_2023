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
QQQJA 483///5905"""

DEBUG = False

class Hand:

    def __init__(self, data):
        data = data.split()
        #print(data[0], "Becomes", end="")

        def jokerise(x):
            if x.isdigit():
                return int(x)
            elif x == "J":
                return -1
            else:
                return "TJQKAJ".index(x)+10
        
        self.cards = list(map(jokerise, data[0]))
        
        #print(self.cards)
        self.bid = int(data[1])
        five_kind, four_kind, three_kind = False, False, False
        full_house = False
        pairs, two_pairs = False, False
        high = max(self.cards)

        jokers = self.cards.count(-1)        
        freqs = Counter(card for card in self.cards if card > -1).most_common()

        try:
            most_common_freq = freqs[0][1]
            most_common_card = freqs[0][0]
            sec_most_common_freq = freqs[1][1]
            sec_most_common_card = freqs[1][0]

            most_common_freq += jokers
            
            if most_common_freq == 5:
                five_kind = True            
            elif most_common_freq == 4:
                four_kind = True            
            elif most_common_freq == 3:
                jokers_left = (3 - most_common_freq)
                if sec_most_common_freq == 2 - jokers_left:
                    full_house = True
                else:
                    three_kind = True            
            elif most_common_freq == 2:
                jokers_left = (2 - most_common_freq)
                if sec_most_common_freq == 2 - jokers_left:
                    two_pairs = True
                else:
                    pairs = True
                    
        except IndexError:
            five_kind = True

        self.stats = {"5":five_kind,
                      "4":four_kind,
                      "f":full_house,
                      "3":three_kind,
                      "P":two_pairs,
                      "p":pairs,
                      "h":high}

    def __str__(self):
        stat = [key for key, stat in self.stats.items() if stat is not None]
        return f"{self.cards} {stat}"

    def tie_break(self, other):
        for this_card, that_card in zip(self.cards, other.cards):
            if this_card > that_card:
                p.bugprint(self, f"stronger because {this_card} vs {that_card}")
                return True
            elif this_card < that_card:
                p.bugprint(other, f"stronger because {this_card} vs {that_card}")
                return False       

    def __gt__(self, other):
        p.bugprint("Comparing", str(self), str(other))
        for stat_id in self.stats.keys():
            p.bugprint(stat_id)
            if self.stats[stat_id]:
                if other.stats[stat_id]:
                    return self.tie_break(other)
                p.bugprint(self, f"stronger because {stat_id}")
                return True
            elif other.stats[stat_id]:
                p.bugprint(other, f"stronger because {stat_id}")
                return False

def solve(data):

    
    winnings = 0

    ## order data
    hands = sorted([Hand(row) for row in data])
    
    ## calculate 
    for i, hand in enumerate(hands):
        rank = i + 1
        winnings += (rank * hand.bid)
        p.bugprint(rank, "*", hand.bid)
    

    return winnings

def tests():

    test_cases = {"5":"77777 999",
                  "5J":"7777J 999",
                  "5JJ":"777JJ 999",
                  "5JJJ":"77JJJ 999",
                  "5JJJJ":"7JJJJ 999",
                  "5JJJJJ":"JJJJJ 999",
                  "4":"77776 999",
                  "4J":"777J6 999",
                  "4JJ":"77JJ6 999",
                  "4JJJ":"7JJJ6 999",
                  "3JJ":"765JJ 999",
                  "3":"77765 999",
                  "f":"77766 999",
                  "p":"77456 999",
                  "pJ":"J7654 999",
                  "P":"77665 999"}

    for win, hand in test_cases.items():
        
        print(f"Testing {hand}, should get {win[0]}")
        stats = Hand(hand).stats
        print(stats)
        
        print()
        
        assert stats[win[0]]


if __name__ == "__main__":
    tests()
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
