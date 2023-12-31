import random
from game import Board
import globals as globals

class Bot13521047(object):
    """
    Bot player
    """

    def __init__(self):
        self.player = None
        self.NIM = "13521047"

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, return_var):

        try:
            location = self.get_input(board)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1

        while move == -1 or move not in board.availables:
            if globals.stop_threads:
                return
            try:
                location = self.get_input(board)
                if isinstance(location, str):  # for python3
                    location = [int(n, 10) for n in location.split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
        return_var.append(move) 

    def __str__(self):
        return "{} a.k.a Player {}".format(self.NIM,self.player)
    
    def get_input(self, board : Board) -> str:
        """
            Parameter board merepresentasikan papan permainan. Objek board memiliki beberapa
            atribut penting yang dapat menjadi acuan strategi.
            - board.height : int (x) -> panjang papan
            - board.width : int (y) -> lebar papan
            Koordinat 0,0 terletak pada kiri bawah

            [x,0] [x,1] [x,2] . . . [x,y]                               
            . . . . . . . . . . . . . . .  namun perlu diketahui        Contoh 4x4: 
            . . . . . . . . . . . . . . .  bahwa secara internal        11 12 13 14 15
            . . . . . . . . . . . . . . .  sel-sel disimpan dengan  =>  10 11 12 13 14
            [2,0] [2,1] [2,2] . . . [2,y]  barisan interger dimana      5  6  7  8  9
            [1,0] [1,1] [1,2] . . . [1,y]  kiri bawah adalah nol        0  1  2  3  4
            [0,0] [0,1] [0,2] . . . [0,y]          
                                 
            - board.states : dict -> Kondisi papan. 
            Key dari states adalah integer sel (0,1,..., x*y)
            Value adalah integer 1 atau 2:
            -> 1 artinya sudah diisi player 1
            -> 2 artinya sudah diisi player 2

            TODO: Tentukan x,y secara greedy. Kembalian adalah sebuah string "x,y"
        """
        myPositions, enemyPositions = self.get_positions(board.states)
        myPositions.sort()
        enemyPositions.sort()
        myPositions = [self.convert_to_coordinate(x) for x in myPositions]
        enemyPositions = [self.convert_to_coordinate(x) for x in enemyPositions]

        myHorizontal = self.get_horizontal(myPositions)
        myHorizontal.sort(key=len, reverse=True)
        myVertical = self.get_vertical(myPositions)
        myVertical.sort(key=len, reverse=True)
        myDiagonal1 = self.get_diagonal1(myPositions)
        myDiagonal1.sort(key=len, reverse=True)
        myDiagonal2 = self.get_diagonal2(myPositions)
        myDiagonal2.sort(key=len, reverse=True)

        myLongestSide, myLongestLine = self.get_longest_line(myHorizontal, myVertical, myDiagonal1, myDiagonal2)
        myAction = self.get_next_position(myLongestSide, myLongestLine, myPositions, enemyPositions)

        x = random.randint(1, board.height)
        y = random.randint(1, board.width)
        if (len(myLongestLine) >= 3 and myAction != (-1, -1)):
            x = myAction[0]
            y = myAction[1]
        else:
            enemyHorizontal = self.get_horizontal(enemyPositions)
            enemyHorizontal.sort(key=len, reverse=True)
            enemyVertical = self.get_vertical(enemyPositions)
            enemyVertical.sort(key=len, reverse=True)
            enemyDiagonal1 = self.get_diagonal1(enemyPositions)
            enemyDiagonal1.sort(key=len, reverse=True)
            enemyDiagonal2 = self.get_diagonal2(enemyPositions)
            enemyDiagonal2.sort(key=len, reverse=True)

            enemyLongestSide, enemyLongestLine = self.get_longest_line(enemyHorizontal, enemyVertical, enemyDiagonal1, enemyDiagonal2)
            enemyAction = self.get_next_position(enemyLongestSide, enemyLongestLine, myPositions, enemyPositions)
            while (len(enemyLongestLine) >= 3 and enemyAction == (-1, -1) and (len(enemyHorizontal) != 0 or len(enemyVertical) != 0 or len(enemyDiagonal1) != 0 or len(enemyDiagonal2) != 0)):
                if (enemyLongestSide == "horizontal"):
                    del enemyHorizontal[0]
                elif (enemyLongestSide == "vertical"):
                    del enemyVertical[0]
                elif (enemyLongestSide == "diagonal1"):
                    del enemyDiagonal1[0]
                elif (enemyLongestSide == "diagonal2"):
                    del enemyDiagonal2[0]
                else:
                    break
                enemyLongestSide, enemyLongestLine = self.get_longest_line(enemyHorizontal, enemyVertical, enemyDiagonal1, enemyDiagonal2)
                enemyAction = self.get_next_position(enemyLongestSide, enemyLongestLine, myPositions, enemyPositions)

            if (len(enemyLongestLine) >= 3 and enemyAction != (-1, -1)):
                x = enemyAction[0]
                y = enemyAction[1]
            else:
                while (myAction == (-1,-1) and (len(myHorizontal) != 0 or len(myVertical) != 0 or len(myDiagonal1) != 0 or len(myDiagonal2) != 0)):
                    if (myLongestSide == "horizontal"):
                        del myHorizontal[0]
                    elif (myLongestSide == "vertical"):
                        del myVertical[0]
                    elif (myLongestSide == "diagonal1"):
                        del myDiagonal1[0]
                    elif (myLongestSide == "diagonal2"):
                        del myDiagonal2[0]
                    else:
                        break
                    myLongestSide, myLongestLine = self.get_longest_line(myHorizontal, myVertical, myDiagonal1, myDiagonal2)
                    myAction = self.get_next_position(myLongestSide, myLongestLine, myPositions, enemyPositions)
                if (myAction != (-1, -1)):
                    x = myAction[0]
                    y = myAction[1]
        return f"{x},{y}"

    def get_positions(self, state: dict):
        myPositions = []
        enemyPositions = []

        for p in state:
            if (state[p] == self.player):
                myPositions.append(p)                
            else:
                enemyPositions.append(p)
        
        return (myPositions, enemyPositions)

    def convert_to_coordinate(self, num: int):
        return (num // 8, num % 8)

    def get_horizontal(self, positions: list):
        horizontalList = []
        if (len(positions) != 0):
            tempList = [positions[0]]
            i = 1
            j = 0

            while (i < len(positions)):
                if (positions[i][0] == tempList[j][0] and (abs(positions[i][1] - tempList[j][1]) == 1)):
                    tempList.append(positions[i])
                    j = j + 1
                else:
                    horizontalList.append(tempList.copy())
                    tempList = [positions[i]]
                    j = 0
                i = i + 1
        
            horizontalList.append(tempList.copy())

        return horizontalList

    def get_vertical(self, positions: list):
        verticalList = []
        tempList = []
        
        for y in range (8):
            prevExist = False
            for x in range (9):
                currentPosition = (x,y)
                if (currentPosition in positions):
                    tempList.append(currentPosition)
                    prevExist = True
                elif (not currentPosition in positions and prevExist):
                    prevExist = False
                    verticalList.append(tempList.copy())
                    tempList.clear()

        return verticalList
    
    def get_diagonal1(self, positions: list):
        diagonal1List = []
        tempList = []

        for y in range (8):
            x = 0
            prevExist = False
            while (x < 9 and y < 9):
                currentPosition = (x, y)
                if (currentPosition in positions):
                    tempList.append(currentPosition)
                    prevExist = True
                elif (not currentPosition in positions and prevExist):
                    prevExist = False
                    diagonal1List.append(tempList.copy())
                    tempList.clear()
                x += 1
                y += 1

        for x in range (1,8):
            y = 0
            prevExist = False
            while (x < 9 and y < 9):
                currentPosition = (x, y)
                if (currentPosition in positions):
                    tempList.append(currentPosition)
                    prevExist = True
                elif (not currentPosition in positions and prevExist):
                    prevExist = False
                    diagonal1List.append(tempList.copy())
                    tempList.clear()
                x += 1
                y += 1

        return diagonal1List
    

    def get_diagonal2(self, positions: list):
        diagonal1List = []
        tempList = []

        for y in range (7, -1, -1):
            x = 0
            prevExist = False
            while (x < 9 and y > -2):
                currentPosition = (x, y)
                if (currentPosition in positions):
                    tempList.append(currentPosition)
                    prevExist = True
                elif (not currentPosition in positions and prevExist):
                    prevExist = False
                    diagonal1List.append(tempList.copy())
                    tempList.clear()
                x += 1
                y -= 1

        for x in range (1,8):
            y = 7
            prevExist = False
            while (x < 9 and y > -1):
                currentPosition = (x, y)
                if (currentPosition in positions):
                    tempList.append(currentPosition)
                    prevExist = True
                elif (not currentPosition in positions and prevExist):
                    prevExist = False
                    diagonal1List.append(tempList.copy())
                    tempList.clear()
                x += 1
                y -= 1

        return diagonal1List
    
    def get_longest_line(self, myHorizontal, myVertical, myDiagonal1, myDiagonal2):
        longestSide = "none"
        longestLine = [(-1, -1)]
        if (len(myHorizontal) != 0):
            longestSide = "horizontal"
            longestLine = myHorizontal[0]
        if (len(myVertical) != 0 and len(myVertical[0]) >= len(longestLine)):
            longestSide = "vertical"
            longestLine = myVertical[0]
        if (len(myDiagonal1) != 0 and len(myDiagonal1[0]) >= len(longestLine)):
            longestSide = "diagonal1"
            longestLine = myDiagonal1[0]
        if (len(myDiagonal2) != 0 and len(myDiagonal2[0]) >= len(longestLine)):
            longestSide = "diagonal2"
            longestLine = myDiagonal2[0]

        return longestSide, longestLine


    def get_next_position(self, longestSide, longestLine, myPositions, enemyPositions):
        if (longestSide == "horizontal"):
            leftSide = (longestLine[0][0], longestLine[0][1]-1)
            if (self.is_input_valid(leftSide, myPositions, enemyPositions)):
                return leftSide
            rightSide = (longestLine[-1][0], longestLine[-1][1]+1)
            if (self.is_input_valid(rightSide, myPositions, enemyPositions)):
                return rightSide
        elif (longestSide == "vertical"):
            upSide = (longestLine[-1][0]+1, longestLine[-1][1])
            if (self.is_input_valid(upSide, myPositions, enemyPositions)):
                return upSide
            bottomSide = (longestLine[0][0]-1, longestLine[0][1])
            if (self.is_input_valid(bottomSide, myPositions, enemyPositions)):
                return bottomSide

        elif (longestSide == "diagonal1"):
            upSide = (longestLine[-1][0]+1, longestLine[-1][1]+1)
            if (self.is_input_valid(upSide, myPositions, enemyPositions)):
                return upSide
            bottomSide = (longestLine[0][0]-1, longestLine[0][1]-1)
            if (self.is_input_valid(bottomSide, myPositions, enemyPositions)):
                return bottomSide
        elif (longestSide == "diagonal2"):
            upSide = (longestLine[-1][0]+1, longestLine[-1][1]-1)
            if (self.is_input_valid(upSide, myPositions, enemyPositions)):
                return upSide
            bottomSide = (longestLine[0][0]-1, longestLine[0][1]+1)
            if (self.is_input_valid(bottomSide, myPositions, enemyPositions)):
                return bottomSide
        return (-1,-1)

    def is_input_valid(self, position, enemyPositions, myPositions):
        return (0 <= position[0] <= 7) and (0 <= position[1] <= 7) and (not position in myPositions) and (not position in enemyPositions)