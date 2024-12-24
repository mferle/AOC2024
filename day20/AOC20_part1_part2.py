from collections import defaultdict
from AOCutil_read_maze import read_maze

class Part1Part2():

    def __init__(self, lines):
        self.maze, self.start_pos, self.end_pos = read_maze(lines)
        self.w = len(lines[0])
        self.h = len(lines)

    def find_lowest(self, maze):
        # initialize position
        q = [(self.start_pos)]
        all_costs = defaultdict(lambda:9999999999)
        all_costs = {(self.start_pos): 0}

        while q:
            # take first element from list of positions to use in iteration
            pos = q.pop()
            # get current cost
            curr_cost = all_costs[(pos)]

            # get all neighbors
            new_points = {}
            new_points[(pos[0] + 1, pos[1])] = 1
            new_points[(pos[0] - 1, pos[1])] = 1
            new_points[(pos[0], pos[1] + 1)] = 1
            new_points[(pos[0], pos[1] - 1)] = 1

            # for each neighbor
            for new_state, cost_incr in new_points.items():
                # check if blocked
                if maze[new_state] == '#':
                    continue
                new_cost = curr_cost + cost_incr
                # check if the new point was already visited with a lower cost
                if (new_state) in all_costs and all_costs[new_state] <= new_cost:
                    continue

                # add to all costs
                all_costs[new_state] = new_cost
                # append to nodes to visit
                q.append(new_state)

        # find the lowest cost for the end position
        lowest = all_costs[self.end_pos]

        return lowest

    def part1(self) -> int:
        initial_lowest = self.find_lowest(self.maze)

        inner_walls = []
        for m in self.maze:
            if 0 < m[0] < self.h - 1 and 0 < m[1] < self.w - 1:
                inner_walls.append(m)

        all_cheats = defaultdict(int)
        for w in inner_walls:
            cheat_maze = self.maze.copy()
            cheat_maze[w] = '.'
            one_cheat = initial_lowest - self.find_lowest(cheat_maze)
            all_cheats[one_cheat] += 1
        
        total = 0
        for p in all_cheats:
            if p >= 100:
                total += all_cheats[p]

        return total
    
    def part2(self) -> str:
        total = 0

        # ToDo

        return total
