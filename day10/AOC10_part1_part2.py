    
class Part1Part2():

    def __init__(self, lines):
        self.lines = lines

        positions = {}
        # construct a dictionary with the height as key and all points for the given height as a list of values
        for i, l in enumerate(lines):
            for j, p in enumerate(l):
                if p == '.':
                    continue
                if int(p) in positions:
                    positions[int(p)] = positions[int(p)] + [(i, j)]
                else:
                    positions[int(p)] = [(i, j)]
        self.positions = positions

    def find_neighbor_pos(self, pos_list, search_height):
        # for a given list of points, construct a new list with neighboring points of the given height
        out_pos = []
        candidates = self.positions[search_height]
        for cp in pos_list:
            if (cp[0] + 1, cp[1]) in candidates:
                out_pos.append((cp[0] + 1, cp[1]))
            if (cp[0] - 1, cp[1]) in candidates:
                out_pos.append((cp[0] - 1, cp[1]))
            if (cp[0], cp[1] + 1) in candidates:
                out_pos.append((cp[0], cp[1] + 1))
            if (cp[0], cp[1] - 1) in candidates:
                out_pos.append((cp[0], cp[1] - 1))
        return out_pos
    
    def all_paths(self):
        # initialize total
        total1 = 0
        total2 = 0

        # get a list of all positions with height 0
        zero_list = self.positions[0]
        # for each 0 position
        for z in zero_list:
            curr_list = [z]
            curr_seek = 1

            # find neighboring points in increasing heights
            for i in range(len(self.positions) - 1):
                curr_list = self.find_neighbor_pos(curr_list, curr_seek)
                curr_seek += 1

            # count number of distinct positions with height 9 and add to total
            total1 += len(set(curr_list))
            # count number of all positions with height 9 and add to total
            total2 += len(curr_list)
    
        return total1, total2

    def part1(self) -> int:
        total1, total2 = self.all_paths()
        return total1

    def part2(self) -> int:
        total1, total2 = self.all_paths()
        return total2
