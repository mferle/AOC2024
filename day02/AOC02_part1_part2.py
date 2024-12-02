class Part1Part2():

    def __init__(self, reports, logger):
        self.reports = reports
        self.logger = logger
    
    def safe_or_unsafe(self, r) -> bool:
        # define whether it is increasing or decreasing by comparing the first two elements
        if int(r[0]) < int(r[1]):
            inc_dec = 'inc'
        else:
            inc_dec = 'dec'

        # loop through the numbers to next-to-last
        for i in range(len(r) - 1):
            # define current number, next number, and difference
            curr = int(r[i])
            next = int(r[i+1])
            diff = abs(next - curr)
            # check if difference is less than 1 or greater than 3
            if (diff < 1) or (diff > 3):
                # not safe
                return False
            # check if number is increasing or decreasing like the first pair
            if (inc_dec == 'dec') and (next > curr):
                # not safe
                return False
            if (inc_dec == 'inc') and (next < curr):
                # not safe
                return False

        # if all checks passed, it's safe
        return True
    
    def part1(self) -> int:
        # initialize count
        safe_count = 0

        for r in self.reports:
            if self.safe_or_unsafe(r):
                safe_count += 1

        return safe_count

    def part2(self) -> int:
        # initialize count
        safe_count = 0

        for r in self.reports:
            self.logger.debug(f"Processing report: {r}")

            # check if main report is safe
            if self.safe_or_unsafe(r):
                safe_count += 1
            else:
                # check subreports, each time one element removed
                unsafe_count = 0
                safe_flg = False
                for i in range(len(r)):
                    sub_r = r[0:i] + r[i+1:]
                    if self.safe_or_unsafe(sub_r):
                        safe_flg = True
                    else:
                        unsafe_count += 1
                # if at least one of the subreports was safe or at most one was unsafe
                if safe_flg or unsafe_count <= 1:
                    safe_count += 1

        return safe_count