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
PROCS = 8

stages = ["seed", "soil", "fertilizer", "water", "light", "temp", "humidity", "location"]

def create_logger():
    import multiprocessing, logging
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(\
        '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
    handler = logging.FileHandler('loggy.txt')
    handler.setFormatter(formatter)

    # this bit will make sure you won't have 
    # duplicated messages in the output
    if not len(logger.handlers): 
        logger.addHandler(handler)
    return logger

def return_to_seed(value, maps):    
    i = 0
    while i < len(maps):
        for this_range in maps[i]:
            source, dest, length = this_range
            if source <= value <= source + length:            
                index = abs(value - source)                
                value = dest + index
                break
        i += 1
    return value
        

def solve(data):
    count = 0

    seed_data = list(data[0][7:].split())
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


    p.bugprint(maps)

    ## reverse the maps to go backwards
    maps = list(reversed(maps))

    return construct_tests(maps, seed_ranges)

def test_locations(final_tests):
    logger = create_logger()
    logger.info('Starting pooling')
 
    test_location, end_location, maps, seed_ranges = final_tests
    print(f"This proc will iterate from {test_location} to {end_location}")
    while test_location < end_location:
        seed = return_to_seed(test_location, maps)
        #print(f"Location {test_location} comes from seed {seed}")
        for seed_range in seed_ranges:
            if seed in seed_range:                
                return test_location

        test_location += 1
    return INF
    

def construct_tests(maps, seed_ranges):
    tests = list(range(0, SEARCH_SPACE, SEARCH_SPACE//PROCS))
    print("Starting a pool party...")
    with multiprocessing.Pool() as pool:
        final_tests = [[[tests[i], tests[i+1], maps, seed_ranges]] for i in range(len(tests)-1)]        
        x = pool.starmap(test_locations, final_tests)
    print("The pool party's over!!!")
    return min(x)
        


SEARCH_SPACE = 100

logger = create_logger()
logger.info('Starting pooling')

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    
    if p.check(TESTS, solve):
        SEARCH_SPACE = 251346198
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
