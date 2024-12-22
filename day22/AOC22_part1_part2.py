import math

class Part1Part2():

    def __init__(self, lines):
        self.lines = [int(l) for l in lines]
        print(lines)

    def calc_next_secret_number(self, n):
        # Calculate the result of multiplying the secret number by 64. 
        r1 = n * 64
        # Mix this result into the secret number: calculate the bitwise XOR of the given value and the secret number.
        r2 = r1 ^ n
        # The secret number becomes the result of that operation. 
        n = r2
        # Prune the secret number: calculate the value of the secret number modulo 16777216. 
        r3 = r2 % 16777216
        # The secret number becomes the result of that operation.
        n = r3
        # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. 
        r4 = math.floor(r3 / 32)
        # Then, mix this result into the secret number. 
        r5 = r4 ^ n
        n = r5
        # Finally, prune the secret number.
        r6 = r5 % 16777216
        n = r6
        # Calculate the result of multiplying the secret number by 2048. 
        r7 = r6 * 2048
        # Then, mix this result into the secret number. 
        r8 = r7 ^ n
        n = r8
        # Finally, prune the secret number.
        r9 = r8 % 16777216

        return r9

    def calc_all_numbers(self, how_many):
        # initialize total
        total = 0
        # initialize all differences and all prices
        all_diffs = []
        all_prices = []
        # for each secret number
        for secret_number in self.lines:
            # initialize the differences and prices
            diffs = []
            prices = []
            prev_secret_number = secret_number
            # for how many iterations
            for i in range(how_many):
            # get the next secret number
                secret_number = self.calc_next_secret_number(secret_number)
                # calculate and append the difference
                diffs.append((secret_number % 10) - (prev_secret_number % 10))
                # append the price
                prices.append(secret_number % 10)
                prev_secret_number = secret_number

            total += secret_number
            # append to all differences and all prices
            all_diffs.append(diffs)
            all_prices.append(prices)

        return total, all_diffs, all_prices

    def part1(self, how_many) -> int:
        total, all_diffs, all_prices = self.calc_all_numbers(how_many)
        return total

    def part2(self, how_many) -> str:
        total, all_diffs, all_prices = self.calc_all_numbers(how_many)

        # initialize all 4-price sequences
        sequences = {}
        # loop throught all differences
        for dx, diffs in enumerate(all_diffs):
            for idx, d in enumerate(diffs):
                if idx < 3:
                    continue
                # calculate the current sequence
                curr_seq = (diffs[idx-3], diffs[idx-2], diffs[idx-1], diffs[idx])
                if curr_seq in sequences:
                    # if the sequence is in all sequences and the sequence was not found yet, add the price and flag that the sequence was found
                    flgs = sequences[curr_seq][1]
                    if flgs[dx] == 0:
                        flgs[dx] = 1
                        sequences[curr_seq] = (sequences[curr_seq][0] + all_prices[dx][idx], flgs)
                else:
                    # if the sequence is not yet in all sequences, add the price and flag that the sequence was found
                    flgs = [0 for _ in range(len(self.lines))]
                    flgs[dx] = 1
                    sequences[curr_seq] = (all_prices[dx][idx], flgs)

        # find the highest value
        max_value = 0
        for s in sequences:
            if sequences[s][0] > max_value:
                max_value = sequences[s][0]

        return max_value
