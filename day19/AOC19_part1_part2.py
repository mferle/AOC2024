from functools import cache

class Part1Part2():

    def __init__(self, lines):
        self.designs = []
        for idx, l in enumerate(lines):
            if idx == 0:
                self.towels = [c.strip() for c in l.split(',')]
            elif len(l) > 0:
                self.designs.append(l)

    # recursive function to find if the beginning of the string matches a towel and sends the remainder to itself
    @cache
    def find_arr(self, des):
        # arrangement found, no remainder
        if des == '':
            return 1
        else:
            # assume no matches
            arr_cnt = 0
            # for each towel, check for arrangements
            for t in self.towels:
                if des.startswith(t):
                    arr_cnt += self.find_arr(des[len(t):])
            return arr_cnt

    def part1(self) -> int:
        total = 0
        # count how many designs have arrangements
        for idx, des in enumerate(self.designs):
            c = self.find_arr(des)
            if c > 0:
                total += 1

        return total
    
    def part2(self) -> str:
        total = 0
        # sum the total number of arrangements
        for idx, des in enumerate(self.designs):
            total += self.find_arr(des)

        return total
