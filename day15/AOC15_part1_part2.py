import copy

class Part1Part2():

    def __init__(self, lines):
        self.h = 0
        # initialize grid
        self.grid = []
        self.moves = ''
        # parse input into grid
        for j, l in enumerate(lines):
            # if line starts with #
            if len(l) > 0 and l[0] == '#':
                self.w = len(l)
                one_line = []
                for i, c in enumerate(l):
                    # mark the start position
                    if c == '@':
                        self.start_pos = (i, j)
                        one_line.append('.')
                    else:
                        one_line.append(c)
                self.grid.append(one_line)
                self.h += 1
            # append all moves into a single line
            elif len(l) > 0 and l[0] in ['<', '^', '>', 'v']:
                self.moves = self.moves + l

        # initialize vectors and arrows
        self.vectors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.arrows = ['<', '^', '>', 'v']

    def print_grid(self, grid, pos):
        for j, g in enumerate(grid):
            line = ''
            for i, c in enumerate(g):
                if pos == (i, j):
                    line = line + '@'
                else:
                    line = line + c
            print(line)

    def part1(self) -> int:
        # current position
        pos = self.start_pos
        # current warehouse
        wh = copy.deepcopy(self.grid)

        # for each move
        for m in self.moves:
            v = self.vectors[self.arrows.index(m)]
            # calculate next position
            next_pos = (pos[0] + v[0], pos[1] + v[1])

            # if next position is a wall, do nothing
            if wh[next_pos[1]][next_pos[0]] == '#':
                pass
            # if next position is free, move
            elif wh[next_pos[1]][next_pos[0]] == '.':
                pos = next_pos
            # if next position is a box, figure out if it can be moved
            elif wh[next_pos[1]][next_pos[0]] == 'O':
                # check if there is free space at the end of a sequence of boxes
                can_move_box = False
                box_pos = next_pos
                while True:
                    next_box_pos = (box_pos[0] + v[0], box_pos[1] + v[1])
                    if wh[next_box_pos[1]][next_box_pos[0]] == 'O':
                        box_pos = next_box_pos
                    elif wh[next_box_pos[1]][next_box_pos[0]] == '.':
                        can_move_box = True
                        break
                    else:
                        break
                # if free space was found, move the box
                if can_move_box:
                    wh[next_pos[1]][next_pos[0]] = '.'
                    wh[next_box_pos[1]][next_box_pos[0]] = 'O'
                    pos = next_pos

        # calculate total
        total = 0
        for j in range(self.h):
            for i in range(self.w):
                if wh[j][i] == 'O':
                    total += 100*j + i
        return total

    def part2(self) -> int:
        # current warehouse - wide
        whw = []
        for l in self.grid:
            line = []
            for c in l:
                # If the tile is #, the new map contains ## instead.
                if c == '#':
                    line.append('#')
                    line.append('#')
                # If the tile is O, the new map contains [] instead.
                if c == 'O':
                    line.append('[')
                    line.append(']')
                # If the tile is ., the new map contains .. instead.
                if c == '.':
                    line.append('.')
                    line.append('.')
            whw.append(line)

        # If the tile is @, the new map contains @. instead.
        w_start_pos = (2*self.start_pos[0], self.start_pos[1])

        self.print_grid(whw, w_start_pos)

        # current position
        pos = w_start_pos

        # for each move
        for m in self.moves:
            v = self.vectors[self.arrows.index(m)]
            # calculate next position
            next_pos = (pos[0] + v[0], pos[1] + v[1])

            # if next position is a wall, do nothing
            if whw[next_pos[1]][next_pos[0]] == '#':
                pass
            # if next position is free, move
            elif whw[next_pos[1]][next_pos[0]] == '.':
                pos = next_pos
            # if next position is a box, figure out if it can be moved
            # ################
            # when moving left
            elif m == '<' and whw[next_pos[1]][next_pos[0]] in ('[', ']'):
                # check if there is free space at the end of a sequence of boxes
                can_move_box = False
                box_pos = next_pos
                while True:
                    next_box_pos = (box_pos[0] + v[0], box_pos[1] + v[1])
                    if whw[next_box_pos[1]][next_box_pos[0]] in ('[', ']'):
                        box_pos = next_box_pos
                    elif whw[next_box_pos[1]][next_box_pos[0]] == '.':
                        can_move_box = True
                        break
                    else:
                        break
                # if free space was found, move the box
                if can_move_box:
                    for k in range(next_box_pos[0], next_pos[0]):
                        whw[next_box_pos[1]][k] = whw[next_box_pos[1]][k+1]
                    whw[next_pos[1]][next_pos[0]] = '.'
                    pos = next_pos
            # #################
            # when moving right
            elif m == '>' and whw[next_pos[1]][next_pos[0]] in ('[', ']'):
                # check if there is free space at the end of a sequence of boxes
                can_move_box = False
                box_pos = next_pos
                while True:
                    next_box_pos = (box_pos[0] + v[0], box_pos[1] + v[1])
                    if whw[next_box_pos[1]][next_box_pos[0]] in ('[', ']'):
                        box_pos = next_box_pos
                    elif whw[next_box_pos[1]][next_box_pos[0]] == '.':
                        can_move_box = True
                        break
                    else:
                        break
                # if free space was found, move the box
                if can_move_box:
                    for k in range(next_box_pos[0], next_pos[0], -1):
                        whw[next_box_pos[1]][k] = whw[next_box_pos[1]][k-1]
                    whw[next_pos[1]][next_pos[0]] = '.'
                    pos = next_pos
            # ######################
            # when moving up or down
            elif m in ['^', 'v'] and whw[next_pos[1]][next_pos[0]] in ('[', ']'):
                # check if there is free space at the end of a sequence of boxes
                can_move_box = False
                box_pos_list = [next_pos]
                if whw[next_pos[1]][next_pos[0]] == '[':
                    box_pos_list.append((next_pos[0] + 1, next_pos[1]))
                if whw[next_pos[1]][next_pos[0]] == ']':
                    box_pos_list.append((next_pos[0] - 1, next_pos[1]))
                all_boxes_move = box_pos_list.copy()
                # continue searching the next lines until all can move or blocked
                while True:
                    points_to_check = set()
                    for b in box_pos_list:
                        next_box_pos = (b[0] + v[0], b[1] + v[1])
                        if whw[next_box_pos[1]][next_box_pos[0]] != '.':
                            points_to_check.add(next_box_pos)
                        if whw[next_box_pos[1]][next_box_pos[0]] == '[':
                            points_to_check.add((next_box_pos[0] + 1, next_box_pos[1]))
                        if whw[next_box_pos[1]][next_box_pos[0]] == ']':
                            points_to_check.add((next_box_pos[0] - 1, next_box_pos[1]))
                    block_cnt = 0
                    free_cnt = 0
                    for np in points_to_check:
                        if whw[np[1]][np[0]] == '#':
                            block_cnt += 1
                        if whw[np[1]][np[0]] == '.':
                            free_cnt += 1
                    # if at least one is blocked can't move
                    if block_cnt > 0:
                        break
                    # if all can move, finish the loop
                    elif free_cnt == len(points_to_check):
                        can_move_box = True
                        break
                    else:
                        # continue checking the next level
                        box_pos_list = points_to_check.copy()
                        for bl in box_pos_list:
                            all_boxes_move.append(bl)

                # if free space was found, move the boxes
                if can_move_box:
                    # move boxes in reverse order
                    for bb in all_boxes_move[::-1]:
                        whw[bb[1]+v[1]][bb[0]] = whw[bb[1]][bb[0]]
                        whw[bb[1]][bb[0]] = '.'
                    pos = next_pos

        self.print_grid(whw, pos)

        # calculate total
        total = 0
        for j in range(self.h):
            for i in range(self.w * 2):
                if whw[j][i] == '[':
                    total += 100*j + i
        return total
