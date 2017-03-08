# Catherine Javadian, Jennifer Cafiero, and Jordana Approvato
# We pledge our honor that we have abided by the Stevens Honor System
# TO RUN: python ./puzzlesolver.py input.txt

from sys import argv

tiles = []
orientation = [0]*9
tileOrder = [-1]*9
solutions = []

def parse_and_solve():
    """solves the puzzle"""
    global tiles
    tiles = tiles.splitlines()
    for i in range(len(tiles)):
        tiles[i] = tiles[i].split(",")
    used = []
    solve(0,used)

def in_bounds(x_p, y_p):
    """ returns true if x and y are within bounds (0,1,2), otherwise false """
    if (x_p >= 3 or x_p < 0) or (y_p >= 3 or y_p < 0):
        return False
    return True

def align(ori, currT, x_p, y_p, side):
    """ checks to see if the tile will match in the puzzle """
    index = x_p + 3*(y_p)
    checkTile = tiles[tileOrder[index]]
    currS = currT[(ori+side)%4]
    newTS = checkTile[(side+2+orientation[index])%4]
    return (currS[0] == newTS[0]) and (currS[1] != newTS[1])

def tileExists(x_p, y_p):
    """ returns true if the given tile has already been used """
    index = x_p + 3*(y_p)
    checkTile = tileOrder[index]
    if (checkTile == -1):
        return False
    return True

def fits(x_p, y_p, dx, dy, ori, currT, side):
    """ checks if tile is in bounds, exists, and aligns """
    if (in_bounds(x_p+dx, y_p+dy) and tileExists(x_p+dx, y_p+dy)) and not align(ori, currT, x_p+dx, y_p+dy, side) :
        return False
    return True

def fitsAll(x_p, y_p, currT, ori):
    """ checks if all tiles fit """
    if (fits(x_p, y_p, 0, -1, ori, currT,0) and fits(x_p, y_p, 1, 0, ori, currT,1) and fits(x_p, y_p, 0, 1, ori, currT, 2) and fits(x_p, y_p, -1, 0, ori, currT, 3)):
        return True
    return False

def findPiece(used):
    """ finds piece that has not been used yet """
    for i in range(9):
        if not i in used:
            return i
    return -1

def solve(index, used):
    """ finds solution to puzzle using given input and recurssion"""
    tempUsed = list(used)
    piece = findPiece(used)
    global solutions
    if (piece == -1) :
        if (min(tileOrder[0], tileOrder[2], tileOrder[6], tileOrder[8]) == tileOrder[0]):
            sol = [list(tileOrder), list(orientation)]
            solutions.append(list(sol))
    while (piece != -1):
        x_p = index % 3
        y_p = index // 3
        currT = tiles[piece]
        tileOrder[index] = -1
        if (fitsAll(x_p, y_p, currT, 0)):
            tileOrder[index] = piece
            new_used = used + [piece]
            orientation[index] = 0
            solve(index + 1, new_used)
        tileOrder[index] = -1
        if (fitsAll(x_p, y_p, currT, 1)):
            tileOrder[index] = piece
            new_used = used + [piece]
            orientation[index] = 1
            solve(index + 1, new_used)
        tileOrder[index] = -1
        if (fitsAll(x_p, y_p, currT, 2)):
            tileOrder[index] = piece
            new_used = used + [piece]
            orientation[index] = 2
            solve(index + 1, new_used)
        tileOrder[index] = -1
        if (fitsAll(x_p, y_p, currT, 3)):
            tileOrder[index] = piece
            new_used = used + [piece]
            orientation[index] = 3
            solve(index + 1, new_used)
        tempUsed += [piece]
        piece = findPiece(tempUsed)
        tileOrder[index] = -1

def openFile(file):
    """ opens file and returns content """
    myReadFile = open(file, 'r')
    readAll = myReadFile.read()
    myReadFile.close
    return readAll

