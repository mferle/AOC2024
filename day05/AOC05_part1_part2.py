class Part1Part2():

    def __init__(self, all_pairs, pages):
        self.all_pairs = all_pairs
        self.pages = pages
        self.incorrect_pages = []

    def correct_or_not(self, p):
        # check all pairs in the list of pages
        for i in range(len(p) - 1):
            curr_pair = p[i] + '|' + p[i+1]
            if not curr_pair in self.all_pairs:
                # if any pair fails, the order is not correct, return False
                return False
        # if none failed, the order is correct, return True
        return True

    def part1(self) -> int:
        # initialize total
        total = 0

        # check all lists of pages
        for p in self.pages:
            if self.correct_or_not(p):
                # if correct order, add middle page to total
                total += int(p[len(p) // 2])
            else:
                # if not correct order, append to list of incorrect pages
                self.incorrect_pages.append(p)

        return total

    def part2(self) -> int:
        # initialize total
        total = 0

        # loop over all incorrect pages
        for p in self.incorrect_pages:
            in_order = False
            # while there are still pairs not in order
            while not in_order:
                # check all pairs in the list of pages
                for i in range(len(p) - 1):
                    p1 = p[i]
                    p2 = p[i+1]
                    curr_pair = p1 + '|' + p2
                    if curr_pair in self.all_pairs:
                        continue
                    # current pair not OK, switch them
                    p[i] = p2
                    p[i+1] = p1
                    # check if the entire list of pages is in order
                    in_order = self.correct_or_not(p)
                    break
            # add middle page to total
            total += int(p[len(p) // 2])

        return total
