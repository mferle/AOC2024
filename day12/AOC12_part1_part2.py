from collections import deque

class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
        self.w = len(self.lines[0])
        self.h = len(self.lines)

        # initialize dictionary with the plant as id and a list of all points
        self.plants = {}
        # initialize a list of all points in the grid
        self.points = deque()

        # populate the plant dictionary and list o fpoints
        for i in range(self.w):
            for j in range(self.h):
                p = lines[i][j]
                if p in self.plants:
                    self.plants[p] = self.plants[p] + [(i,j)]
                else:
                    self.plants[p] = [(i,j)]
                self.points.append((i, j))

    def part1(self) -> int:
        total = 0
        total2 = 0
        # initialize plot
        plots = []

        while len(self.points) > 0:
            # get next plot
            plot = self.points.pop()
            # get the plant
            plant = self.lines[plot[0]][plot[1]]
            # get all positions of the plant
            all_plants = self.plants[plant]
            # initialize current plot
            curr_plot = set()
            curr_plot.add(plot)
            while True:
                new_plot = set()
                for p in curr_plot:
                    new_plot.add(p)
                # loop through all points in the current plot and find adjacent points
                # when adjacent point is found, add it to the new plot and remove it from the list of all points
                for p in curr_plot:
                    if (p[0]+1, p[1]) in all_plants:
                        new_plot.add((p[0]+1, p[1]))
                        try:
                            fnd = self.points.index((p[0]+1, p[1]))
                            self.points.remove((p[0]+1, p[1]))
                        except:
                            pass
                    if (p[0]-1, p[1]) in all_plants:
                        new_plot.add((p[0]-1, p[1]))
                        try:
                            fnd = self.points.index((p[0]-1, p[1]))
                            self.points.remove((p[0]-1, p[1]))
                        except:
                            pass
                    if (p[0], p[1]+1) in all_plants:
                        new_plot.add((p[0], p[1]+1))
                        try:
                            fnd = self.points.index((p[0], p[1]+1))
                            self.points.remove((p[0], p[1]+1))
                        except:
                            pass
                    if (p[0], p[1]-1) in all_plants:
                        new_plot.add((p[0], p[1]-1))
                        try:
                            fnd = self.points.index((p[0], p[1]-1))
                            self.points.remove((p[0], p[1]-1))
                        except:
                            pass
                # if no new points were added, stop the loop
                if len(curr_plot) == len(new_plot):
                    break
                else:
                    # otherwise reset the variables and continue the loop
                    curr_plot = set()
                    for p in new_plot:
                        curr_plot.add(p)
            # append the current plot to the list of plots
            plots.append(curr_plot)

        # calculate the perimeter
        for one_plot in plots:
            perimeter = 0
            # for each plot
            for p in one_plot:
                # identify the plant
                plant = self.lines[p[0]][p[1]]
                # check in all four directions the neighboring plant
                # if plant is the same, there is no perimeter
                # if plant is different or at the edge of the grid, add 1 to perimeter
                if p[0]+1 >= self.h:
                    perimeter += 1
                else:
                    if self.lines[p[0]+1][p[1]] != plant:
                        perimeter += 1
                if p[0]-1 < 0:
                    perimeter += 1
                else:
                    if self.lines[p[0]-1][p[1]] != plant:
                        perimeter += 1
                if p[1]+1 >= self.w:
                    perimeter += 1
                else:
                    if self.lines[p[0]][p[1]+1] != plant:
                        perimeter += 1
                if p[1]-1 < 0:
                    perimeter += 1
                else:
                    if self.lines[p[0]][p[1]-1] != plant:
                        perimeter += 1
            # add to total for part 1
            total += perimeter * len(one_plot)

            # calculate perimeter for part 2
            perimeter_count = 0
            for p in one_plot:
                i, j = p[0], p[1]
                # check if outside corner
                if ((i+1, j+1) not in one_plot) and ((i+1, j) not in one_plot) and ((i, j+1) not in one_plot):
                    perimeter_count += 1
                if ((i-1, j-1) not in one_plot) and ((i-1, j) not in one_plot) and ((i, j-1) not in one_plot):
                    perimeter_count += 1
                if ((i+1, j-1) not in one_plot) and ((i+1, j) not in one_plot) and ((i, j-1) not in one_plot):
                    perimeter_count += 1
                if ((i-1, j+1) not in one_plot) and ((i-1, j) not in one_plot) and ((i, j+1) not in one_plot):
                    perimeter_count += 1
                # check if inside corner
                if ((i+1, j+1) not in one_plot) and ((i+1, j) in one_plot) and ((i, j+1) in one_plot):
                    perimeter_count += 1
                if ((i-1, j-1) not in one_plot) and ((i-1, j) in one_plot) and ((i, j-1) in one_plot):
                    perimeter_count += 1
                if ((i+1, j-1) not in one_plot) and ((i+1, j) in one_plot) and ((i, j-1) in one_plot):
                    perimeter_count += 1
                if ((i-1, j+1) not in one_plot) and ((i-1, j) in one_plot) and ((i, j+1) in one_plot):
                    perimeter_count += 1
                # check if diagonal
                if ((i+1, j+1) in one_plot) and ((i+1, j) not in one_plot) and ((i, j+1) not in one_plot):
                    perimeter_count += 1
                if ((i-1, j-1) in one_plot) and ((i-1, j) not in one_plot) and ((i, j-1) not in one_plot):
                    perimeter_count += 1
                if ((i+1, j-1) in one_plot) and ((i+1, j) not in one_plot) and ((i, j-1) not in one_plot):
                    perimeter_count += 1
                if ((i-1, j+1) in one_plot) and ((i-1, j) not in one_plot) and ((i, j+1) not in one_plot):
                    perimeter_count += 1

            total2 += perimeter_count * len(one_plot)
 
        return total, total2
