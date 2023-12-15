from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from collections import OrderedDict


PP_ARGS = False, False #rotate, cast int

DAY = 15
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7///145"""

DEBUG = False

def hash(step):
    current = 0
    for char in step:
        current += ord(char)
        current *= 17
        current %= 256
    return current

def parse_lens(step):

    if step.endswith("-"):
        return step[:-1], "-", None
    else:
        label, focal = step.split("=")
        return label, "=", focal

class Box:

    def __init__(self):
        self.data = []

    def replace(self, key, new_key, new_val):
        for i, item in enumerate(self.data):
            if item[0] == key:
                
                self.data[i] = (new_key, new_val)
                return True
        return False

    def append(self, new_key, new_val):
        p.bugprint("append")
        self.data.append((new_key, new_val))

    def pop(self, key):
        p.bugprint("pop")

        for i, item in enumerate(self.data):
            if item[0] == key:
                break
        else:
            return False

        self.data.pop(i)
        return True

    def display(self, idx):
        if self.data:
            p.bugprint(f"Box {idx}: {self.data}")

def solve(data):
    total = 0
    boxes = [Box() for _ in range(256)]
    lenses = data[0].split(",")
        
    for step in lenses:
        print(step)

        label, op, focal = parse_lens(step)
        idx = hash(label)
        box = boxes[idx]

        if "-" in step:

            if not box.pop(label):

                p.bugprint(f"Couldn't remove {label} not found in box {idx}")
            
        else:
  
            if not box.replace(label, label, focal):
                box.append(label, focal)
                
            
            
        p.bugprint(f"After '{step}'")
        for i in range(len(boxes)):
            boxes[i].display(i)


    for box_num in range(len(boxes)):
        box = boxes[box_num]
        box_num += 1
        p.bugprint("This box has", box.data)
        for slot_num, lens in enumerate(box.data):
            
            slot_num += 1
            foc_power = box_num * slot_num * int(lens[1])
            p.bugprint(f"{lens[0]}: {box_num} (box {box_num}) * {slot_num} (slot num) * {lens[1]} (focal length) = {foc_power}")
  
            total += foc_power

    return total
        



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
