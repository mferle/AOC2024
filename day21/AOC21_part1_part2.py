class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
        print(lines)

        self.num_kp = {}
        self.num_kp['7'] = (0, 0)
        self.num_kp['8'] = (0, 1)
        self.num_kp['9'] = (0, 2)
        self.num_kp['4'] = (1, 0)
        self.num_kp['5'] = (1, 1)
        self.num_kp['6'] = (1, 2)
        self.num_kp['1'] = (2, 0)
        self.num_kp['2'] = (2, 1)
        self.num_kp['3'] = (2, 2)
        self.num_kp['0'] = (3, 1)
        self.num_kp['A'] = (3, 2)
#        +---+---+---+
#        | 7 | 8 | 9 |
#        +---+---+---+
#        | 4 | 5 | 6 |
#        +---+---+---+
#        | 1 | 2 | 3 |
#        +---+---+---+
#            | 0 | A |
#            +---+---+
 
        self.dir_kp = {}
        self.dir_kp['^'] = (0, 1)
        self.dir_kp['A'] = (0, 2)
        self.dir_kp['<'] = (1, 0)
        self.dir_kp['v'] = (1, 1)
        self.dir_kp['>'] = (1, 2)
#            +---+---+
#            | ^ | A |
#        +---+---+---+
#        | < | v | > |
#        +---+---+---+

    def one_move(self, start, end, keypad, forbidden):
        # get start and end positions
        start_pos = keypad[start]
        end_pos = keypad[end]
        # calculate differences in each direction
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        # calculate moves north-south
        moveEW = ''
        if dx > 0:
            sym = 'v'
        else:
            sym = '^'
        for i in range(abs(dx)):
            moveEW = moveEW + sym
        # calculate moves east-west
        moveNS = ''
        if dy > 0:
            sym = '>'
        else:
            sym = '<'
        for i in range(abs(dy)):
            moveNS = moveNS + sym
        # check if going right, then EW first is better
        if sym == '>' and (end_pos[0], start_pos[1]) != forbidden:
            return moveEW + moveNS + 'A'
        # if not in forbidden cell, NS first is better
        if (start_pos[0], end_pos[1]) != forbidden:
            return moveNS + moveEW + 'A'
        # otherwise EW first
        if (end_pos[0], start_pos[1]) != forbidden:
            return moveEW + moveNS + 'A'

    def keypad_seq(self, code, keypad, forbidden):
        steps = ''

        curr_code = 'A'
        for rem_code in code:
            # get from curr_code to rem_code

            steps += self.one_move(curr_code, rem_code, keypad, forbidden)

            # position reached, prepare for next position
            curr_code = rem_code

        return steps
    
    def part1(self) -> int:
        total = 0

        for code in self.lines:
            first_sequence = self.keypad_seq(code, self.num_kp, (3, 0))
            second_sequence = self.keypad_seq(first_sequence, self.dir_kp, (0, 0))
            third_sequence = self.keypad_seq(second_sequence, self.dir_kp, (0, 0))

            total += len(third_sequence * int(code.replace('A', '')))
        return total
    
    def part2(self) -> str:
        total = 0

        return total
