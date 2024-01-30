# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 99642 André Bento
# 99656 Diogo Guerreiro
import time
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import copy

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self,grid,blankPositions,rowMax,colMax,colSum,rowSum,hintList,shipOneLeft, hintListEdit, lastPlayed):
        self.grid = grid
        self.blankPositions = blankPositions
        self.rowMax = rowMax
        self.colMax = colMax
        self.colSum = colSum
        self.rowSum = rowSum
        self.hintList = hintList
        self.hintListEdit= hintListEdit
        self.shipOneLeft = shipOneLeft
        self.shipTwoLeft = 3
        self.shipThreeLeft = 2
        self.shipFourLeft = 1
        self.lastPlayed = lastPlayed
 

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.is_valid_position(row,col):
            return self.grid[row][col]
        return None
    
    def set_value (self, row: int , col: int, value: str ):
        if self.is_valid_position (row, col):
            self.grid[row][col] = value
    
    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if self.is_valid_position (row -1, col):
            up = self.get_value(row-1, col)
        else:
            up = None
        if self.is_valid_position (row +1, col):
            down = self.get_value( row +1, col)
        else:
            down = None
        return (up, down)
    
    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if self.is_valid_position(row,col-1):
            left=self.get_value(row,col-1)
        else:
            left=None
        if self.is_valid_position(row,col+1):
            right=self.get_value(row,col+1)
        else:
            right=None
        return (left,right)
    
    def is_valid_position(self,row,col):
        return 0<=row<=9 and 0<=col<=9
    
    def copyBoard (self):
        newBoard = copy.deepcopy(self)
        return newBoard
    
    #Devolve True se o limite da linha for excedido e False se não
    def checkRowLimit (self, row:int):
        if self.rowSum[row] > self.rowMax[row]:
            return True
        else:
            return False
    
    #Devolve True se o limite da coluna for excedido e False se não
    def checkColLimit (self, col:int ):
        if self.colSum[col] > self.colMax[col]:
            return True
        else:
            return False
        
    #Devolve True se houver colisão
    def checkBoatColision_aux (self, row:int, col: int, lenght: int, position: str):
        aguas=["W","."]
        if position == 'H':
            
            if lenght == 1:
                listaH1 =[[row+1,col-1],[row+1,col],[row+1,col+1],[row,col-1],[row,col+1],[row-1,col-1],[row-1,col],[row-1,col+1]]
                for item in listaH1:
                    if self.is_valid_position (item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            elif lenght == 2:
                listaH2 = [[row-1,col-1],[row-1,col],[row-1,col+1],[row-1,col+2],[row,col-1],[row,col+2],[row+1,col-1],[row+1,col],[row+1,col+1],[row+1,col+2]]
                for item in listaH2:
                    if self.is_valid_position (item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            elif lenght == 3:
                listaH3 = [[row-1,col-1],[row-1,col],[row-1,col+1],[row-1,col+2],[row-1,col+3],[row,col-1],[row,col+3],[row+1,col-1],[row+1,col],[row+1,col+1],[row+1,col+2],[row+1,col+3]]
                for item in listaH3:
                    if self.is_valid_position(item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            elif lenght == 4:
                listaH4 =[[row-1,col-1],[row-1,col],[row-1,col+1],[row-1,col+2],[row-1,col+3],[row-1,col+4],[row,col-1],[row,col+4],[row+1,col-1],[row+1,col],[row+1,col+1],[row+1,col+2],[row+1,col+3],[row+1,col+4]]
                for item in listaH4:
                    if self.is_valid_position(item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            return False
                
        if position=='V':
            if lenght == 1:
                listaV1=[[row+1,col-1],[row+1,col],[row+1,col+1],[row,col-1],[row,col+1],[row-1,col-1],[row-1,col],[row-1,col+1]]
                for item in listaV1:
                    if self.is_valid_position (item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            elif lenght == 2:
                listaV2=[[row-1,col-1],[row-1,col],[row-1,col+1],[row,col-1],[row,col+1],[row+1,col-1],[row+1,col+1],[row+2,col-1],[row+2,col],[row+2,col+1]]
                for item in listaV2:
                    if self.is_valid_position (item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            elif lenght == 3:
                listaV3=[[row-1,col-1],[row-1,col],[row-1,col+1],[row+1,col-1],[row+1,col+1],[row+2,col-1],[row+2,col+1],[row+3,col-1],[row+3,col],[row+3,col+1]]
                for item in listaV3:
                    if self.is_valid_position (item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            elif lenght == 4:
                listaV4=[[row-1,col-1],[row-1,col],[row-1,col+1],[row+1,col-1],[row+1,col+1],[row+2,col-1],[row+2,col+1],[row+3,col-1],[row+3,col+1],[row+4,col-1],[row+4,col],[row+4,col+1]]
                for item in listaV4:
                    if self.is_valid_position (item[0], item[1]) and self.get_value(item[0], item[1]) not in aguas:
                        return True
            return False
    
#-----------------------------------------------------------------------------------------------------------------------------------------------    
#Funções que vamos usar só para o input
    def addWaterToHints (self):
        water=["W", "."]
        for hint in self.hintList:
            if hint[2] != "W":
                if hint[2] == "T":
                    listT = [[hint[0],hint[1]-1],[hint[0],hint[1]+1],[hint[0]-1,hint[1]-1],[hint[0]-1,hint[1]],[hint[0]-1,hint[1]+1],[hint[0]+1,hint[1]-1],[hint[0]+1,hint[1]+1]]
                    for item in listT:
                        if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                            self.blankPositions.remove((item[0],item[1]))
                            self.set_value(item[0],item[1], ".")
                elif hint[2] == "R":
                    listR = [[hint[0]-1,hint[1]],[hint[0]+1,hint[1]],[hint[0]-1,hint[1]+1],[hint[0],hint[1]+1],[hint[0]+1,hint[1]+1], [hint[0]+1,hint[1]-1], [hint[0]-1,hint[1]-1]]
                    for item in listR:
                        if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                            self.blankPositions.remove((item[0],item[1]))
                            self.set_value(item[0],item[1], ".")
                elif hint[2] == "B":
                    listB = [[hint[0],hint[1]-1],[hint[0],hint[1]+1],[hint[0]+1,hint[1]+1],[hint[0]+1,hint[1]-1],[hint[0]+1,hint[1]],[hint[0]-1,hint[1]-1],[hint[0]-1,hint[1]+1]]
                    for item in listB:
                        if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                            self.blankPositions.remove((item[0],item[1]))
                            self.set_value(item[0],item[1], ".")
                elif hint[2] == "L":
                    listL = [[hint[0]-1,hint[1]],[hint[0]+1,hint[1]],[hint[0]+1,hint[1]-1],[hint[0],hint[1]-1],[hint[0]-1,hint[1]-1],[hint[0]-1,hint[1]+1],[hint[0]+1,hint[1]+1]]
                    for item in listL:
                        if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                            self.blankPositions.remove((item[0],item[1]))
                            self.set_value(item[0],item[1], ".")    
                elif hint[2] == "C":
                    listC = [[hint[0]-1,hint[1]-1],[hint[0]-1,hint[1]],[hint[0]-1,hint[1]+1],[hint[0],hint[1]-1],[hint[0],hint[1]+1],[hint[0]+1,hint[1]-1],[hint[0]+1,hint[1]],[hint[0]+1,hint[1]+1]]
                    for item in listC:
                        if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                            self.blankPositions.remove((item[0],item[1]))
                            self.set_value(item[0],item[1], ".") 
                elif hint[2] == "M":
                    if self.adjacent_horizontal_values(hint[0], hint[1])[0] in water or self.adjacent_horizontal_values(hint[0], hint[1])[1] in water:
                        listM = [[hint[0]+1,hint[1]-1],[hint[0]+1,hint[1]+1],[hint[0],hint[1]-1],[hint[0],hint[1]+1],[hint[0]-1,hint[1]-1],[hint[0]-1,hint[1]+1], [hint[0]-2,hint[1]-1], [hint[0]-2,hint[1]+1],[hint[0]+2,hint[1]+1], [hint[0]+2,hint[1]-1]]
                        for item in listM:
                            if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                                self.blankPositions.remove((item[0],item[1]))
                                self.set_value(item[0],item[1], ".")

                    elif self.adjacent_vertical_values(hint[0], hint[1])[0] in water or self.adjacent_vertical_values(hint[0], hint[1])[1] in water:
                        listM = [[hint[0]+1,hint[1]-1],[hint[0]-1,hint[1]-1],[hint[0]+1,hint[1]],[hint[0]-1,hint[1]],[hint[0]+1,hint[1]+1],[hint[0]-1,hint[1]+1],[hint[0]-1,hint[1]-2], [hint[0]+1,hint[1]-2],[hint[0]-1,hint[1]+2], [hint[0]+1,hint[1]+2]]
                        for item in listM:
                            if self.is_valid_position(item[0],item[1]) and self.get_value(item[0],item[1]) == " ":
                                self.blankPositions.remove((item[0],item[1]))
                                self.set_value(item[0],item[1], ".")
    


    def fillRowColWithWater(self):
        for i in range(10):
            self.fillRowWithWater(i)
            self.fillColWithWater(i)
    
    
    
    #Tamos a dizer que as rows vão de 0 a 9
    def fillRowWithWater (self, row: int):
        if self.rowMax[row] == self.rowSum[row]:
            for i in range(10):
                if self.grid[row][i] == " ":
                    self.blankPositions.remove((row,i))
                    self.set_value(row, i, '.')


    #Tamos a dizer que as cols vão de 0 a 9
    def fillColWithWater (self, col: int):
        if self.colMax[col] == self.colSum[col]:
            for i in range(10):
                if self.grid[i][col] == " ":
                    self.blankPositions.remove((i,col))
                    self.set_value(i,col, '.')
            


    def remove_boat(self,boat_type):
        if (boat_type==2):
            self.shipTwoLeft-=1
        elif (boat_type==3):
            self.shipThreeLeft-=1
        elif (boat_type==4):
            self.shipFourLeft-=1
        

    def eliminate_hint(self,to_delete : list):
        for hintToEliminate in to_delete:
            self.hintListEdit.remove(hintToEliminate)        

        

    def update_boat(self):
        for i in range(10):
            for j in range(10):
                if self.get_value(i,j)=='L':
                    to_delete=[]
                    to_delete.append((i,j,self.get_value(i,j)))
                    counter=1
                    boat_type=0
                    j=j+1
                    
                    
                    while (j<10):
                        if(self.get_value(i,j)=='M'):
                            
                            to_delete.append((i,j,self.get_value(i,j)))
                            counter+=1
                        elif(self.get_value(i,j)=='R'):
                            counter+=1
                            to_delete.append((i,j,self.get_value(i,j)))

                            boat_type=counter
                            
                            self.eliminate_hint(to_delete)
                            self.remove_boat(boat_type)
                        else:
                            to_delete = []
                            break
                        j+=1

        for j in range(10):
            for i in range(10):
                if self.get_value(i,j)=='T':
                    to_delete=[]
                    to_delete.append((i,j,self.get_value(i,j)))
                    counter=1
                    boat_type=0
                    i=i+1
                    
                    while (i<10):
                        if(self.get_value(i,j)=='M'):
                            to_delete.append((i,j,self.get_value(i,j)))
                            counter+=1
                        elif(self.get_value(i,j)=='B'):
                            counter+=1
                            to_delete.append((i,j,self.get_value(i,j)))
                            boat_type=counter
                            self.eliminate_hint(to_delete)
                            self.remove_boat(boat_type)
                        else:
                            to_delete =[]
                            break
                        i+=1
#--------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """

        grid =[[' ' for _ in range(10) ] for _ in range(10)]
        counter= 0
        rowAndCol=[]

        shipOneLeft=4
        for line in sys.stdin:
            if counter == 2:
                break
            rowAndCol.append(line)
            counter+=1

        rowMax = [int(val) for val in rowAndCol[0].split()[1:]]
        colMax = [int(val) for val in rowAndCol[1].split()[1:]]


        rowSum = 10*[0]
        colSum= 10*[0]

        hintList=[]
        hintListEdit=[]

        
        counter = 0
        lines = []
        for line in sys.stdin:
            lines.append(line)

        blankPositions = [(i, j) for i in range(10) for j in range(10)]
        
        boats=["T", "R", "B", "L", "M", "C"]
        for hint in lines:
            hint_split = hint.split()
            tuplo = (int(hint_split[1]), int(hint_split[2]), hint_split[3])
            hintList.append(tuplo)
            if hint_split[3] != "C" and hint_split[3] != "W":
                hintListEdit.append(tuplo)    
            grid[tuplo[0]] [tuplo[1]] = tuplo[2]
            blankPositions.remove((tuplo[0], tuplo[1]))
            if hint[3] == "C":
                shipOneLeft -=1

            if tuplo[2] in boats:
                rowSum[tuplo[0]] +=1
                colSum[tuplo[1]] +=1

        board = Board(grid,blankPositions,rowMax,colMax,colSum,rowSum,hintList,shipOneLeft, hintListEdit, (-1,-1,-1,-1))

        return board
    
    #da print do board
    def __str__(self) -> str:
        res = ""
        self.giveNameBoats ()
        for hint in self.hintList:
            self.set_value (hint[0], hint[1], hint[2])
        for i in range(10):
            for j in range(10):
                val = self.grid[i][j]
                res += str(val)
            if i != 9:
                res += "\n"
        return res
    
    def giveNameBoats(self):
        for i in range(10):
            for j in range (10):
                if self.get_value(i,j) == 'X':
                    if self.isLeft (i,j):
                        self.set_value(i,j,'l')
                    elif self.isRight(i,j):
                        self.set_value(i,j,'r')
                    elif self.isTop(i,j):
                        self.set_value(i,j,'t')
                    elif self.isCircle(i,j):
                        self.set_value(i,j,'c')
                    elif self.isBottom(i,j):
                        self.set_value(i,j,'b')
                    else:
                        self.set_value(i,j,'m')


    #se for left dá TRUE
    def isLeft (self, row, col):
        aguas =["W", "."]
        boats =['X', 'm', 't', 'b', 'r']
        lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row+1,col-1),(row+1,col),(row+1,col+1)]
        for item in lista:
            if self.is_valid_position (item[0], item[1]) and self.get_value (item[0], item[1]) not in aguas:
                return False
        if self.get_value (row, col +1) not in boats:
            return False
        return True
    
    def isCircle (self, row, col):
        aguas =["W", "."]
        lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row, col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
        if (self.get_value(row, col)!='X'):
            return False
        for item in lista:
                if self.is_valid_position (item[0], item[1]) and self.get_value (item[0], item[1]) not in aguas:
                    return False

        return True
        

    def isTop (self,row,col):
        aguas =["W", "."]
        boats =['X', 'm', 'b', 'r', 'l']
        lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col+1)]
        for item in lista:
            if self.is_valid_position (item[0], item[1]) and self.get_value (item[0], item[1]) not in aguas:
                return False
        if self.get_value (row+1, col) not in boats:
            return False
        return True
    
    def isBottom (self,row,col):
        aguas =["W", "."]
        boats =['X', 'm', 't', 'r', 'l']
        lista=[(row-1,col-1),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1, col),(row+1,col+1)]
        for item in lista:
            if self.is_valid_position (item[0], item[1]) and self.get_value (item[0], item[1]) not in aguas:
                return False
        if self.get_value (row-1, col) not in boats:
            return False
        return True
    
    
    def isRight(self,row,col):
            aguas =["W", "."]
            boats =['X', 'm', 't', 'b', 'l']
            lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
            for item in lista:
                if self.is_valid_position (item[0], item[1]) and self.get_value (item[0], item[1]) not in aguas:
                    return False
            if self.get_value (row, col -1) not in boats:
                return False
            return True

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        board.addWaterToHints()
        board.fillRowColWithWater()
        board.update_boat()
        self.initial=BimaruState(board)
        

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        #Vai ver as actions possiveis de fazer com as hints
        if state.board.hintListEdit != []:
            for hint in state.board.hintListEdit:
                if hint[2] == "L":
                    actions_possiveis =[(hint[0], hint[1], 2,'H',("NULL")), (hint[0], hint[1], 3,'H', ("NULL")), (hint[0], hint[1], 4,'H', ("NULL"))]
                    for action in actions_possiveis:
                        if self.doesActionFit (state, action) == True:
                            actions.append(action)
                elif hint[2] == "R":
                    actions_possiveis =[(hint[0], hint[1]-1, 2,'H', ("NULL")), (hint[0], hint[1]-2, 3,'H', ("NULL")), (hint[0], hint[1]-3, 4,'H', ("NULL"))]
                    for action in actions_possiveis:
                        if self.doesActionFit (state,action) == True:
                            actions.append(action)
                elif hint[2] == "T":
                    actions_possiveis =[(hint[0], hint[1], 2,'V', ("NULL")), (hint[0], hint[1], 3,'V', ("NULL")), (hint[0], hint[1], 4,'V', ("NULL"))]
                    for action in actions_possiveis:
                        if self.doesActionFit (state,action) == True:
                            actions.append(action)
                elif hint[2] == "B":
                    actions_possiveis =[(hint[0]-1, hint[1], 2,'V', ("NULL")), (hint[0]-2, hint[1], 3,'V', ("NULL")), (hint[0]-3, hint[1], 4,'V', ("NULL"))]
                    for action in actions_possiveis:
                        if self.doesActionFit (state,action) == True:
                            actions.append(action)
                elif hint[2] == "M":
                    actions_possiveis =[(hint[0], hint[1]-2, 4,'H',("NULL")), (hint[0], hint[1]-1, 4,'H', ("NULL")), (hint[0], hint[1]-1, 3,'H', ("NULL")), (hint[0]-2, hint[1], 4,'V',("NULL")), (hint[0]-1, hint[1], 4,'V', ("NULL")), (hint[0]-1, hint[1], 3,'V', ("NULL"))]
                    for action in actions_possiveis:
                        if self.doesActionFit (state,action) == True:
                            actions.append(action)
            return actions
        
        #Vai ver as actions possiveis de fazer com barcos de 4
        elif state.board.shipFourLeft > 0:
            for space in state.board.blankPositions:
                actions_possiveis =[(space[0], space[1], 4, 'H'), (space[0], space[1], 4, 'V')]
                for action in actions_possiveis:
                    if self.doesActionFit (state,action) == True:
                        actions.append(action)
  
            return actions
        #Vai ver as actions possiveis de fazer com barcos de 3
        elif state.board.shipThreeLeft > 0:
            for space in state.board.blankPositions:
                actions_possiveis =[(space[0], space[1], 3, 'H'), (space[0], space[1], 3, 'V')]
                for action in actions_possiveis:
                    if self.doesActionFit (state,action) == True:
                        actions.append(action)

            return actions
        
        #Vai ver as actions possiveis de fazer com barcos de 2
        elif state.board.shipTwoLeft > 0:
            for space in state.board.blankPositions:
                actions_possiveis =[(space[0], space[1], 2, 'H'), (space[0], space[1], 2, 'V')]
                for action in actions_possiveis:
                    if self.doesActionFit (state,action) == True:
                        actions.append(action)

            return actions
        
        #Vai ver as actions possiveis de fazer com barcos de 1
        elif state.board.shipOneLeft > 0:
            for space in state.board.blankPositions:
                actions_possiveis =[(space[0], space[1], 1, 'H')]
                for action in actions_possiveis:
                    if self.doesActionFit (state,action) == True:
                        actions.append(action)

            return actions
        
            

    #Recebe uma action e ve se dá para por -> vê se as posições tao a NULL ou se é uma hint
    def doesActionFit (self, state, action):
        hints=['R','L','B','T','C','M']
        row = action[0]
        col = action[1]
        lenght = action[2]
        position = action[3]
        if position == "H":
            if lenght == 4:
                lista =[(row,col),(row,col+1),(row,col+2),(row,col+3)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
            if lenght == 3:
                lista =[(row,col),(row,col+1),(row,col+2)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
            if lenght == 2:
                lista =[(row,col),(row,col+1)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
            if lenght == 1:
                lista =[(row,col)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
        if position == "V":
            if lenght == 4:
                lista =[(row,col),(row+1,col),(row+2,col),(row+3,col)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
            if lenght == 3:
                lista =[(row,col),(row+1,col),(row+2,col)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
            if lenght == 2:
                lista =[(row,col),(row+1,col)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True
            if lenght == 1:
                lista =[(row,col)]
                for item in lista:
                    if not (state.board.is_valid_position (item[0], item[1]) and (state.board.get_value(item[0], item[1]) == " " or state.board.get_value(item[0], item[1]) in hints)):
                        return False
                return True

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        

        new_board = state.board.copyBoard()
        row = action[0]
        col = action[1]
        lenght = action[2]
        position = action[3]

        #Vai meter o barco no local da action com a posicao e tamanho dado
        if position == 'H':
            if lenght == 4:
                lista = [(row, col), (row, col+1), (row, col+2), (row, col+3)]
                waterlist =[(row-1,col-1),(row-1,col),(row-1,col+1),(row-1,col+2),(row-1,col+3),(row-1, col+4),(row,col-1),(row,col+4),(row+1,col-1),(row+1,col),(row+1,col+1),(row+1,col+2),(row+1,col+3),(row+1,col+4)]
                self.addShipH (state, new_board, row, col, lista, waterlist)
                new_board.shipFourLeft -=1
            elif lenght == 3:
                lista = [(row, col), (row, col+1), (row, col+2)]
                waterlist =[(row-1, col-1), (row-1, col), (row-1, col+1), (row-1, col+2), (row-1, col+3), (row, col-1),(row, col+3), (row+1, col-1), (row+1, col), (row+1, col+1), (row+1, col+2), (row+1, col+3)]
                self.addShipH (state, new_board, row, col, lista, waterlist)
                new_board.shipThreeLeft -=1
            elif lenght == 2:
                lista = [(row, col), (row, col+1)]
                waterlist =[(row-1, col-1),(row-1, col),(row-1, col+1),(row-1, col+2),(row, col-1),(row, col+2),(row+1, col-1),(row+1, col),(row+1, col+1),(row+1, col+2)]
                self.addShipH (state, new_board, row, col, lista, waterlist)
                new_board.shipTwoLeft -=1
            elif lenght == 1:
                lista = [(row, col)]
                waterlist =[(row-1, col-1), (row-1, col),(row-1, col+1),(row, col-1),(row, col+1),(row+1, col-1),(row+1, col),(row+1, col+1)]
                self.addShipH (state, new_board, row, col, lista, waterlist)
                new_board.shipOneLeft -=1
        else:
            if lenght == 4:
                lista = [(row, col), (row+1, col), (row+2, col), (row+3, col)]
                waterlist =[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1, col-1),(row+1,col+1),(row+2,col-1),(row+2,col+1),(row+3,col-1),(row+3,col+1),(row+4,col-1),(row+4,col),(row+4,col+1)]
                self.addShipV (state, new_board, row, col, lista, waterlist)
                new_board.shipFourLeft -=1
            elif lenght == 3:
                lista = [(row, col), (row+1, col), (row+2, col)]
                waterlist =[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1, col-1),(row+1,col+1),(row+2,col-1),(row+2,col+1),(row+3,col-1),(row+3,col),(row+3,col+1)]
                self.addShipV (state, new_board, row, col, lista, waterlist)
                new_board.shipThreeLeft -=1
            elif lenght == 2:
                lista = [(row, col), (row+1, col)]
                waterlist =[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1, col-1),(row+1,col+1),(row+2,col-1),(row+2,col),(row+2,col+1)]
                self.addShipV (state, new_board, row, col, lista, waterlist)
                new_board.shipTwoLeft -=1
            elif lenght == 1:
                lista = [(row, col)]
                waterlist =[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1, col-1),(row+1,col),(row+1,col+1)]
                self.addShipV (state, new_board, row, col, lista, waterlist)
                new_board.shipOneLeft -=1
    

        new_board.LastPlayed = (row, col, lenght, position)
        new_state = BimaruState(new_board)
        
        return new_state



    # Adicionar barco para os Horizontal
    def addShipH (self, state, new_board, row, col, lista, waterlist ):
        # Dar update dos rowSum e colSum e retirar hints que estejam no meio
        counter =0
        colunas=[]
        for pos in lista:
            if state.board.get_value(pos[0], pos[1]) == " ":
                counter+=1
                colunas.append(pos[1])
                new_board.colSum[pos[1]] +=1
                new_board.set_value(pos[0], pos[1], 'X')
                new_board.blankPositions.remove((pos[0], pos[1]))
            else:
                new_board.hintListEdit.remove ((pos[0], pos[1], state.board.get_value(pos[0], pos[1])))
                new_board.set_value(pos[0], pos[1], 'X')
        new_board.rowSum[row] += counter
        #Meter água á volta do barco
        for water in waterlist:
            if new_board.is_valid_position(water[0], water[1]) and new_board.get_value(water[0], water[1]) == " ":
                new_board.blankPositions.remove((water[0], water[1]))
                new_board.set_value(water[0], water[1], '.')
        #Verificar as colunas e linhas
        new_board.fillRowWithWater(row)
        for i in colunas:
            new_board.fillColWithWater(i)

    #Adicionar Barco para os Vertical
    def addShipV (self, state, new_board, row, col, lista, waterlist ):
        # Dar update dos rowSum e colSum e retirar hints que estejam no meio
        counter =0
        linhas=[]
        for pos in lista:
            if state.board.get_value(pos[0], pos[1]) == " ":
                counter+=1
                linhas.append(pos[0])
                new_board.rowSum[pos[0]] +=1
                new_board.set_value(pos[0], pos[1], 'X')
                new_board.blankPositions.remove((pos[0], pos[1]))
            else:
                new_board.hintListEdit.remove ((pos[0], pos[1], state.board.get_value(pos[0], pos[1])))
                new_board.set_value(pos[0], pos[1], 'X')
        new_board.colSum[col] += counter
        #Meter água á volta do barco
        for water in waterlist:
            if new_board.is_valid_position(water[0], water[1]) and new_board.get_value(water[0], water[1]) == " ":
                new_board.blankPositions.remove((water[0], water[1]))
                new_board.set_value(water[0], water[1], '.')
        #Verificar as colunas
        new_board.fillColWithWater(col)
        for i in linhas:
            new_board.fillRowWithWater(i)
            


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        return state.board.blankPositions == [] and state.board.rowSum == state.board.rowMax and state.board.colSum == state.board.colMax

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""

        print("------------------------------------")
        print(node.state.board)
        print(node.state.board.rowSum)
        print(node.state.board.rowMax)
        print("------------------")
        print(node.state.board.colSum)
        print(node.state.board.colMax)
        
        print("------------------------------------")


        heuristic = 1000
        lastMove = node.action
        if lastMove == None:
            lastMove =(-1, -1, -1, -1)
        lastMoveRow = lastMove[0]
        lastMoveCol = lastMove[1]
        lastMoveLenght =lastMove[2]
        lastMovePosition = lastMove[3]

        #verifica se as colunas e linhas onde tá o barco estragaram
        if self.checkRowColLimits (node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition):
            print('checkRowColLimits')
            return float('inf')
        #Verifica se o número de barcos está ok
        if self.checkNumberOfBoats (node):
            print('checkNumberOfBoats')
            return float('inf')
        #Vê se existe alguma colisão
        if self.checkBoatColision (node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition):
            print('checkBoatColision')
            return float('inf')
        #Vê se as hints ainda estão no local certo
        if self.checkHintsInPlace (node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition):
            print('checkHintsInPlace')
            return float('inf')
        
        heuristic -= self.calculateHeuristic(node)

        print(heuristic)
        return heuristic


    
    def aux_checkRowColLimits (self, node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition,lista ):
        if lastMovePosition == "H":
            #Se for horizontal vai ver todas as colunas que o barco ocupou
            for col in lista:
                if node.state.board.checkColLimit(col):
                    return True
            #Verifica a linha que o barco ficou
            if node.state.board.checkRowLimit(lastMoveRow):
                return True
            return False
        else:
            #Se for vertical vai ver todas as linhas que o barco ocupou
            
            for row in lista:
                if node.state.board.checkRowLimit(row):
                    return True
            #Verifica a coluna que o barco ficou
            if node.state.board.checkColLimit(lastMoveCol):
                return True
            return False

    #Função que tem os sitios que o barco ocupou para depois chamar a função auxiliar e avaliar se ultrapassou o limite

    #devolve TRUE se tiver FORA DOS LIMITS
    def checkRowColLimits (self, node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition ):
        if lastMovePosition == 'H':
            if lastMoveLenght == 4:
                lista =[lastMoveCol,lastMoveCol+1,lastMoveCol+2,lastMoveCol+3]
                if self.aux_checkRowColLimits(node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition, lista ):
                    return True
                return False
            elif lastMoveLenght == 3:
                lista =[lastMoveCol,lastMoveCol+1,lastMoveCol+2]
                if self.aux_checkRowColLimits(node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition, lista ):
                    return True
                return False
            elif lastMoveLenght == 2:
                lista =[lastMoveCol,lastMoveCol+1]
                if self.aux_checkRowColLimits(node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition, lista ):
                    return True
                return False
            elif lastMoveLenght == 1:
                if node.state.board.checkRowLimit(lastMoveRow):
                    return True
                if node.state.board.checkColLimit(lastMoveCol):
                    return True
            return False
        else:
            if lastMovePosition == 'V':
                if lastMoveLenght == 4:
                    lista =[lastMoveRow,lastMoveRow+1,lastMoveRow+2,lastMoveRow+3]
                    if self.aux_checkRowColLimits(node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition, lista ):
                        return True
                    return False
                elif lastMoveLenght == 3:
                    lista =[lastMoveRow,lastMoveRow+1,lastMoveRow+2]
                    if self.aux_checkRowColLimits(node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition, lista ):
                        return True
                    return False
                elif lastMoveLenght == 2:
                    lista =[lastMoveRow,lastMoveRow+1]
                    if self.aux_checkRowColLimits(node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition, lista ):
                        return True
                    return False
                elif lastMoveLenght == 1:
                    if node.state.board.checkRowLimit(lastMoveRow):
                        return True
                    if node.state.board.checkColLimit(lastMoveCol):
                        return True
                return False

     #Verifica se o numero de barcos está dentro dos limites       
    def checkNumberOfBoats (self, node):
        if 0<=node.state.board.shipOneLeft<=4 and 0<=node.state.board.shipTwoLeft<=3 and 0<=node.state.board.shipThreeLeft<=2 and 0<=node.state.board.shipFourLeft<=1:
            return False
        else:
            return True
        
    #Verifica se há colisões entre barcos
    def checkBoatColision (self, node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition):
        if node.state.board.checkBoatColision_aux (lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition):
            return True
        else:
            return False
        
    #ve se alguma das coordenadas onde o barco ficou era hint
    def checkHintsInPlace_aux (self, node, lista, position):
        for pos in lista:
            for hint in node.state.board.hintListEdit:
                if (pos[0] == hint[0] and pos[1] == hint[1]):
                    if self.checkIfHintisTheSame (node, pos[0], pos[1], hint[2], position) == False:
                        return True
        return False
    
    #ve se a hint que tava la antes continua a ser o mesmo tipo de hint
    def checkIfHintisTheSame (self, node, row, col, hinttype, position):
        
        aguas =["W", "."]
        if hinttype == "L":
            lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row+1,col-1),(row+1,col),(row+1,col+1)]
            for item in lista:
                if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                    return False
            if node.state.board.get_value (row, col +1) != "X":
                return False
            return True

        elif hinttype == "R":
            lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
            for item in lista:
                if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                    return False
            if node.state.board.get_value (row, col -1) != "X":
                return False
            return True
            

        elif hinttype == "T":
            lista=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col+1)]
            for item in lista:
                if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                    return False
            if node.state.board.get_value (row+1, col) != "X":
                return False
            return True
            
    
        elif hinttype == "B":
            lista=[(row-1,col-1),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1, col),(row+1,col+1)]
            for item in lista:
                if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                    return False
            if node.state.board.get_value (row-1, col) != "X":
                return False
            return True
            

        elif hinttype == "C":
            lista=[(row-1,col-1),(row-1, col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1, col),(row+1,col+1)]
            for item in lista:
                if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                    return False
            return True
            

        elif hinttype == "M":
            if position == "H":
                lista=[(row-1,col-1),(row-1, col),(row-1,col+1),(row+1,col-1),(row+1, col),(row+1,col+1)]
                for item in lista:
                    if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                        return False
                if node.state.board.get_value (row, col-1) != "X" or node.state.board.get_value (row, col+1) != "X":
                    return False
                return True
            else:
                lista=[(row-1,col-1),(row-1, col+1),(row,col-1),(row,col+1),(row+1, col-1),(row+1,col+1)]
                for item in lista:
                    if node.state.board.is_valid_position (item[0], item[1]) and node.state.board.get_value (item[0], item[1]) not in aguas:
                        return False
                if node.state.board.get_value (row-1, col) != "X" or node.state.board.get_value (row+1, col) != "X":
                    return False
                return True
        
    #Hint é do tipo (row, col, tipo de barco)
    def checkHintsInPlace (self, node, lastMoveRow, lastMoveCol, lastMoveLenght, lastMovePosition):
        if lastMovePosition == "H":
            if lastMoveLenght == 4:
                lista=[(lastMoveRow, lastMoveCol),(lastMoveRow, lastMoveCol+1),(lastMoveRow, lastMoveCol+2),(lastMoveRow, lastMoveCol+3)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
            elif lastMoveLenght == 3:
                lista=[(lastMoveRow, lastMoveCol),(lastMoveRow, lastMoveCol+1),(lastMoveRow, lastMoveCol+2)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
            elif lastMoveLenght == 2:
                lista=[(lastMoveRow, lastMoveCol),(lastMoveRow, lastMoveCol+1)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
            elif lastMoveLenght == 1:
                lista=[(lastMoveRow, lastMoveCol)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
        else:
            if lastMoveLenght == 4:
                lista=[(lastMoveRow, lastMoveCol),(lastMoveRow+1, lastMoveCol),(lastMoveRow+2, lastMoveCol),(lastMoveRow+3, lastMoveCol)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
            elif lastMoveLenght == 3:
                lista=[(lastMoveRow, lastMoveCol),(lastMoveRow+1, lastMoveCol),(lastMoveRow+2, lastMoveCol)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
            elif lastMoveLenght == 2:
                lista=[(lastMoveRow, lastMoveCol),(lastMoveRow+1, lastMoveCol)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False
            elif lastMoveLenght == 1:
                lista=[(lastMoveRow, lastMoveCol)]
                if self.checkHintsInPlace_aux (node, lista,lastMovePosition):
                    return True
                return False


    def calculateHeuristic (self, node):
        barcos4 =  1- node.state.board.shipFourLeft
        barcos3 =  2- node.state.board.shipThreeLeft
        barcos2 =  3- node.state.board.shipTwoLeft
        barcos1 =  4- node.state.board.shipOneLeft

        return (barcos4*4) +(barcos3*3) + (barcos2*2) + (barcos1*1)

        
    
            


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    start_time = time.time()

    board = Board.parse_instance()

    
    BimaruStart = Bimaru(board)
    
    answer = greedy_search(BimaruStart)

    print(answer.state.board)

    end_time = time.time()
    tempo = end_time- start_time
    print (tempo)
