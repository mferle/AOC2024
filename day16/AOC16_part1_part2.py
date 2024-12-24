from collections import defaultdict
from AOCutil_read_maze import read_maze

class Part1Part2():

    def __init__(self, lines):
        self.maze, self.start_pos, self.end_pos = read_maze(lines)
        self.start_fac = (1, 0)

    def find_lowest(self):
        # initialize position and facing
        q = [(self.start_pos, self.start_fac)]
        all_costs = defaultdict(lambda:9999999999)
        all_costs = {(self.start_pos, self.start_fac): 0}

        while q:
            # take first element from list of position and facing to use in iteration
            pos, fac = q.pop()
            # get current cost
            curr_cost = all_costs[(pos, fac)]

            # get all neighbors
            new_points = {}
            # turn 90 degrees up or down
            if fac in [(1, 0), (-1, 0)]:
                new_points[pos, (0, 1)] = 1000
                new_points[pos, (0, -1)] = 1000
            # turn 90 degrees left or right
            if fac in [(0, 1), (0, -1)]:
                new_points[pos, (1, 0)] = 1000
                new_points[pos, (-1, 0)] = 1000
            # move in the same direction
            new_points[(pos[0] + fac[0], pos[1] + fac[1]), fac] = 1

            # for each neighbor
            for new_state, cost_incr in new_points.items():
                pp, new_fac = new_state
                # check if blocked
                if self.maze[pp] == "#":
                    continue
                new_cost = curr_cost + cost_incr
                # check if the new point was already visited with a lower cost
                if (pp, new_fac) in all_costs and all_costs[(pp, new_fac)] <= new_cost:
                    continue

                # add to all costs
                all_costs[(pp, new_fac)] = new_cost
                # append to nodes to visit
                q.append((pp, new_fac))

        # find the lowest cost for the end position
        lowest = 999999999999
        for c in all_costs:
            if c[0] == self.end_pos:
                if all_costs[c] < lowest:
                    lowest = all_costs[c]
                    end_fac = c[1]

        return lowest, all_costs, end_fac

    def part1(self) -> int:
        lowest, all_costs, end_fac = self.find_lowest()
        return lowest

    def part2(self) -> int:
        lowest, all_costs, end_fac = self.find_lowest()

        # initialize list of locations
        locations = {self.end_pos}
        candidates = {(self.end_pos, end_fac)}
        while candidates:
            curr_pos = candidates.pop()
            cost = all_costs[curr_pos]

            # get previous points
            prev_points = {}
            # turn 90 degrees up or down
            if curr_pos[1] in [(1, 0), (-1, 0)]:
                prev_points[curr_pos[0], (0, 1)] = 1000
                prev_points[curr_pos[0], (0, -1)] = 1000
            # turn 90 degrees left or right
            if curr_pos[1] in [(0, 1), (0, -1)]:
                prev_points[curr_pos[0], (1, 0)] = 1000
                prev_points[curr_pos[0], (-1, 0)] = 1000
            # move in the opposite direction
            prev_points[(curr_pos[0][0] - curr_pos[1][0], curr_pos[0][1] - curr_pos[1][1]), curr_pos[1]] = 1

            # loop through previous points
            for prev_state, cost_increase in prev_points.items():
                prev_loc, prev_fac = prev_state
                # check previous location
                if self.maze[prev_loc] == "#":
                    continue
                # add to costs
                if all_costs[prev_state] + cost_increase == cost:
                    candidates.add(prev_state)
                    locations.add(prev_loc)

        return len(locations)
