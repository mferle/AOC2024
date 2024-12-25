import math

class Part1Part2():

    def __init__(self, lines):
        self.reg = {}
        for l in lines:
            if l[0:8] == 'Register':
                r = l.split(':')[0].split()[1]
                rv = int(l.split(':')[1])
                self.reg[r] = rv
            if l[0:7] == 'Program':
                self.prog = [int(c) for c in l.split(':')[1].split(',')]
        print(self.reg, self.prog)

    def one_program(self, lreg):
        output = []
        step = 0
        while True:
            opcode = self.prog[step]
            operand = self.prog[step+1]

            if operand in [0, 1, 2, 3]: # Combo operands 0 through 3 represent literal values 0 through 3.
                opval = operand
            if operand == 4: # Combo operand 4 represents the value of register A.
                opval = lreg['A']
            if operand == 5: # Combo operand 5 represents the value of register B.
                opval = lreg['B']
            if operand == 6: # Combo operand 6 represents the value of register C.
                opval = lreg['C']

            # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. 
            # The denominator is found by raising 2 to the power of the instruction's combo operand. 
            # The result of the division operation is truncated to an integer and then written to the A register.
            if opcode == 0:
                res = lreg['A'] / (2 ** opval)
                lreg['A'] = math.trunc(res)
            # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
            if opcode == 1:
                res = lreg['B'] ^ operand
                lreg['B'] = res
            # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
            if opcode == 2:
                res = opval % 8
                lreg['B'] = res
            # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, 
            # it jumps by setting the instruction pointer to the value of its literal operand; 
            # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
            if opcode == 3:
                if lreg['A'] == 0:
                    pass
                else:
                    step = operand
                    continue
            # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. 
            # (For legacy reasons, this instruction reads an operand but ignores it.)
            if opcode == 4:
                res = lreg['B'] ^ lreg['C']
                lreg['B'] = res
            # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. 
            if opcode == 5:
                res = opval % 8
                output.append(res)
            # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. 
            if opcode == 6:
                res = lreg['A'] / (2 ** opval)
                lreg['B'] = int(res)
            # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. 
            if opcode == 7:
                res = lreg['A'] / (2 ** opval)
                lreg['C'] = int(res)

            step += 2
            if step >= len(self.prog):
                break

        return ','.join([str(i) for i in output])

    def part1(self) -> int:
        new_reg = {}
        new_reg['A'] = self.reg['A']
        new_reg['B'] = self.reg['B']
        new_reg['C'] = self.reg['C']
        output = self.one_program(new_reg)
        return output
    
    def part2(self) -> int:
        total = 0

        #ToDo

        return total