def main():
    """ runs the full program. does not check for bad args """
    global tiles
    global solutions
    tiles = openFile(argv[1])
    #tiles = "Y1,G0,R0,B1\nY0,B1,R1,B0\nY1,R1,G0,B0\nY1,G0,B0,G1\nB0,G0,R1,Y1\nY0,G1,R1,B0\nR0,B1,Y1,G0\nY0,R1,B1,G0\nR0,G1,Y1,B0"
    parse_and_solve()
    printInput()
    print_all_sols()

def printInput():
    """ prints the initial values from the input file """
    print("Input tiles:")
    for i in range(9):
        print(str(i+1) + ". <" + tiles[i][0] + ", " + tiles[i][1] + ", " + tiles[i][2] + ", " + tiles[i][3] + ">")
    print("")

def printTopRow1(sol):
    """ prints the top top row """
    ori1 = sol[1][0]
    ori2 = sol[1][1]
    ori3 = sol[1][2]
    tile1 = tiles[sol[0][0]]
    tile2 = tiles[sol[0][1]]
    tile3 = tiles[sol[0][2]]
    piece1 = tile1[ori1]
    piece2 = tile2[ori2]
    piece3 = tile3[ori3]
    print("|" + (str(sol[0][0]+1)) + "  " + str(piece1) + "   |" + (str(sol[0][1]+1)) + "  " + str(piece2) + "   |" + (str(sol[0][2]+1)) + "  " + str(piece3) + "   |")

def printMidRow2(sol):
    """ prints the top middle row """
    ori1 = sol[1][0]
    ori2 = sol[1][1]
    ori3 = sol[1][2]
    tile1 = tiles[sol[0][0]]
    tile2 = tiles[sol[0][1]]
    tile3 = tiles[sol[0][2]]
    piece1_l = tile1[(ori1+3)%4]
    piece2_l = tile2[(ori2+3)%4]
    piece3_l = tile3[(ori3+3)%4]
    piece1_r = tile1[(ori1+1)%4]
    piece2_r = tile2[(ori2+1)%4]
    piece3_r = tile3[(ori3+1)%4]
    print("|" + str(piece1_l) + "    " + str(piece1_r) + "|" + str(piece2_l) + "    " + str(piece2_r) + "|" + str(piece3_l) + "    " + str(piece3_r) + "|")

def printBotRow3(sol):
    """ prints the top bottom row """
    ori1 = sol[1][0]
    ori2 = sol[1][1]
    ori3 = sol[1][2]
    tile1 = tiles[sol[0][0]]
    tile2 = tiles[sol[0][1]]
    tile3 = tiles[sol[0][2]]
    piece1 = tile1[(ori1+2)%4]
    piece2 = tile2[(ori2+2)%4]
    piece3 = tile3[(ori3+2)%4]
    print("|   " + str(piece1) + "   |   " + str(piece2) + "   |   " + str(piece3) + "   |")

def printTopRow4(sol):
    """ prints the middle top row """
    ori1 = sol[1][3]
    ori2 = sol[1][4]
    ori3 = sol[1][5]
    tile1 = tiles[sol[0][3]]
    tile2 = tiles[sol[0][4]]
    tile3 = tiles[sol[0][5]]
    piece1 = tile1[ori1]
    piece2 = tile2[ori2]
    piece3 = tile3[ori3]
    print("|" + str(sol[0][3]+1) + "  " + str(piece1) + "   |" + str(sol[0][4]+1) + "  " + str(piece2) + "   |" + str(sol[0][5]+1) + "  " + str(piece3) + "   |")

def printMidRow5(sol):
    """ prints the middle middle row """
    ori1 = sol[1][3]
    ori2 = sol[1][4]
    ori3 = sol[1][5]
    tile1 = tiles[sol[0][3]]
    tile2 = tiles[sol[0][4]]
    tile3 = tiles[sol[0][5]]
    piece1_l = tile1[(ori1+3)%4]
    piece2_l = tile2[(ori2+3)%4]
    piece3_l = tile3[(ori3+3)%4]
    piece1_r = tile1[(ori1+1)%4]
    piece2_r = tile2[(ori2+1)%4]
    piece3_r = tile3[(ori3+1)%4]
    print("|" + str(piece1_l) + "    " + str(piece1_r) + "|" + str(piece2_l) + "    " + str(piece2_r) + "|" + str(piece3_l) + "    " + str(piece3_r) + "|")

