from collections import defaultdict

class Part1Part2():

    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2
    
    def part1(self) -> int:
        # initialize the result
        total = 0

        # sort the lists
        self.list1.sort()
        self.list2.sort()

        # sum the differences between the two lists
        for i in range(len(self.list1)):
            total += abs(self.list1[i] - self.list2[i])
        return total

    def part2(self) -> int:
        # initialize the result
        total = 0

        # initialize a defaultdict
        counts = defaultdict(lambda: 0)

        # count each occurence of the elements in list2
        for c in self.list2:
            counts[c] += 1
        
        # multiply elements in list1 by their occurrence
        for c in self.list1:
            if c in counts:
                total += c * counts[c]

        return total