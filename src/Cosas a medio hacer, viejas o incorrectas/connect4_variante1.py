from __future__ import print_function
import random
import matplotlib.pyplot as plt
import numpy as np
import copy


def available_moves(board):
    res = []
    for j in range(len(board[0])):
        for i in range(len(board)):
            if board[i][j] == ' ':
                res.append((i,j))
                break
    return res

def tuple_from_board(board):
    return tuple([val for row in board for val in row])

class Connect4:
    def __init__(self, playerX, playerO,height,width):
        self.board = [ [ ' ' for _ in range(width)] for _ in range(height)]
        self.playerX, self.playerO = playerX, playerO
        self.width = width
        self.height = height
        self.occupancy = [0]*width
        self.win_len = 4

    def play_game(self):
        self.playerX.start_game('X')
        self.playerO.start_game('O')
        self.playerX_turn = random.choice([True, False])
        if self.playerX_turn:
            self.playerX.started += 1
        else:
            self.playerO.started += 1

        while True: #yolo
            if self.playerX_turn:
                player, color, other_player, other_color = self.playerX, 'X', self.playerO, 'O'
            else:
                player, color, other_player, other_color = self.playerO, 'O', self.playerX, 'X'
            if player.breed == "human":
                self.display_board()
            new_pos = player.move(self.board,self.possible_moves())

            if self.board[new_pos[0]][new_pos[1]] != ' ':
                player.reward(-99, self.board) # score of shame
                break
            
            self.move(new_pos)
            self.board[new_pos[0]][new_pos[1]] = color


            # BLOQUEO

            if self.player_wins(other_color,player.last_move):
                player.reward(0.5, self.board, True)

            # GANO

            if self.player_wins(color,player.last_move):
                player.reward(1, self.board, True)
                other_player.reward(-1, self.board, False)
                player.score(1)
                #self.display_board()
                break

            # TABLERO LLENO

            if self.board_full(): # tie game
                player.reward(0.5, self.board, True)
                other_player.reward(0.5, self.board, False)
                #player.score(0.5)
                #other_player.score(0.5)
                break            

            other_player.reward(0, self.board, False)
            self.playerX_turn = not self.playerX_turn

    def player_wins(self, color, new_pos):
        #Arma fila vertical
        #print('new_pos=',new_pos)
        if new_pos[0] >= 3 and all([ self.board[new_pos[0]-i][new_pos[1]]==color for i in range(0,4) ]):
            #print('Player Wins vertical Line!!!')
            return True 
        #Arma linea horizontal
        init=max(0,new_pos[1]-3)
        end=min(self.width-4,new_pos[1])
        for i in range(init,end+1):
            #print([item for item in self.board[new_pos[0]][i:i+4]])
            if all([item==color for item in self.board[new_pos[0]][i:i+4]]):
                #print('Player Wins Horizontal Line!!!')
                return True
        #Arma diagonal pendiente positiva
        dr = new_pos[0] - max(0,new_pos[0]-3)
        dc = new_pos[1] - max(0,new_pos[1]-3)
        delta = min(dr,dc)
        init=(new_pos[0]-delta,new_pos[1]-delta)
        while init[0]+3 <= self.height-1 and init[1]+3 <= self.width-1 and (init[0] <= new_pos[0] and init[1] <= new_pos[1]): 
            if all([self.board[init[0]+i][init[1]+i]==color for i in range(0,4) ]):
                #print('Player Wins Positive Diagonal Line!!!')
                return True
            init= (init[0] + 1,init[1] + 1)
        #Arma diagonal pendiente negativa
        dr = min(self.height-1,new_pos[0]+3)-new_pos[0]
        dc = new_pos[1] - max(0,new_pos[1]-3)
        delta = min(dr,dc)
        init=(new_pos[0]+delta,new_pos[1]-delta)
        while init[0]-3 >= 0  and init[1]+3 <= self.width-1 and (init[0] >= new_pos[0] and init[1] <= new_pos[1]): 
            if all([self.board[init[0]-i][init[1]+i]==color for i in range(0,4) ]):
                #print('Player Wins Negative Diagonal Line!!!')
                return True
            init= (init[0] - 1,init[1] + 1)

        return False

    def board_full(self):
        return not any([val==' ' for row in self.board for val in row])

    def display_board(self):
        #print(self.board)
        print('')
        for row in range(0,self.height):
            print('|',end='')
            for col in range(0,self.width):
                print(self.board[self.height-1-row][col],'|',end='')
            print('')
        print('')

    def possible_moves(self):
        return [(self.occupancy[c],c) for c in range(0,self.width) if self.occupancy[c] < self.height ]

    def move(self,new_pos):
        self.occupancy[new_pos[1]] += 1


