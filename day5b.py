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
56 93 4///46"""

DEBUG = False

stages = ["seed", "soil", "fertilizer", "water", "light", "temp", "humidity", "location"]


memo = {}

def recurse_if_needed(maps, value, lowest, d):
    key = hash(str(maps) + str(value) + str(lowest) + str(d))
    new = memo.get(key)
    if new is None:
        new = get_fits(maps, value, lowest, d+1)
        memo[key] = new
    return new

def get_fits(maps, current, lowest=INF, d=0):

    if current > lowest:  # prune
        return lowest

    try:
        this_map = maps.pop(0)
    except IndexError:
        p.bugprint("\t"*d, "this branch returns", current)
        return current
    

    p.bugprint("\t"*d, "finding out where", stages[d], current, "fits!")
    
    value = current
    found_fit = False
    
    for this_range in this_map:

        p.bugprint("\t"*d, "checking range", this_range)
        # swap destination and source
        source, dest, length = this_range
        if source <= current <= source + length:            
            index = abs(current - source)
            p.bugprint("\t"*d, "FOUND! Corresponds to:", dest+index)
            value = dest + index
            new = recurse_if_needed(maps, value, lowest, d+1)
            value = min([new, value])
            found_fit = True

    if not found_fit:
        value = recurse_if_needed(maps, value, lowest, d+1)
        

    return value


def solve(data):
    count = 0
    seed_data = list(data[0][8:].split())
    seed_ranges = []
    while seed_data:
        start, length = int(seed_data.pop(0)), int(seed_data.pop(0))
        seed_ranges.append(range(start, start+length))
    
    maps = []

    lowest_poss = INF
    for row in data[1:]:
        
        if not row.strip(): continue

        p.bugprint (" row is ", row)
        if "map:" in row:
            maps.append([])
        else:           
            maps[-1].append(list(map(int, row.split())))
            if maps[-1][1] <= lowest_poss:
                lowest_poss = maps[-1][1]

    p.bugprint(maps)

    ## reverse the maps to go backwards
    maps = reversed(maps)

    test_location = lowest_poss
    while True:
        seed = return_to_seed(location)
        print("Location {location} comes from seed {seed}")
        for seed_range in seed_ranges:
            if seed in seed_range:
                return result

            
            
            
            




            
        
        
        

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