def printBotRow6(sol):
    """ prints the middle bottom row """
    ori1 = sol[1][3]
    ori2 = sol[1][4]
    ori3 = sol[1][5]
    tile1 = tiles[sol[0][3]]
    tile2 = tiles[sol[0][4]]
    tile3 = tiles[sol[0][5]]
    piece1 = tile1[(ori1+2)%4]
    piece2 = tile2[(ori2+2)%4]
    piece3 = tile3[(ori3+2)%4]
    print("|   " + str(piece1) + "   |   " + str(piece2) + "   |   " + str(piece3) + "   |")

def printTopRow7(sol):
    """ prints the bottom top row """
    ori1 = sol[1][6]
    ori2 = sol[1][7]
    ori3 = sol[1][8]
    tile1 = tiles[sol[0][6]]
    tile2 = tiles[sol[0][7]]
    tile3 = tiles[sol[0][8]]
    piece1 = tile1[ori1]
    piece2 = tile2[ori2]
    piece3 = tile3[ori3]
    print("|" + (str(sol[0][6]+1)) + "  " + str(piece1) + "   |" + (str(sol[0][7]+1)) + "  " + str(piece2) + "   |" + (str(sol[0][8] + 1)) + "  " + str(piece3) + "   |")

def printMidRow8(sol):
    """ prints the bottom middle row """
    ori1 = sol[1][6]
    ori2 = sol[1][7]
    ori3 = sol[1][8]
    tile1 = tiles[sol[0][6]]
    tile2 = tiles[sol[0][7]]
    tile3 = tiles[sol[0][8]]
    piece1_l = tile1[(ori1+3)%4]
    piece2_l = tile2[(ori2+3)%4]
    piece3_l = tile3[(ori3+3)%4]
    piece1_r = tile1[(ori1+1)%4]
    piece2_r = tile2[(ori2+1)%4]
    piece3_r = tile3[(ori3+1)%4]
    print("|" + str(piece1_l) + "    " + str(piece1_r) + "|" + str(piece2_l) + "    " + str(piece2_r) + "|" + str(piece3_l) + "    " + str(piece3_r) + "|")

def printBotRow9(sol):
    """ prints the bottom bottom row """
    ori1 = sol[1][6]
    ori2 = sol[1][7]
    ori3 = sol[1][8]
    tile1 = tiles[sol[0][6]]
    tile2 = tiles[sol[0][7]]
    tile3 = tiles[sol[0][8]]
    piece1 = tile1[(ori1+2)%4]
    piece2 = tile2[(ori2+2)%4]
    piece3 = tile3[(ori3+2)%4]
    print("|   " + str(piece1) + "   |   " + str(piece2) + "   |   " + str(piece3) + "   |")

def print_all_sols():
    """ prints all solutions """
    numSol = len(solutions)
    if (numSol == 0):
        print("No solutions found.")
        return
    if (numSol == 1):
        print("1 unique solution found:")
    else:
        print(str(len(solutions)) + " unique solutions found:")
    for i in range(numSol):
        print("+--------+--------+--------+")
        printTopRow1(solutions[i])
        printMidRow2(solutions[i])
        printBotRow3(solutions[i])
        print("+--------+--------+--------+")
        printTopRow4(solutions[i])
        printMidRow5(solutions[i])
        printBotRow6(solutions[i])
        print("+--------+--------+--------+")
        printTopRow7(solutions[i])
        printMidRow8(solutions[i])
        printBotRow9(solutions[i])
        print("+--------+--------+--------+\n")

main()
