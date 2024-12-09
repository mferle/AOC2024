from collections import deque 
    
class Part1Part2():

    def __init__(self, disk_map):
        self.disk_map = disk_map

    def part1(self) -> int:
        # convert the disk map into a deque
        blocks = deque()
        for idx, c in enumerate(self.disk_map):
            file_id = (idx+1) // 2
            if (idx+1) % 2 == 1:
                for i in range(int(c)):
                    blocks.append(file_id)
            else:
                for i in range(int(c)):
                    blocks.append(-1)

        # find first occurrence of -1
        first_empty = blocks.index(-1)

        # repeat while there is still empty space
        while first_empty:
            # remove the last element
            last_element = blocks.pop()
            # if the last element is not empty space
            if last_element != -1:
                # switch the last element with the empty space
                blocks.remove(-1)
                blocks.insert(first_empty, last_element)
            # find the next empty space
            try:
                first_empty = blocks.index(-1)
            except:
                first_empty = 0

        # calculate the checksum by multiplying the position with the value
        total = 0
        for idx, c in enumerate(blocks):
            total += idx*c
        return total
    
    def part2(self) -> int:
        # convert the disk map into a deque
        blocks = deque()
        # keep track of file_ids to move
        file_ids = deque()
        for idx, c in enumerate(self.disk_map):
            file_id = (idx+1) // 2
            if (idx+1) % 2 == 1:
                file_ids.append((file_id, int(c)))
                blocks.append((file_id, int(c)))
            else:
                blocks.append((-1, int(c)))

        #check for each file_id if it can be moved
        while len(file_ids) > 0:
            f = file_ids.pop()
            position_of_f = blocks.index(f)
            # find contiguous empty space for the file
            for idx, b in enumerate(blocks):
                # don't look beyond the file position
                if idx > position_of_f:
                    break
                # if contiguous space exists
                if b[0] == -1 and b[1] >= f[1]:
                    # swap the file
                    orig_pos = blocks.index(f)
                    blocks[orig_pos] = (-1, f[1])
                    blocks[idx] = (-1, b[1] - f[1])
                    blocks.insert(idx, f)
                    break

        # convert the deque to a list
        string = []
        for b in blocks:
            for i in range(b[1]):
                if b[0] == -1:
                    string.append(0)
                else:
                    string.append(b[0])
        # calculate the checksum by multiplying the position with the value
        total = 0
        for idx, c in enumerate(string):
            if c > -1:
                total += idx*c
        return total
