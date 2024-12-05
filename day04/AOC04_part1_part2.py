class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
        self.w = len(self.lines[0])
        self.h = len(self.lines)
    
    def part1(self) -> int:
        # initialize total
        total = 0

        # for each cell in the grid
        for i in range(self.w):
            for j in range(self.h):
                # always starts with X
                if self.lines[i][j] != 'X':
                    continue
                # found X, now find all neighbors
                for ii in [i-1, i, i+1]:
                    for jj in [j-1, j, j+1]:
                        # skip current cell
                        if (ii, jj) == (i, j):
                            continue
                        # check if the neighbor is within boundaries
                        if ii < 0 or ii >= self.w or jj < 0 or jj >= self.h:
                            continue
                        # check if neighbor is M
                        if self.lines[ii][jj] != 'M':
                            continue
                        # found M, now calculate the vector and continue in the same direction
                        vector = (ii - i, jj - j)
                        # calculate position of A
                        (ia, ja) = (ii + vector[0], jj + vector[1])
                        # check if position is within boundaries
                        if ia < 0 or ia >= self.w or ja < 0 or ja >= self.h:
                            continue
                        # check if value is A
                        if self.lines[ia][ja] != 'A':
                            continue
                        # found A, now calculate position of S
                        (iis, js) = (ia + vector[0], ja + vector[1])
                        # check if position is within boundaries
                        if iis < 0 or iis >= self.w or js < 0 or js >= self.h:
                            continue
                        # if the value is S, add to total
                        if self.lines[iis][js] == 'S':
                            total += 1
        return total

    def part2(self) -> int:
        # initialize total
        total = 0

        # for each cell in the grid
        for i in range(self.w):
            for j in range(self.h):
                # look for A
                if self.lines[i][j] != 'A':
                    continue
                # found A, now find all neighbors diagonally
                top_left = (i-1, j-1)
                top_rght = (i+1, j-1)
                bot_left = (i-1, j+1)
                bot_rght = (i+1, j+1)
                # check if neighbors are within boundaries
                if    top_left[0] >= 0 and top_left[0] < self.w and top_left[1] >= 0 and top_left[1] < self.h \
                    and top_rght[0] >= 0 and top_rght[0] < self.w and top_rght[1] >= 0 and top_rght[1] < self.h \
                    and bot_left[0] >= 0 and bot_left[0] < self.w and bot_left[1] >= 0 and bot_left[1] < self.h \
                    and bot_rght[0] >= 0 and bot_rght[0] < self.w and bot_rght[1] >= 0 and bot_rght[1] < self.h:
                    # check diagonals, must be M and S or S and M on each diagonal
                    if   ((self.lines[top_left[0]][top_left[1]] == 'M' and self.lines[bot_rght[0]][bot_rght[1]] == 'S') \
                        or (self.lines[top_left[0]][top_left[1]] == 'S' and self.lines[bot_rght[0]][bot_rght[1]] == 'M')) \
                    and  ((self.lines[top_rght[0]][top_rght[1]] == 'M' and self.lines[bot_left[0]][bot_left[1]] == 'S') \
                        or (self.lines[top_rght[0]][top_rght[1]] == 'S' and self.lines[bot_left[0]][bot_left[1]] == 'M')):
                        # all criteria fulfilled, add to total
                        total += 1
        return total
