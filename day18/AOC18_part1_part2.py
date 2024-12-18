import math

class Part1Part2():

    def __init__(self, lines, exit, bytes):
        self.start_pos = (0, 0)
        self.end_pos = exit
        self.bytes = bytes
        self.incoming = []
        for l in lines:
            self.incoming.append((int(l.split(',')[0]), int(l.split(',')[1])))

    def print_mem(self, path):
        for j in range(self.end_pos[0] + 1):
            line = ''
            for i in range(self.end_pos[0] + 1):
                if (i, j) in self.incoming[0:self.bytes]:
                    line += '#'
                elif (i, j) in path:
                    line += 'O'
                else:
                    line += '.'

    def find_lowest(self, bytes):
        visited = set([(self.start_pos)])
        q = [(self.start_pos)]
        cost = 0

        cnt = 0
        while True:
            cnt += 1
            # no path found
            if len(q) == 0:
                return -1
            new_q = set()
            cost += 1

            # check all points
            for curr_pos in q:
                i = curr_pos[0]
                j = curr_pos[1]
                # get all neighbors
                for ii, jj in [(i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)]:
                    # if reached end
                    if (ii, jj) == self.end_pos:
                        return cost
                    # if out of memory space
                    if not (0 <= ii <= self.end_pos[0] and 0 <= jj <= self.end_pos[0]):
                        continue
                    # if corrupted
                    if (ii, jj) in self.incoming[0:bytes]:
                        continue
                    # if already visited
                    if (ii, jj) in visited:
                        continue

                    visited.add((ii, jj))
                    new_q.add((ii, jj))
            q = new_q

    def part1(self) -> int:
        # find the path with the lowest cost
        return self.find_lowest(self.bytes)
    
    def part2(self) -> str:
        # loop through all sequences of incoming byte positions
        for i in range(len(self.incoming)):
            # find the path wit the lowest cost for each
            cost = self.find_lowest(i)
            # if path not found, return the incoming value
            if cost == -1:
                return self.incoming[i-1]
