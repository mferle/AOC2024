class Part1Part2():

    def __init__(self, lines, w, h):
        self.w = w
        self.h = h
        # initialize list of robots
        self.robots = []
        # parse input into the list of robots
        for l in lines:
            pv = l.split()
            position = pv[0].replace('p=', '')
            velocity = pv[1].replace('v=', '')
            p = position.split(',')
            v = velocity.split(',')
            self.robots.append([(int(p[0]), int(p[1])), (int(v[0]), int(v[1]))])

    def n_seconds(self, robots, n):
        # take list of robots and their velocities and return the list after one second
        new_robots = []
        for r in robots:
            pos = r[0]
            vel = r[1]
            new_pos = ((pos[0] + vel[0]*n) % self.w, (pos[1] + vel[1]*n) % self.h)
            new_robots.append([(new_pos), (vel)])
        return new_robots
    
    def part1(self) -> int:
        # define number of seconds
        seconds = 100

        # move all seconds at once
        robots_moved = self.n_seconds(self.robots, seconds)

        # define the quadrants
        q1 = ((0, 0), (self.w // 2, self.h // 2))
        q2 = ((self.w // 2 + 1, 0), (self.w, self.h // 2))
        q3 = ((0, self.h // 2 + 1), (self.w // 2, self.h))
        q4 = ((self.w // 2 + 1, self.h // 2 + 1), (self.w, self.h))

        # initialize total for each quadrant
        q1tot = 0
        q2tot = 0
        q3tot = 0
        q4tot = 0

        # for each robot
        for r in robots_moved:
            pos = r[0]
            # check each quadrant and if the robot's position is in the quadrant, add to total
            if q1[0][0] <= pos[0] < q1[1][0] and q1[0][1] <= pos[1] < q1[1][1]:
                q1tot += 1
            if q2[0][0] <= pos[0] < q2[1][0] and q2[0][1] <= pos[1] < q2[1][1]:
                q2tot += 1
            if q3[0][0] <= pos[0] < q3[1][0] and q3[0][1] <= pos[1] < q3[1][1]:
                q3tot += 1
            if q4[0][0] <= pos[0] < q4[1][0] and q4[0][1] <= pos[1] < q4[1][1]:
                q4tot += 1

        # multiply the totals
        total = q1tot * q2tot * q3tot * q4tot

        return total

    def part2(self) -> int:
        total = 0

        # repeat moving the robot and find out in which second the standard deviation of robot distribution changes significantly
        # i direction
        seconds = 0
        stddev_list = []
        found_offset = False
        while not found_offset:
            seconds += 1
            # calculate the robot positions after each second
            robots_moved = self.n_seconds(self.robots, seconds)

            # calculate how many robots in each column
            bunches = []
            for i in range(self.w):
                bunch = 0
                for j in range(self.h):
                    for r in robots_moved:
                        if (i, j) == (r[0][0], r[0][1]):
                            bunch += 1
                bunches.append(bunch)

            # calculate the standard deviation
            mean = sum(bunches) / len(bunches) 
            variance = sum([((x - mean) ** 2) for x in bunches]) / len(bunches) 
            stddev = variance ** 0.5

            # check if current standard deviation is significantly higher than the average of the previous
            if len(stddev_list) > 0:
                if stddev > 2*(sum(stddev_list)/len(stddev_list)):
                    found_offset = True
                    i_offset = seconds - 1
            stddev_list.append(stddev)

        # j direction
        seconds = 0
        stddev_list = []
        found_offset = False
        while not found_offset:
            seconds += 1
            # calculate the robot positions after each second
            robots_moved = self.n_seconds(self.robots, seconds)

            # calculate how many robots in each column
            bunches = []
            for j in range(self.h):
                bunch = 0
                for i in range(self.w):
                    for r in robots_moved:
                        if (i, j) == (r[0][0], r[0][1]):
                            bunch += 1
                bunches.append(bunch)

            # calculate the standard deviation
            mean = sum(bunches) / len(bunches) 
            variance = sum([((x - mean) ** 2) for x in bunches]) / len(bunches) 
            stddev = variance ** 0.5

            # check if current standard deviation is significantly higher than the average of the previous
            if len(stddev_list) > 0:
                if stddev > 2*(sum(stddev_list)/len(stddev_list)):
                    found_offset = True
                    j_offset = seconds - 1
            stddev_list.append(stddev)

        # find when both offsets intersect
        i = 0
        while True:
            i += 1
            if i % 101 == i_offset and i % 103 == j_offset:
                total = i + 1
                break

        # after finding the result, move the original robots for that many seconds and print the layout - should see the christmas tree
        robots_moved = self.n_seconds(self.robots, total)

        for i in range(self.w):
            line = ''
            for j in range(self.h):
                sym = '.'
                for r in robots_moved:
                    if r[0][0] == j and r[0][1] == i:
                        sym = '*'
                line = line + sym
            print(line)

        return total
