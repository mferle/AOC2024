class Part1Part2():

    def __init__(self, line):
        # initialize dictionary of stones and their counts
        self.stones_dict = {}
        for stone in line.split():
            if stone in self.stones_dict.keys():
                self.stones_dict[stone] = self.stones_dict[stone] + 1
            else:
                self.stones_dict[stone] = 1

    def stone_change(self, stone):
        # input one stone and output a list of stones after the change
        new_stones = []
        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1
        if stone == '0':
            new_stones.append('1')
        # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones
        elif len(stone) % 2 == 0:
            new_stones.append(str(int(stone[0:int(len(stone)/2)])))
            new_stones.append(str(int(stone[int(len(stone)/2):])))
        # the stone is replaced by a new stone; the old stone's number multiplied by 2024
        else:
            new_stones.append(str(int(stone)*2024))
        return new_stones

    def one_blink(self, s_dict):
        # keep dictionary of stones and their counts
        new_s_dict = {}

        # for each stone in the previous dictionary
        for stone in s_dict:
            # get a list of stones after the change
            new_list = self.stone_change(stone)
            # add to new dictionary, adding the number of stones from previously
            for s in new_list:
                if s in new_s_dict.keys():
                    new_s_dict[s] = new_s_dict[s] + s_dict[stone]
                else:
                    new_s_dict[s] = s_dict[stone]

        return new_s_dict

    def both_parts(self, blinks) -> int:
        # initialize local variable for stones_dict to iterate
        stones_dict = self.stones_dict
        # for as many blinks as the parameter
        for i in range(blinks):
            stones_dict = self.one_blink(stones_dict)

        # sum the stones
        total = 0
        for s in stones_dict:
            total += stones_dict[s]

        return total

    def part1(self) -> int:
        return self.both_parts(25)

    def part2(self) -> int:
        return self.both_parts(75)
