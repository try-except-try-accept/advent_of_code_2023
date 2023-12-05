from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy

from math import inf as INF

PP_ARGS = False, False #rotate, cast int

DAY = 5
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4///35"""

DEBUG = False

stages = ["seed", "soil", "fertilizer", "water", "light", "temp", "humidity", "location"]

def get_fits(maps, current, d=0):

    try:
        this_map = maps.pop(0)
    except IndexError:
        return current

    p.bugprint("\t"*d, "finding out where", stages[d], current, "fits!")
    
    value = current
    found_fit = False
    
    for this_range in this_map:

        p.bugprint("\t"*d, "checking range", this_range)
        
        dest, source, length = this_range
        if source <= current <= source + length:            
            index = abs(current - source)
            p.bugprint("FOUND! Corresponds to:", dest+index)
            value = get_fits(maps, dest + index, d+1)
            found_fit = True

    if not found_fit:
        value = get_fits(maps, value, d+1)
        

    return value


def solve(data):
    count = 0
    seeds = map(int, data[0].replace("seeds: ", "").split())
    maps = []
    for row in data[1:]:
        
        if not row.strip(): continue

        p.bugprint (" row is ", row)
        if "map:" in row:
            maps.append([])
        else:           
            maps[-1].append(list(map(int, row.split())))

    p.bugprint(maps)

    return min(get_fits(deepcopy(maps), s) for s in seeds)

            
            
            
            




            
        
        
        

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
