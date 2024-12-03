import re
class Part1Part2():

    def __init__(self, program):
        self.program = program
    
    def calc_mul(self, pgm) -> int:
        # initialize total
        total = 0

        pgms = pgm.split('mul(')
        print(pgms, '\n')

        for str in pgms:
        #print(str)
            x = re.search("^[0-9]*,[0-9]*\)", str)
            if x:
                #print('*** ', x.group())
                mult = x.group()[:-1].split(',')
                #print(mult)
                total += int(mult[0]) * int(mult[1])

        return total

    def part1(self) -> int:
        # initialize total
        total = 0

        total += self.calc_mul(self.program)

        return total

    def part2(self) -> int:
        # initialize total
        total = 0

        pdn = re.split('(do\(\)|don\'t\(\))', 'do()' + self.program)
        do_or_not = False
        for s in pdn:
            if s == 'do()':
                do_or_not = True
            elif s == 'don\'t':
                do_or_not = False
            elif do_or_not:
                total += self.calc_mul(s)
                do_or_not = False

        return total