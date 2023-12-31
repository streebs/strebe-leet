import aocd
from abc import ABC, abstractmethod
import unittest
import sys

def calculate(s):
    l = len(s)

    if l == 0:
        return 0
    if l == 1:
        return 1
    if l > 1:
        return 2**(l-1)

def part_a(data):

    winScores = []
    for card in data:
        card = card.split(':')[1]
        s = card.split('|')
        myNumsAsString = s[0]
        winNumsAsString = s[1]

        myNumsAsString = myNumsAsString.strip()
        myNumsAsList = myNumsAsString.split(' ')

        winNumsAsString = winNumsAsString.strip()
        winNumsAsList = winNumsAsString.split(' ')

        for el in myNumsAsList:
            if el == '':
                myNumsAsList.remove('')

        for el in winNumsAsList:
            if el == '':
                winNumsAsList.remove('')

        for num in range(len(myNumsAsList)):
            myNumsAsList[num] = int(myNumsAsList[num])

        for num in range(len(winNumsAsList)):
            winNumsAsList[num] = int(winNumsAsList[num])

        myNumsSet = set(myNumsAsList)
        WinNumsSet = set(winNumsAsList)

        winScores.append(calculate(myNumsSet.intersection(WinNumsSet)))

    return sum(winScores)

# Part B Globals and Classes
winTable = {}

class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Root(Node):
    def __init__(self):
        self.cardNum = "root"
        self.children = [CardNode(i) for i in winTable]
    def accept(self, visitor):
        visitor.preVisit(self)
        for child in self.children:
            if child is not None:
                child.accept(visitor)
        visitor.visit(self)

class CardNode(Node):
    def __init__(self, cardNum, children=[]):
        self.cardNum = cardNum
        self.children = children
    def accept(self, visitor):
        visitor.preVisit(self)
        for child in self.children:
            if child is not None:
                child.accept(visitor)
        visitor.visit(self)

class Visitor(ABC):
    def preVisit(self, node):
        pass
    def visit(self, node):
        pass

class BuildTree(Visitor):
    def preVisit(self, node):
        if node.cardNum == "root":
            pass
        else:
            node.children = [CardNode(i) for i in winTable[node.cardNum]]

class CountTree(Visitor):
    def __init__(self):
        self.count = 0
    def preVisit(self, node):
        if node.cardNum == "root":
            pass
        else:
            self.count += 1

def fillTable(data):
    # start by creating a lookup table that takes the card number as input and returns a list of the winning cards
    cardNum = 1
    for card in data:
        card = card.split(':')[1]
        s = card.split('|')
        myNumsAsString = s[0]
        winNumsAsString = s[1]

        myNumsAsString = myNumsAsString.strip()
        myNumsAsList = myNumsAsString.split(' ')

        winNumsAsString = winNumsAsString.strip()
        winNumsAsList = winNumsAsString.split(' ')

        for el in myNumsAsList:
            if el == '':
                myNumsAsList.remove('')

        for el in winNumsAsList:
            if el == '':
                winNumsAsList.remove('')

        for num in range(len(myNumsAsList)):
            myNumsAsList[num] = int(myNumsAsList[num])

        for num in range(len(winNumsAsList)):
            winNumsAsList[num] = int(winNumsAsList[num])

        myNumsSet = set(myNumsAsList)
        WinNumsSet = set(winNumsAsList)

        numWins = len(list(myNumsSet.intersection(WinNumsSet)))

        winTable[cardNum] = [i for i in range(cardNum+1, cardNum + numWins + 1)]
        cardNum += 1



def part_b(data):
    # create lookup table
    fillTable(data)
    # build tree
    root = Root()
    build = BuildTree()
    root.accept(build)
    # count nodes and return!
    cnt = CountTree()
    root.accept(cnt)
    return cnt.count





################# UNIT TESTS #################
test_data = [
    'Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3: 1 21 53 59 44 | 69 82 63 72 16 21 14 1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58 5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(part_a(test_data), 13) # make sure to update tests
        self.assertEqual(part_b(test_data), 30)


############### DATA RETRIEVAL ###############
data = aocd.get_data(day=4, year=2023)
data_as_list = data.split("\n")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        sys.argv = [sys.argv[0]] # unittest uses the system args to run so it has to be cleared :/
        unittest.main()
    else:
        aocd.submit(part_a(data_as_list), part='a', day=4, year=2023)
        aocd.submit(part_b(data_as_list), part='b', day=4, year=2023)

if __name__ == "__main__":
    main()