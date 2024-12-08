class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
        self.w = len(self.lines[0])
        self.h = len(self.lines)

        # initialize antennas: list of locations for each frequency
        self.antennas = {}
        for i in range(self.w):
            for j in range(self.h):
                if self.lines[i][j] != '.':
                    if self.lines[i][j] not in self.antennas:
                        self.antennas[self.lines[i][j]] = [(i, j)]
                    else:
                        curr_list = self.antennas[self.lines[i][j]]
                        curr_list.append((i, j))
                        self.antennas[self.lines[i][j]] = curr_list

    def get_antinodes(self, kmax):
        all_antinodes = []

        # for each antenna frequency
        for a in self.antennas:
            curr_list = self.antennas[a]
            # get all pairs of antennas
            for i in range(len(curr_list)):
                for j in range(len(curr_list) - i - 1):
                    a1 = curr_list[i]
                    a2 = curr_list[j + i + 1]
                    # calculate the vector in each direction
                    v1 = (a1[0] - a2[0], a1[1] - a2[1])
                    v2 = (a2[0] - a1[0], a2[1] - a1[1])
                    # calculate antinode candidates by adding each vector to each antenna in the pair k-times
                    antinode_candidates = []
                    for k in range(kmax):
                        antinode_candidates.append((a1[0] + (k+1)*v1[0], a1[1] + (k+1)*v1[1]))
                        antinode_candidates.append((a1[0] + (k+1)*v2[0], a1[1] + (k+1)*v2[1]))
                        antinode_candidates.append((a2[0] + (k+1)*v1[0], a2[1] + (k+1)*v1[1]))
                        antinode_candidates.append((a2[0] + (k+1)*v2[0], a2[1] + (k+1)*v2[1]))
                    for n in antinode_candidates:
                        # for Part 1, must not be in the antenna position
                        if kmax==1 and (n == a1 or n == a2):
                            continue
                        # must be in grid
                        if n[0] < 0 or n[0] >= self.w or n[1] < 0 or n[1] >= self.h:
                            continue
                        all_antinodes.append(n)

        return len(set(all_antinodes))

    def part1(self) -> int:
        return self.get_antinodes(1)
    
    def part2(self) -> int:
        return self.get_antinodes(self.w)
