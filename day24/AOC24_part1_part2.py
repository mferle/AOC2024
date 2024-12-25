from copy import deepcopy

class Part1Part2():

    def __init__(self, lines):
        self.wires = {}
        self.gates = []
        for l in lines:
            if l.find(':') > -1:
                w, v = l.split(':')
                self.wires[w] = int(v)
            if l.find('->') > -1:
                q, g = l.split('->')
                self.gates.append(((q.split()), g.strip()))

    def binary_number(self, w):
        # find all wires that start with the value of w
        bits_list = []
        for k in self.wires.keys():
            if k[0] == w:
                bits_list.append((k, self.wires[k]))

        # sort the wires
        bits_list.sort()

        bits_string = ''
        # calculate the binary value
        multiplier = 1
        total = 0
        for b in bits_list:
            bits_string = bits_string + str(b[1])
            total += b[1] * multiplier
            multiplier = multiplier * 2

        return total, bits_string
    
    def part1(self) -> int:

        xvalue, xbits = self.binary_number('x')
        yvalue, ybits = self.binary_number('y')
        zbits_to_be = bin(xvalue + yvalue)[2:]
        print(xbits[::-1])
        print(ybits[::-1])
        print(zbits_to_be)
        zdict = {}
        for i in range(len(zbits_to_be)):
            b = int(zbits_to_be[len(zbits_to_be) - 1 - i])
            zdict[f'z{i:02d}'] = b
        print(zdict)

        q = deepcopy(self.gates)

        while len(q) > 0:
            # take first element from q
            e, g = q[0]
            # set q to the remainder
            q = q[1:]
            # get the gates and operation
            a, op, b = e
            # if both gates have signals, calculate the output
            if a in self.wires and b in self.wires:
                if op == 'AND':
                    if self.wires[a] == 1 and self.wires[b] == 1:
                        self.wires[g] = 1
                    else:
                        self.wires[g] = 0
                if op == 'OR':
                    if self.wires[a] == 1 or self.wires[b] == 1:
                        self.wires[g] = 1
                    else:
                        self.wires[g] = 0
                if op == 'XOR':
                    if self.wires[a] != self.wires[b]:
                        self.wires[g] = 1
                    else:
                        self.wires[g] = 0
            else:
                # add to end of q to come back later
                q.append(((a, op, b), g))

        zvalue, zbits = self.binary_number('z')

        print(zbits[::-1])

        for zz in zdict:
            if zdict[zz] != self.wires[zz]:
                print(zz, zdict[zz], self.wires[zz])        

        return zvalue

    def part2(self) -> str:
        total = 0

        # ToDo
        
        return total
