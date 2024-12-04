class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
    
    def part1(self) -> int:
        # initialize total
        total = 0

        candidates = []
        # for each cell in the grid
        for i in range(len(self.lines[0])):
            for j in range(len(self.lines)):
                # always starts with X
                if self.lines[i][j] == 'X':
                    # find all neighbors
                    for ii in [i-1, i, i+1]:
                        for jj in [j-1, j, j+1]:
                            # skip current cell
                            if (ii, jj) != (i, j):
                                # check if within boundaries
                                if ii >= 0 and ii < len(self.lines[0]) and jj >= 0 and jj < len(self.lines):
                                    # if neighbor is M, add to candidates
                                    if self.lines[ii][jj] == 'M':
                                        candidates.append([(i, j), (ii, jj)])

        # loop for all candidates
        for cnd in candidates:
            # calculate the vector
            vector = (cnd[1][0] - cnd[0][0], cnd[1][1] - cnd[0][1])
            # calculate position of A
            ia = cnd[1][0] + vector[0]
            ja = cnd[1][1] + vector[1]
            # check if position is within boundaries
            if ia >= 0 and ia < len(self.lines[0]) and ja >= 0 and ja < len(self.lines):
                # if the value is A, continue searching for S
                if self.lines[ia][ja] == 'A':
                    # calculate position of S
                    iis = ia + vector[0]
                    js = ja + vector[1]
                    # check if position is within boundaries
                    if iis >= 0 and iis < len(self.lines[0]) and js >= 0 and js < len(self.lines):
                        # if the value is S, add to total
                        if self.lines[iis][js] == 'S':
                            total += 1
        return total

    def part2(self) -> int:
        # initialize total
        total = 0

        # for each cell in the grid
        for i in range(len(self.lines[0])):
            for j in range(len(self.lines)):
                # look for A
                if self.lines[i][j] == 'A':
                    #print(i, j)
                    # find all neighbors diagonally
                    top_left = (i-1, j-1)
                    top_rght = (i+1, j-1)
                    bot_left = (i-1, j+1)
                    bot_rght = (i+1, j+1)
                    # check if neighbors are within boundaries
                    if    top_left[0] >= 0 and top_left[0] < len(self.lines[0]) and top_left[1] >= 0 and top_left[1] < len(self.lines) \
                      and top_rght[0] >= 0 and top_rght[0] < len(self.lines[0]) and top_rght[1] >= 0 and top_rght[1] < len(self.lines) \
                      and bot_left[0] >= 0 and bot_left[0] < len(self.lines[0]) and bot_left[1] >= 0 and bot_left[1] < len(self.lines) \
                      and bot_rght[0] >= 0 and bot_rght[0] < len(self.lines[0]) and bot_rght[1] >= 0 and bot_rght[1] < len(self.lines):
                        # check diagonals, must be M and S or S and M on each diagonal
                        if   ((self.lines[top_left[0]][top_left[1]] == 'M' and self.lines[bot_rght[0]][bot_rght[1]] == 'S') \
                           or (self.lines[top_left[0]][top_left[1]] == 'S' and self.lines[bot_rght[0]][bot_rght[1]] == 'M')) \
                        and  ((self.lines[top_rght[0]][top_rght[1]] == 'M' and self.lines[bot_left[0]][bot_left[1]] == 'S') \
                           or (self.lines[top_rght[0]][top_rght[1]] == 'S' and self.lines[bot_left[0]][bot_left[1]] == 'M')):
                            total += 1
        return total
