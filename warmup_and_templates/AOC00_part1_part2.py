class Part1Part2():

    def __init__(self, lines):
        self.lines = lines
    
    def part1(self) -> int:
        # initialize the result
        total = 0
        # read each line in the list
        for line in self.lines:
            # find the first character that is a digit
            for chr in line:
                # if the character is a digit, save it and break from the loop
                if chr.isnumeric():
                    first_digit = int(chr)
                    break

            # repeat from reverse, find the last character that is a digit
            line_reverse = line[::-1]
            for chr in line_reverse:
                # if the character is a digit, save it and break from the loop
                if chr.isnumeric():
                    last_digit = int(chr)
                    break

            # add to the total
            total += 10*first_digit + last_digit
        return total

    def part2(self) -> int:
        # initialize the result
        total = 0

        # write your own solution for part2 ...

        return total