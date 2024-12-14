import math

class Part1Part2():

    def __init__(self, lines):
        # initialize claws
        self.claws = []
        one_claw = []
        for l in lines:
            if l[0:6] == 'Button':
                button = l.split(':')
                buttons = button[1].split(',')
                xbutton = buttons[0].split('+')
                ybutton = buttons[1].split('+')
                one_claw.append((int(xbutton[1]), int(ybutton[1])))
            if l[0:5] == 'Prize':
                prize = l.split(':')
                prizes = prize[1].split(',')
                xprize = prizes[0].split('=')
                yprize = prizes[1].split('=')
                one_claw.append((int(xprize[1]), int(yprize[1])))
                self.claws.append(one_claw)
                one_claw = []

    def part1(self) -> int:
        total = 0
        for c in self.claws:
            xa = c[0][0]
            ya = c[0][1]
            xb = c[1][0]
            yb = c[1][1]
            xp = c[2][0]
            yp = c[2][1]

            # solve equation and substitute values
            na = (xp*yb - yp*xb) / (yb*xa - ya*xb)
            nb = (yp*xa - xp*ya) / (yb*xa - ya*xb)

            # if both results are integers
            if math.floor(na) == na and math.floor(nb) == nb:
                total += int(3*na + nb)

        return total

    def part2(self) -> int:
        total = 0
        for c in self.claws:
            xa = c[0][0]
            ya = c[0][1]
            xb = c[1][0]
            yb = c[1][1]
            # same as part 1 but add large number
            xp = c[2][0] + 10000000000000
            yp = c[2][1] + 10000000000000

            # solve equation and substitute values
            na = (xp*yb - yp*xb) / (yb*xa - ya*xb)
            nb = (yp*xa - xp*ya) / (yb*xa - ya*xb)

            # if both results are integers
            if math.floor(na) == na and math.floor(nb) == nb:
                total += int(3*na + nb)

        return total
