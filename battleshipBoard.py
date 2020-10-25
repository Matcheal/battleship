import sys
from prettytable import PrettyTable

EMPTY_SPACE = "_"
SHIP_SYMBOL = "o"
HIT_SYMBOL = "X"
MISSED_SYMBOL = "M"

def xArray(symbol):
    list = [symbol]
    for x in range(10):
        list.append(EMPTY_SPACE)
    return list
def xxArray():
    list = []
    list.append(xArray("A"))
    list.append(xArray("B"))
    list.append(xArray("C"))
    list.append(xArray("D"))
    list.append(xArray("E"))
    list.append(xArray("F"))
    list.append(xArray("G"))
    list.append(xArray("H"))
    list.append(xArray("I"))
    list.append(xArray("J"))
    return list

def bipolarRange(start, stop):
    if start < stop:
        return range(start, stop + 1)
    elif start > stop:
        return range(stop, start + 1)
    else:
        return None

class Board:
    dictionary = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
    def __init__(self):
        fieldNamesRow = (" ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.board = PrettyTable()
        self.board._set_field_names(fieldNamesRow)
        self.table = xxArray()
        self.fill(self.table)
        self.board._set_hrules(0)
        self.yourTurn = True
        # self.board.set_style(12)
        # self.board._set_padding_width(1)


    def print(self):                                            #print board
        print(self.board)

    def fill(self, table):                                      #fill the table representing the board
        for i in range(10):
            # print(list(Board.dictionary.keys())[list(Board.dictionary.values()).index(0)])
            self.board.add_row(table[i])

    def insertByCoor(self, coordinates, symbol = SHIP_SYMBOL):          #insert single character into the board with the given string
        row, col = self.getSingleCoor(coordinates)
        self.board.clear_rows()
        self.table[row-1][col] = symbol if len(symbol) == 1 else symbol[0]
        self.fill(self.table)
        return True

    def insert(self, row, col, symbol = SHIP_SYMBOL):                   #insert single character into the board with the given bearing(row, col)
        self.board.clear_rows()
        self.table[row-1][col] = symbol if len(symbol) == 1 else symbol[0]
        self.fill(self.table)
        return True


    def getSingleCoor(self, coordinates):                       #get mathematical representation of coordinates from a string
        coordinatesRow = Board.dictionary[coordinates[0].upper()]
        coordinatesCol = int(coordinates[1]) if len(coordinates) == 2 else int(coordinates[1:3])
        return (coordinatesRow, coordinatesCol)

    def getDoubleCoor(self, coordinates):                       #get mathematical representation of coordinates from a string containing two coordinates
        start, end = coordinates.split(" ")
        startRow, startCol = self.getSingleCoor(start)
        endRow, endCol = self.getSingleCoor(end)
        return startRow, startCol, endRow, endCol

    def checkSingleCoor(self, coordinates):                     #check validity of a single coordinates
        if coordinates[0].upper() not in Board.dictionary:
            return False
        coordinatesRow = Board.dictionary[coordinates[0].upper()]
        try:
            coordinatesCol = int(coordinates[1]) if len(coordinates) == 2 else int(coordinates[1:3])
        except ValueError:
            print("Wrong value! Try again.")
            return False
        if (coordinatesRow < 1 or coordinatesRow > 10) or (coordinatesCol < 1 or coordinatesCol > 10):
            return False
        return True

    def validCoor(self, coordinates):                           #check validity of a single or double coordinates
        if (len(coordinates) == 2 or len(coordinates) == 3):
            if self.checkSingleCoor(coordinates):
                return True
        else:
            if len(coordinates.split(" ")) != 2:
                print("Wrong coordinates format(or length)!")
                return False
            start, end = coordinates.split(" ")
            if not self.checkSingleCoor(start):
                print("Wrong ending coordinates!")
                return False
            startRow, startCol = self.getSingleCoor(start)
            if not self.checkSingleCoor(end):
                print("Wrong ending coordinates!")
                return False
            endRow, endCol = self.getSingleCoor(end)
            if (startRow != endRow and startCol != endCol):
                print("Wrong coordinates!")
                return False

            return True

    def checkPointAvailability(self, row, col):                 #check for any existing neighbouring points on a board
        X = 10
        Y = 10
        neighbours = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                                           for y2 in range(y-1, y+2)
                                           if (0 < x <= X and
                                               0 < y <= Y and
                                               # (x != x2 or y != y2) and
                                               (1 <= x2 <= X) and
                                               (1 <= y2 <= Y))]
        # print(neighbours(row,col))
        for coorTuple in neighbours(row,col):
            if self.table[coorTuple[0]-1][coorTuple[1]] != EMPTY_SPACE:
                return False
        return True

    def checkShipAvailability(self, coorList, length):
        startRow, startCol, endRow, endCol = coorList
        if startRow == endRow:
            if len(bipolarRange(startCol, endCol)) != length:
                print("Wrong ship length!")
                return False
            for i in bipolarRange(startCol, endCol):
                if not self.checkPointAvailability(startRow, i):
                    print("Too close to the next ship! Try somewhere else.")
                    return False
        else:
            if len(bipolarRange(startRow, endRow)) != length:
                print("Wrong ship length!")
                return False
            for i in bipolarRange(startRow, endRow):
                if not self.checkPointAvailability(i, startCol):
                    print("Too close to the next ship! Try somewhere else.")
                    return False
        return True



    def insertShip(self, coorList, length):  # inserts Ship unconditionally
        startRow, startCol, endRow, endCol = coorList
        if startRow == endRow:
            if len(bipolarRange(startCol, endCol)) != length:
                print("Wrong ship length!")
                return False
            for i in bipolarRange(startCol, endCol):
                self.insert(startRow, i)
            return True
        else:
            if len(bipolarRange(startRow, endRow)) != length:
                print("Wrong ship length!")
                return False
            for i in bipolarRange(startRow, endRow):
                self.insert(i, startCol)
            return True

    def safeInsertShip(self, coordinates, length):              #inserts Ship with all precautions
        if not self.validCoor(coordinates):
            return False
        if length == 1 and (len(coordinates) == 2 or len(coordinates) == 3):
            row, col = self.getSingleCoor(coordinates)
            if self.checkPointAvailability(row, col):
                self.insert(row,col)
                return True
            else:
                print("Too close to the next ship! Try somewhere else.")
                return False
        elif length == 1 and not(len(coordinates) == 2 or len(coordinates) == 3):
            print("Wrong coordinates format!")
            return False
        elif length != 1 and (len(coordinates) == 2 or len(coordinates) == 3):
            print("Wrong coordinates format!")
            return False
        else:
            if self.checkShipAvailability(self.getDoubleCoor(coordinates), length):
                self.insertShip(self.getDoubleCoor(coordinates), length)
                return True
            else:
                return False


    def initShips(self, command = None):                                        #initiates loading ships sequence
        print("Initiate the position of your ships, in the following order:\n1x 4 square ship, 2x 3 square ship, 3x 2 square ship, 4x 1 square ship.",
              "Enter the starting and ending coordinates of the ship, like in the following example: A1 A4 for 4 square ship.\nType \"player\" to view your board or \"opponent\" to view your current knowledge  opponent's board")
        shipList = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        if command == "ready":
            coorList = ["A1 A4", "C1 C3", "H10 J10", "A6 A7", "E2 F2", "G5 G6", "A10", "J1", "J5", "I3"]
            for i in range(10):
                self.safeInsertShip(coorList[i], shipList[i])
            return True
        elif command == "two":
            self.safeInsertShip("A2", 1)
            self.safeInsertShip("A4", 1)
            return True
        elif command == "short":
            for i in [2, 1]:
                self.print()
                print("Enter " + str(i) + " square ship coordinates: ")
                while(True):
                    coordinates = input()
                    if self.safeInsertShip(coordinates, i):
                        break
            return True
        else:
            for i in shipList:
                self.print()
                print("Enter " + str(i) + " square ship coordinates: ")
                while(True):
                    coordinates = input()
                    if self.safeInsertShip(coordinates, i):
                        break
            return True

    def ifHit(self, coordinates):
        row, col = self.getSingleCoor(coordinates)
        if self.table[row-1][col] == SHIP_SYMBOL:
            print("Hit!")
            self.insert(row,col, HIT_SYMBOL)
            return True
        print("Missed!")
        return False

    def countSymbols(self, symbol = SHIP_SYMBOL):
        count = 0
        for row in self.table:
            for elem in row:
                if elem == symbol:
                    count +=1
        # print("Game over, you WON!")
        return count



# b = Board()
# b.safeInsertShip("C2 C4", 3)
# b.print()
# b.ifHit("C2")
# b.ifHit("C3")
# b.ifHit("C4")
# b.print()
# print(b.ifEnd())
# b.safeInsertShip("B6 E6", 4)
# b.print()
#
# if b.initShips("ready"):
#     b.print()