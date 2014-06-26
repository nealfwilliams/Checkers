import copy
import random
def evaluate(board):
    sum = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if type(board[i][j]) is int:
                sum = sum + board[i][j]
    return sum

def getmoves(player, board):
    moves= []
    for i in range(1,len(board)-1):
        for j in range(1,len(board[i])-1):
            if board[i][j]*player > 0:
                king = bool(board[i][j]*player-1)
                jumptree = [[copy.deepcopy(board),i,j]]
                index = 0
                while (index < len(jumptree)):
                    jumps = find_jumps(player, jumptree[index][0], jumptree[index][1], jumptree[index][2], king)
                    if jumps:
                        jumptree.extend(jumps)
                        jumptree[index]=False
                    index = index + 1
                jumptree[0] = False
                for jump in jumptree:
                    if jump:
                        moves.append(jump[0])
    if len(moves) == 0:
        for i in range(len(board)):     
            for j in range(len(board)):
                value = board[i][j]
                if value==player*1 or value==player*2:
                    if board[i+player][j-1]==0:
                        temp = copy.deepcopy(board)
                        temp[i+player][j-1]=value
                        temp[i][j]=0 
                        moves.append(temp)
                    if board[i+player][j+1]==0:
                        temp = copy.deepcopy(board)
                        temp[i+player][j+1]=value
                        temp[i][j]=0
                        moves.append(temp)
                if value==player*2:
                    if board[i-player][j-1]==0:
                        temp = copy.deepcopy(board)
                        temp[i-player][j-1]=value
                        temp[i][j]=0
                        moves.append(temp)
                    if board[i-player][j+1]==0:
                        temp = copy.deepcopy(board)
                        temp[i-player][j+1]=value
                        temp[i][j]=0
                        moves.append(temp)

    for move in moves:
        for i in range(len(move)):
                if move[1][i] == -1:
                    move[1][i] = -2
                if move[8][i] == 1:
                    move[8][i] = 2
    return moves

def tostring(board):
    render = list(board)
    string = '   |_1_|_2_|_3_|_4_|_5_|_6_|_7_|_8_|\n'
    for i in range(len(render)):
        if not (i==0 or i==9):
            string = string + ' ' + chr(i+64).upper() + ' |'
            for j in range(len(render[i])):
                if not (j==0 or j==9):
                    temp = render[i][j]
                    if temp == -1:
                        temp = 'x'
                    elif temp == -2:
                        temp = 'X'
                    elif temp == 1:
                        temp = 'o'
                    elif temp == 2: 
                        temp = 'O'     
                    elif (i+j)%2==0:
                        temp=' '
                    else:
                        temp = False
                        string = string + '||||'
                    if temp:
                        string = string + ' ' + str(temp) + ' |'
            string = string + "\n   _________________________________\n"
    return string

def find_jumps(player, board, row, col, king):
    jumps = []
    if board[row+player][col-1]*player<0:
        if board[row+player*2][col-2]==0:
            temp = copy.deepcopy(board)
            temp[row][col]=0
            temp[row+player][col-1]=0
            temp[row+player*2][col-2]=player*(1+int(king))
            jumps.append([temp,row+player*2,col-2])
    if board[row+player][col+1]*player<0:
        if board[row+player*2][col+2]==0:
            temp = copy.deepcopy(board)
            temp[row][col]=0
            temp[row+player][col+1]=0
            temp[row+player*2][col+2]=player*(1+int(king))
            jumps.append([temp,row+player*2,col+2])
    if king:
        if board[row-player][col-1]*player<0:
            if board[row-player*2][col-2]==0:
                temp = copy.deepcopy(board)
                temp[row][col]=0
                temp[row-player][col-1]=0
                temp[row-player*2][col-2]=player*2
                jumps.append([temp,row-player*2,col-2]) 
        if board[row-player][col+1]*player<0:
            if board[row-player*2][col+2]==0:
                temp = copy.deepcopy(board)
                temp[row][col]=0
                temp[row-player][col+1]=0
                temp[row-player*2][col+2]=player*2
                jumps.append([temp,row-player*2,col+2]) 
    return jumps 

