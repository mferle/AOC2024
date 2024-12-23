from itertools import combinations
import networkx as nx

class Part1Part2():

    def __init__(self, lines):
        self.pairs = [l.split('-') for l in lines]
        self.pairs_for_lookup = set()
        for p1, p2 in self.pairs:
            self.pairs_for_lookup.add((p1, p2))
            self.pairs_for_lookup.add((p2, p1))
        # create a set of unique computers
        self.comps = set()
        for p in self.pairs:
            self.comps.add(p[0])
            self.comps.add(p[1])

    def part1(self) -> int:
        # use the combinations library to create all possible combinations of 3 elements from the set of computers
        triads = combinations(self.comps, 3)

        # initialize count of all connected triads
        cnt_connected = 0
        # for each combination
        for a, b, c in triads:
            # check if it begins with 't'
            if a[0] != 't' and b[0] != 't' and c[0] != 't':
                continue
            # check if the computers are connected
            if  ((a, b) in self.pairs_for_lookup) and \
                ((a, c) in self.pairs_for_lookup) and \
                ((b, c) in self.pairs_for_lookup):
                cnt_connected += 1

        return cnt_connected

    def part2(self) -> str:
        # Create a graph
        G = nx.Graph()

        # Add nodes
        G.add_nodes_from(self.comps)

        # Add edges
        G.add_edges_from(self.pairs)

        # Finding all maximal cliques
        cliques = list(nx.find_cliques(G))
        largest_clique = max(cliques, key=len)

        return ','.join(sorted(largest_clique))
