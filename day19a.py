from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 19
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}///19114
"""

DEBUG = True

g = globals()

def solve(data):
    ratings = 0
    workflows = {}
    g['workflows'] = workflows
    part_mode = False
    parts = []
    for row in data:
        
        
        if not row:
            part_mode = True
            continue

        if part_mode:
            for val in "xmas":
                row = row.replace(val+"=", f'"{val}":')
            parts.append(eval(row, g))

        else:
            name, body  = row.split("{")

            expression = "lambda x,m,a,s:"
            conditions = body[:-1].split(",")
            
            for e in conditions:
                if ":" in e:
                    condition, result = e.split(":")
                    result = f"workflows['{result}'](x,m,a,s)"
                    expression +=  result + f"if {condition} else ("
                else:
                    result = f"workflows['{e}'](x,m,a,s)"
                    expression += result + (")" * (len(conditions)-1))
            if expression.endswith("else ("):
                expression = expression[:6] + (")" * (len(conditions)-1))

            print(name, "=", expression)
            workflows[f"{name}"] = eval(expression, g)
            print(workflows)


    accepted = 0
    rejected = 0
    
    
    workflows['A'] = lambda x,m,a,s: True
    workflows['R'] = lambda x,m,a,s: False

    for part in parts:
        if workflows['in'](**part):
            this_rating = sum(part.values())
     
            ratings += this_rating


        

        

        
    

    return ratings




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
