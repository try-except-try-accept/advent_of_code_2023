import multiprocessing
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

stages = ["soil", "fertilizer", "water", "light", "temp", "humidity", "location"]


memo = {}

def return_to_seed(value, lowest=INF, d=0):
    global maps
    orig = value
    i = 0
    while i < len(maps):
        this_map = maps[i]
        
        for this_range in this_map:            

            source, dest, length = this_range
            if source <= value <= source + length:            
                index = abs(value - source)        
                value = dest + index
                break
        d -= 1
        i += 1

    for seed_range in seed_ranges:
        if value in seed_range:
            print("Found!", orig)
            

def trace_back_to_seed(test_locations):
    with multiprocessing.Pool() as pool:
        pool.map(return_to_seed, test_locations)


def solve(data):
    global maps
    count = 0
    seed_data = list(data[0][7:].split())
    seed_ranges = []

    while seed_data:
        start, length = int(seed_data.pop(0)), int(seed_data.pop(0))
       
        seed_ranges.append(range(start, start+length))
    
    maps = []

    lowest = INF
    for row in data[1:]:
        
        if not row.strip(): continue


        if "map:" in row:
            maps.append([])
        else:           
            maps[-1].append(list(map(int, row.split())))
           
            dest = maps[-1][-1][1]
            if dest < lowest:
                lowest = dest

    ## reverse the maps to go backwards
    maps = list(reversed(maps))
    p.bugprint("Seed ranges")
    p.bugprint(seed_ranges)



    test_location = lowest
    trace_back_to_seed(list(range(1, 100)))
        
    




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        print("passed")
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
