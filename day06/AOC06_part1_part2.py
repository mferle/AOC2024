import copy

class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
        self.w = len(self.lines[0])
        self.h = len(self.lines)
    
        # initialize obstacles and starting position and direction
        self.obstacles = []
        for i in range(self.w):
            for j in range(self.h):
                if self.lines[i][j] == '#':
                    self.obstacles.append((i, j))
                elif self.lines[i][j] == '^':
                    # mark starting position and direction
                    self.pos = (i, j)
                    self.direction = 'up'

    def walk_grid(self, pos, direction, obstacles):
        # remember already visited nodes with the direction
        previously_visited = [(pos, direction)]

        # add starting position to visited nodes
        visited = [pos]

        # go until not out of grid or reached original position
        while (pos[0] >= 0 and pos [0] < self.w and pos[1] >= 0 and pos[1] < self.h):
            started = True
            # define vector depending on direction
            if direction == 'up':
                vector = (-1, 0)
            elif direction == 'down':
                vector = (1, 0)
            elif direction == 'right':
                vector = (0, 1)
            else:
                vector = (0, -1)
            # calculate next position
            next_pos = (pos[0] + vector[0], pos[1] + vector[1])
            # if not obstacle, add to visited
            if next_pos not in obstacles:
                pos = next_pos
                visited.append(pos)
            # otherwise change direction
            else:
                if direction == 'up':
                    new_direction = 'right'
                elif direction == 'right':
                    new_direction = 'down'
                elif direction == 'down':
                    new_direction = 'left'
                else:
                    new_direction = 'up'
                direction = new_direction

            if (pos, direction) in previously_visited:
                return visited[:-1], True
            else:
                previously_visited.append((pos, direction))

        # remove the last node because it is out of the grid or already visited
        return visited[:-1], False

    def part1(self) -> int:

        visited, is_loop = self.walk_grid(self.pos, self.direction, self.obstacles)

        # return number of distinct nodes
        return len(set(visited))

    def part2(self) -> int:
        # initialize total
        total = 0

        # get a list of visited nodes from Part 1
        visited, is_loop = self.walk_grid(self.pos, self.direction, self.obstacles)

        # create list of candidate obstacles, taking only unoccupied and visited nodes
        candidate_obstacles = []
        for i in range(self.w):
            for j in range(self.h):
                if self.lines[i][j] != '#' and self.lines[i][j] != '^':
                    if (i, j) in visited:
                        candidate_obstacles.append((i, j))
        
        # walk the grid for each obstacle
        for idx, obst in enumerate(candidate_obstacles):
            #print(f"Processing {idx}/{len(candidate_obstacles)}")
            obstacles = copy.deepcopy(self.obstacles)
            obstacles.append(obst)

            visited, is_loop = self.walk_grid(self.pos, self.direction, obstacles)

            if is_loop:
                total += 1

        return total