class Player(object):
    def __init__(self):
        self.breed = "human"
        self.total_score=0
        self.started=0

    def start_game(self, color):
        print("\nNew game!")

    def move(self, board,possible_moves):
        print('Your  turn!')
        my_move = -1;
        while my_move < 0 or my_move > len(possible_moves)-1    :
            print('Select item from move list: ',possible_moves)
            print('Enter value from 0 to ',len(possible_moves)-1,' :',end='')
            my_move = int(raw_input("Your move? "))
        self.last_move = possible_moves[my_move]
        self.last_board = tuple_from_board(board)
        return self.last_move

    def reward(self, value, board, jugueUltimo):
        print (self.breed,' rewarded: ',value)
    def score(self,points):
        self.total_score += points;

    # def available_moves(self, board):
    #     return [i+1 for i in range(0,9) if board[i] == ' ']


class RandomPlayer(Player):
    def __init__(self):
        self.breed = "random"
        self.total_score=0
        self.movements=0
        self.started=0
        self.last_board = None
        self.last_move = None


    def reward(self, value, board, jugueUltimo):
        pass

    def start_game(self, color):
        pass

    def move(self, board,possible_moves):
        self.movements+=1
        self.last_move = random.choice(possible_moves)
        self.last_board = tuple_from_board(board)
        return self.last_move

class QLearningPlayer(Player):
    def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.9):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = {} # (state, action) keys: Q values
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards
        self.total_score=0
        self.movements=0
        self.started=0


    def start_game(self, color):
        self.last_board = None
        self.last_move = None

    def getQ(self, state, action):
        # Initial values considered options:
        # 1. "optimistic" 1.0 initial values encourage exploration; 
        # 2. "pesimistic" 0.0 initial values encourage repeating known movements;
        # 3. random initial values;
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 0.0
        return self.q.get((state, action))

    def move(self, board,possible_moves):
        self.last_board = tuple_from_board(board)
        actions = possible_moves
        if random.random() < self.epsilon: # explore! 
            self.last_move = random.choice(actions)
            return self.last_move

        qs = [self.getQ(self.last_board, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.movements+=1
        self.last_move = actions[i]
        return actions[i]

    def reward(self, value, board, jugueUltimo):
        #print('board before: ',self.last_board)
        #print('board after: ',board)
        #print('possible moves: ',possible_moves)
        if jugueUltimo:
            if self.last_move:
                self.learnYo(self.last_board, self.last_move, value, tuple_from_board(board))
        else:
            if self.last_move:
                self.learnOponente(self.last_board, self.last_move, value, tuple_from_board(board))


    def learnOponente(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        possible_moves = available_moves(result_state)
        if len(possible_moves) > 0:
            maxqnew = max([self.getQ(result_state, a) for a in possible_moves ])
        else: maxqnew = 0
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)

    def learnYo(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        possible_moves = available_moves(state)
        if len(possible_moves) > 0:
            maxqnew = max([self.getQ(result_state, a) for a in possible_moves ])
        else: maxqnew = 0
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)



p1 = RandomPlayer()
#p1 = QLearningPlayer()
p2 = QLearningPlayer()
y1 = list()
y2 = list()
y3 = list()
y4 = list()

plotRange = 200000
for i in xrange(0,plotRange):
    t = Connect4(p1, p2,7,6)
    t.play_game()
    if i % 500 == 0:
        print('i=',i,' ,P1 ratio = ',p1.total_score / float(500),' started: ',p1.started,', P2 ratio = ',p2.total_score / float(500),'started: ',p2.started)
        y1.append(p1.total_score / float(500))
        y2.append(p2.total_score / float(500))
        y3.append(p1.movements / float(500))
        y4.append(p2.movements / float(500))
        p1.started = 0
        p2.started = 0
        p1.total_score = 0
        p2.total_score = 0
        p1.movements = 0
        p2.movements = 0


print("Creating plots..")

player1, = plt.plot(range(0,plotRange,500),y1,label='player1: '+ p1.breed)
player2, = plt.plot(range(0,plotRange,500),y2,label='player2: '+ p2.breed)
plt.ylabel(r'Tasa de Victorias')
plt.xlabel(r'Cantidad de Juegos')

plt.legend([player1, player2],['player1: ' + p1.breed  ,'player2: ' + p2.breed],loc='lower right')
plt.savefig('../informe/IMGs/connect4_victories' + '.pdf')
plt.close()


player1, = plt.plot(range(0,plotRange,500),y3,label='player1: '+ p1.breed)
player2, = plt.plot(range(0,plotRange,500),y4,label='player2: '+ p2.breed)
plt.ylabel(r'Tasa de Movimientos Realizados')
plt.xlabel(r'Cantidad de Juegos')

plt.legend([player1, player2],['player1: ' + p1.breed  ,'player2: ' + p2.breed],loc='lower right')
plt.savefig('../informe/IMGs/connect4_movements' + '.pdf')
plt.close()


p = Player()
p2.epsilon = 0

while True:
    t = Connect4(p, p2,7,6)
    t.play_game()
