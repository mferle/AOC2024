def read_maze(lines):
    # initialize maze
    maze = {}
    # parse input into maze and mark start and end position
    for j, l in enumerate(lines):
        for i, c in enumerate(l):
            maze[(i, j)] = c 
        # mark the start position
            if c == 'S':
                start_pos = (i, j)
                maze[(i, j)] = '.'
        # mark the end position
            if c == 'E':
                end_pos = (i, j)
                maze[(i, j)] = '.'
    return maze, start_pos, end_pos
