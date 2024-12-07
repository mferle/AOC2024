class Part1Part2():

    def __init__(self, lines):
        # parse lines into equations
        self.equations = []
        for l in lines:
            parts = l.split(':')
            test_value = int(parts[0])
            operands = parts[1].split()
            opnum = [int(o) for o in operands]
            self.equations.append((test_value, opnum))

    def solve_equations(self, operators) -> int:
        # keep list of already solved equations
        already_solved = []

        # for each equation
        for x in self.equations:
            # initialize working list
            we = [x]

            # while working list is not empty
            while len(we) > 0:
                # take the last element from the working list
                e = we.pop()

                test_value = e[0]
                operands = e[1]
                op0 = operands[0]
                op1 = operands[1]

                # if there are only two operands left, check if it can be solved
                if len(operands) == 2:
                    if op0 + op1 == test_value:
                        already_solved.append(test_value)
                    elif op0 * op1 == test_value:
                        already_solved.append(test_value)
                    elif '||' in operators and int(str(op0)+str(op1)) == test_value:
                        already_solved.append(test_value)
                # otherwise add to the working list
                else:
                    # add new operands to working list if the new operand is less than the test value
                    if op0 + op1 <= test_value:
                        we.append((test_value, [op0 + op1] + operands[2:]))
                    if op0 * op1 <= test_value:
                        we.append((test_value, [op0 * op1] + operands[2:]))
                    if '||' in operators and int(str(op0)+str(op1)) <= test_value:
                        we.append((test_value, [int(str(op0)+str(op1))] + operands[2:]))

        # sum the unique unique test values from equations already solved
        total = sum(set(already_solved))
        return total

    def part1(self) -> int:
        # define the operators
        operators = ['+', '*']
        return(self.solve_equations(operators))

    def part2(self) -> int:
        # define the operators
        operators = ['+', '*', '||']
        return(self.solve_equations(operators))
