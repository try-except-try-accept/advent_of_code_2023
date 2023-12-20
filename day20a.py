from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 20
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """a,a///aa
"""

DEBUG = True

machine = {}

def get_or_make_module(code):
    module = machine.get(code)
    if module is None:
        sign = code[0]
        name = code[1:]
        if sign == "%":
            module = FlipFlop(name)
        elif sign == "&":
            module = Conjunction(name)
        else:
            module = Broadcaster(name)
    return module

class Module:
    def __init__(self, name):
        self.name = name
        self.destinations = []
        self.origin = None
        self.sending = None
        self.received = None


class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False

    def process(self):
        if self.signal == False:
            self.state = not self.state
        self.sending = self.state

class Conjunction(Module):
    def __init__(self, name, num_inputs):
        super().__init__(name)
        self.memory = [False for _ in range(self)]

    def process(self, sent_from):
        self.memory[sent_from] = self.received
        self.sending = not all(self.memory)
        

class Broadcaster:  
    def __init__(self, name):
        super().__init__(name)


def send_pulse():

    name = "broadcaster"
    signal_q = [False]
    module_q = [machine['broadcaster']]
    
    while True:
        current = module_q.pop(0)
        current.process()

        for destination in current.destination():
            destination.received = new_signal.sending
            module_q.append(destination)

        

def solve(data):
    for row in data:
        node, destinations = row.split(" -> ")
        destinations = destinations.split(", ")

        node = get_or_make_module(node)
        for d in destinations:
            d = get_or_make_module(d)
            node.destinations.append(d)
            d.origin = node




    return send_pulse()


    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
