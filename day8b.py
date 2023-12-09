from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

from math import lcm, inf as INF
PP_ARGS = False, False #rotate, cast int

DAY = 8
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)///6"""

DEBUG = True

node_map = {}

STEP_LIMIT = 5000000

class Node:
    def __init__(self, data):
        
        self.data = data
        self.left = None
        self.right = None
        self.steps_before_cycle = None
        self.z_nodes_passed = {}
        
    def hash(self):
        self.hash = hash(self.data + self.left.data + self.right.data)

    def __str__(self):
        return self.data

    def get_travel_time_to(self, z_nodes, instructions):

        steps_to_end_nodes = {z:[] for z in z_nodes}

        node = self
        steps = 0

        visited = Counter(hash(z) for z in z_nodes)

        while [] in steps_to_end_nodes.values():

            ins = instructions.pop(0)
            instructions.append(ins)

            node = node.left if ins == "L" else node.right

            visited[hash(node)] += 1

            if node in z_nodes and len(steps_to_end_nodes[node]) < 2:                
                print(f"{self} gets to {node} time in {steps} steps")
                steps_to_end_nodes[node].append(steps)

            steps += 1

            if steps > STEP_LIMIT:
                for z in steps_to_end_nodes:
                    if steps_to_end_nodes[z] == []:
                        
                        print(f"{self} can't ever get to {z} even after {steps} steps")
                break
        return steps_to_end_nodes
        



def get_or_make_node(key):
    node = node_map.get(key)
    if node is None:
        node = Node(key)
        node_map[key] = node
    return node

        
        

    

    


def solve(data):
    count = 0

    instructions = data[0]

    start_nodes, end_nodes = [], []

    for row in data[2:]:
        root, conns = row.split(" = ")
        
        left, right = conns.split(", ")
        node = get_or_make_node(root)
        node.left = get_or_make_node(left[1:])
        node.right = get_or_make_node(right[:-1])
        node.hash()
        if root[-1] == "A":
            start_nodes.append(node)
        elif root[-1] == "Z":
            end_nodes.append(node)

    results = []
    ## every A to every Z
    for a_node in start_nodes:        
        steps_to_end_nodes = a_node.get_travel_time_to(end_nodes, list(instructions))
 
        for step in steps_to_end_nodes.values():
            if len(step) == 0:  continue
            cycle_steps = step[1] - step[0]
            results.append(cycle_steps)


    print(results)
    return lcm(*results)



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
