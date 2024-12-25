class Part1Part2():

    def __init__(self, lines):
        # initialize list of locks and keys
        locks_or_keys = []
        # initialize a single lock or key
        one_lock_or_key = []
        for l in lines:
            # if line is blank, starting a new lock or key
            if l == '':
                locks_or_keys.append(one_lock_or_key)
                one_lock_or_key = []
            # otherwise append to the current lock or key
            else:
                one_lock_or_key.append(l)
        locks_or_keys.append(one_lock_or_key)

        # initialize locks
        self.locks = []
        # initialize keys
        self.keys = []
        # split the locks and keys into separate lists depending on the starting line
        for lk in locks_or_keys:
            if lk[0] == '#####':
                self.locks.append(lk)
            else:
                self.keys.append(lk)

    def part1(self) -> int:
        total = 0

        # calculate the lock combinations
        all_lock_combinations = []
        for l in self.locks:
            # initialize the combination
            combination = [0 for _ in range(len(l[0]))]
            for i, one_line in enumerate(l):
                for j, c in enumerate(one_line):
                    # skip first line
                    if i == 0:
                        continue
                    # if the character is #, add to combination
                    if c == '#':
                        combination[j] += 1
            all_lock_combinations.append(combination)

        # calculate the key combinations
        all_key_combinations = []
        for l in self.keys:
            # initialize the combination
            combination = [0 for _ in range(len(l[0]))]
            for i, one_line in enumerate(l):
                for j, c in enumerate(one_line):
                    # skip last line
                    if i == len(l) - 1:
                        continue
                    # if the character is #, add to combination
                    if c == '#':
                        combination[j] += 1
            all_key_combinations.append(combination)

        # initialize matching keys and locks
        total = 0
        for l in all_lock_combinations:
            for k in all_key_combinations:
                fit = True
                # check each pair of key and lock combination
                for i in range(len(l)):
                    if l[i] + k[i] > len(l):
                        fit = False
                # if all of them fit, add to total
                if fit:
                    total += 1
        return total