def computer_move(board, player, dif, count, top):
    if count == dif:
        return evaluate(board)
    moves = getmoves(player, board)
    movedict = {}
    for i in range(len(moves)):
        value = computer_move(moves[i],player*-1,dif, count+1, False)
        movedict[value*player]=i
    if movedict:
        value = max(val for val in movedict)
    else:
        value = float('-inf')
    if top:
        return moves[movedict[value]]
    return player*value
     
class Game():	

    def __init__(self):
        self.board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], ['*', 1, 0, 1, 0, 1, 0, 1, 0, '*'], ['*', 0, 1, 0, 1, 0, 1, 0, 1, '*'], ['*', 1, 0, 1, 0, 1, 0, 1, 0, '*'], ['*', 0, 0, 0, 0, 0, 0, 0, 0, '*'], ['*', 0, 0, 0, 0, 0, 0, 0, 0, '*'], ['*', 0, -1, 0, -1, 0, -1, 0, -1, '*'], ['*', -1, 0, -1, 0, -1, 0, -1, 0, '*'], ['*', 0, -1, 0, -1, 0, -1, 0, -1, '*'], ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self.winner = 0
        self.difficulty = 1
    def set_dif(self, num):
        self.difficulty = int(num)
    def player_turn(self):
        newboard = copy.deepcopy(self.board)
        moves = getmoves(-1, self.board)
        if not moves:
            self.winner = 2 
            return   
        move = raw_input('Enter your move: ')
        rows = {'A','B','C','D','E','F','G','H'}
        cols = {'1','2','3','4','5','6','7','8'}
        args = []
        args.extend([move[i] for i in range(len(move))])
        i, j = args[0:2]
        moves = args[2:]
        i = ord(i)-64 
        j = int(j)
        value = newboard[i][j]
        for move in moves:
            if move == 'q':
                newboard[i][j]=0
                newboard[i-1][j-1]=value
                i,j = i-1,j-1
            if move == 'Q':
                newboard[i][j]=0
                newboard[i-1][j-1]=0
                newboard[i-2][j-2]=value
                i,j = i-2,j-2
            if move == 'w':       
                newboard[i][j]=0
                newboard[i-1][j+1]=value
                i,j = i-1,j+1
            if move == 'W':       
                newboard[i][j]=0
                newboard[i-1][j+1]=0
                newboard[i-2][j+2]=value
                i,j = i-2,j+2
            if move == 'a':
                newboard[i][j]=0
                newboard[i+1][j-1]=value
                i,j = i+1,j-1
            if move == 'A':
                newboard[i][j]=0
                newboard[i+1][j-1]=0
                newboard[i+2][j-2]=value
                i,j = i+2,j-2
            if move == 's': 
                newboard[i][j]=0
                newboard[i+1][j+1]=value
                i,j = i+1,j+1
            if move == 'S':
                newboard[i][j]=0
                newboard[i+1][j+1]=0
                newboard[i+2][j+2]=value
                i,j = i+2,j+2
        for i in range(len(newboard)):
            if newboard[1][i] == -1:
                newboard[1][i] = -2
            if newboard[8][i] == 1:
                newboard[8][i] = 2
        
        if newboard in getmoves(-1, self.board):
            self.board = newboard
            return 0
        else:
            self.player_turn()
    def computer_turn(self):
        if self.winner:
            return self.winner
        if not getmoves(1, self.board):
            return 1
        self.board = computer_move(self.board, 1, self.difficulty, 0, True)
        return 0        
    def declare_winner(self, winner):
        self.winner = winner
        if winner == 1:
            print "Congratulations you win!"
        if winner == 2:
            print "You lose.  Better luck next time!"
    def __str__(self):
        return tostring(self.board) 
          
            
if __name__ == "__main__":
    game = Game()
    print "\n\nTo enter a move, first enter the coordinates of the piece you want to move,\nthen choose which direction to move using the characters 'q' for forward left, \n'w' for forward right, 'a' for back left, and 's' for back right (only kings can move back). \nCapital the direction letter to initiate a jump.  \nIf one or more jumps are possible, you must jump. \nIn order to initiate multi-jump, enter the directions of the jumps in order.  \n\nExample moves: F1w  G2Q D3WQ\n\n"
    difficulty = raw_input('Enter difficulty: ')
    game.set_dif(difficulty)
    while not game.winner:
        print game
        game.player_turn()
        game.declare_winner(game.computer_turn())
        
