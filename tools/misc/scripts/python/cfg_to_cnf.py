import argparse as ap

parser = ap.ArgumentParser(description='Takes a CFG and outputs it as a CNF')

parser.add_argument('-i', '--input', nargs=1,
                    type=ap.FileType('r'),
                    help="The name of the file to read from to.", dest="in_file")

parser.add_argument('-o', '--out_file', nargs='?',
                    type=ap.FileType('w'), default=sys.stdout,
                    help="The name of the file to write to.", dest="out_file")

args = parser.parse_args()

# File format
# Start symbol is the first production encountered
# Productions on left followed by > and what they produce
# Prods seperated by |
# One symbol per line
# epsilon represented by ~

# Example:
# S > A | b
# A > a | ~

EPSILON = '~'
A = 65
z = 122
ascii_size = 57

class Production(object):
    """docstring for Production"""

    def __init__(self, production):
        self.orig = production
        self.symbol = production.split()[0]
        self.productions = []
        for prod in production.split()[2:]:
            if prod != '|':
                self.productions.append((prod, list(prod)))


class Grammar(object):
    """docstring for Grammar"""

    def __init__(self, lines):
        self.lines = lines

        self.var   = set()
        self.terms = set()
        self.s_var = None
        self.prods = {}

        self.generated_var = set()
        self.gen_cnt = 0

        self.parseLines()

    def parseLines(self):
        # Read the first char in to determine start symbol
        self.s_var = self.lines[0][0]

        # For each line parse it
        for line in self.lines:
            self.parseLine(line)

    def parseLine(self, line):
        # Line has the format sym > production [| production]*, so lets clean it a bit
        line = line.split()
        line = [x for x in line if x != '|' or x != '>']


        sym = line[0]
        self.var.add(sym)
        self.prods[sym] = []

        for prod in line[1:]:
            self.prods[sym].append(prod)
            for c in prod:
                if c.islower():
                    self.terms.add(c)
                else:
                    self.var.add(c)

    def generateNewVar(self):
        gen_cnt = self.gen_cnt
        new_var = '!'

        while gen_cnt != 0:
            new_var += chr((gen_cnt % ascii_size) + 65)
            gen_cnt -= ascii_size

        self.gen_cnt += 1
        self.generated_var.add(new_var)

        return new_var

    def badStartSymbol(self):
        for sym, prods in self.prods.items():
            for prod in prods:
                # Check if the start symbol appears in any RHS's
                if self.s_var in prod:
                    return (sym, prod)
        return None

    def hasEpsilons(self):
        for sym, prods in self.prods.items():
            # Check if epsilon is a production for this symbol
            if EPSILON in prod:
                return sym
        return None

    def hasUnits(self):
        for sym, prods in self.prods.items():
            for prod in prods:
                # Check if theres a unit production
                if len(prod) == 1 and prod in self.var:
                    return (sym, prod)
        return None

    def hasLongProds(self):
        for sym, prods in self.prods.items():
            for prod in prods:
                # Check if theres a unit production
                if len(prod) > 2:
                    return (sym, prod)
        return None

    def hasBadProds(self):
        for sym, prods in self.prods.items():
            for prod in prods:
                # Check if theres a production of the form aB
                if len(prod) >= 2 and prod[0] in self.terms and prod[1] in self.var:
                    return (sym, prod
                            )
        return None

    def fixStartSymbols(self):


    def convert(self):




prods = args.in_file.read_lines()
