from __future__ import print_function
import random
import matplotlib.pyplot as plt
import numpy as np
import copy

def display_board(board):
    #print(self.board)
    height=len(board)
    width=len(board[0])
    print('')
    for row in range(0,height):
        print('|',end='')
        for col in range(0,width):
            print(board[height-1-row][col],'|',end='')
        print('')
    print('')

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
    def __init__(self, playerX, playerO,height=6,width=7):
        self.board = [ [ ' ' for _ in range(width)] for _ in range(height)]
        self.playerX, self.playerO = playerX, playerO
        self.width = width
        self.height = height

    def play_game(self):
        self.playerX.start_game('X')
        self.playerO.start_game('O')
        self.playerX_turn = random.choice([True, False])

        while True: #yolo
            if self.playerX_turn:
                player, color, other_player, other_color = self.playerX, 'X', self.playerO, 'O'
            else:
                player, color, other_player, other_color = self.playerO, 'O', self.playerX, 'X'

            if player.breed == "human":
                self.display_board()

            new_pos = player.move(self.board)


            # JUGADA ILEGAL

            """if self.board[new_pos[0]][new_pos[1]] != ' ':
                player.reward(-99, self.board) # score of shame
                break"""
            
            # GUARDO MOVIDA

            self.board[new_pos[0]][new_pos[1]] = color

            # BLOQUEO

            """if self.player_wins(other_color,player.last_move,player.last_board):
                player.reward(0.5, self.board)"""

            # GANO

            if self.player_wins(color,player.last_move):
                player.reward(1, self.board)
                other_player.reward(-1, self.board)
                player.score(1)
                #self.display_board()
                break

            # TABLERO LLENO

            if self.board_full(): # tie game
                player.reward(0.5, self.board)
                other_player.reward(0.5, self.board)
                break            

            other_player.reward(0, self.board)
            self.playerX_turn = not self.playerX_turn


    def player_wins(self, color,new_pos):
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

class Player(object):
    def __init__(self):
        self.breed = "human"
        self.total_score=0
        self.started=0

    def start_game(self, color):
        print("\nNew game!")

    def move(self, board):
        print('Your  turn!')
        possible_moves = available_moves(board)
        my_move = -1;
        while my_move < 0 or my_move > len(possible_moves)-1    :
            print('Select item from move list: ',possible_moves)
            print('Enter value from 0 to ',len(possible_moves)-1,' :',end='')
            my_move = int(raw_input("Your move? "))
        self.last_move = possible_moves[my_move]
        self.last_board = tuple_from_board(board)
        return self.last_move

    def reward(self, value, board):
        print (self.breed,' rewarded: ',value)
    def score(self,points):
        self.total_score += points;

class RandomPlayer(Player):
    def __init__(self):
        self.breed = "random"
        self.total_score=0
        self.movements=0
        self.started=0
        self.last_board = (' ',)*9
        self.last_move = None

    def desc(self):
        return self.breed

    def reward(self, value, board):
        pass

    def start_game(self, color):
        pass

    def move(self, board):
        self.last_move = random.choice(available_moves(board))
        self.last_board = tuple_from_board(board)
        return self.last_move

class Connect4WithBlock(Connect4):
    def play_game(self):
        self.playerX.start_game('X')
        self.playerO.start_game('O')
        self.playerX_turn = random.choice([True, False])

        while True: #yolo
            if self.playerX_turn:
                player, color, other_player, other_color = self.playerX, 'X', self.playerO, 'O'
            else:
                player, color, other_player, other_color = self.playerO, 'O', self.playerX, 'X'

            if player.breed == "human":
                self.display_board()

            new_pos = player.move(self.board)

            # BLOQUEO

            self.board[new_pos[0]][new_pos[1]] = other_color
            if self.player_wins(other_color,player.last_move):
                self.board[new_pos[0]][new_pos[1]] = color
                player.reward(0.5, self.board)

            # GANO
            self.board[new_pos[0]][new_pos[1]] = color
            if self.player_wins(color,player.last_move):
                player.reward(1, self.board)
                other_player.reward(-1, self.board)
                player.score(1)
                #self.display_board()
                break

            # TABLERO LLENO

            if self.board_full(): # tie game
                player.reward(0.5, self.board)
                other_player.reward(0.5, self.board)
                break            

            other_player.reward(0, self.board)
            self.playerX_turn = not self.playerX_turn

class QLearningPlayer(Player):
    def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.9,q_init=1.0):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = {} # (state, action) keys: Q values
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards
        self.total_score=0
        self.q_init=q_init

        self.started=0

    def desc(self):
        desc= self.breed + ',epsilon=' + str(self.epsilon)
        return desc
    def start_game(self, color):
        self.last_board = None
        self.last_move = None

    def getQ(self, state, action):
        # Initial values considered options:
        # 1. "optimistic" 1.0 initial values encourage exploration; 
        # 2. "pesimistic" 0.0 initial values encourage repeating known movements;
        # 3. random initial values;
        if self.q.get((state, action)) is None:
            if self.q_init is None:
                self.q[(state, action)] = random.random() 
            else: self.q[(state, action)] = self.q_init
        return self.q.get((state, action))

    def move(self, board):
        self.last_board = tuple_from_board(board)
        actions = available_moves(board)

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

        self.last_move = actions[i]
        return actions[i]

    def reward(self, value, board):
        if self.last_move:
            possible_moves = available_moves(board)
            self.learn(self.last_board, self.last_move, value, tuple_from_board(board), possible_moves)

    def learn(self, state, action, reward, result_state, possible_moves):
        prev = self.getQ(state, action)
        if len(possible_moves) > 0:
            maxqnew = max([self.getQ(result_state, a) for a in possible_moves ])
        else: maxqnew = 0
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)

class SoftMaxPlayer(QLearningPlayer):
    def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.9,q_init=1.0,tempeture=1.0):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = {} # (state, action) keys: Q values
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards
        self.total_score=0
        self.q_init=q_init

    def move(self, board):
        self.last_board = tuple_from_board(board)
        actions = available_moves(board)

        zq = zip(actions,[ self.getQ(self.last_board, a)  for i in actions])
        eq = np.exp([(i[1]/self.tempeture) for i in zq] )
        p = eq / eq.sum() 
        selected_index = np.random.choice(range(0,len(p)),p=p)    
        selected_action = zq[selected_index][0]

        self.last_move = selected_action
        return selected_action



def train(game_factory,cantidad_de_juegos,p1,p2,file_name):
    y1 = list()
    y2 = list()

    plotRange= cantidad_de_juegos
    for i in xrange(0,plotRange):
        game = game_factory(p1,p2)
        game.play_game()
        if i % 500 == 0:
            print('i=',i,' ,P1 ratio = ',p1.total_score / float(500),', P2 ratio = ',p2.total_score / float(500))
            y1.append(p1.total_score / float(500))
            y2.append(p2.total_score / float(500))
            p1.total_score = 0
            p2.total_score = 0

    print("Creating plot..")

    player1, = plt.plot(range(0,plotRange,500),y1,label='player1: '+ p1.desc() )
    player2, = plt.plot(range(0,plotRange,500),y2,label='player2: '+ p2.desc() )
    plt.ylabel(r'Tasa de Victorias')
    plt.xlabel(r'Cantidad de Juegos')

    lgd = plt.legend([player1, player2],['player1: ' + p1.desc(),'player2: ' + p2.desc() ],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #plt.legend([player1, player2],['player1: ' + p1.desc(),'player2: ' + p2.desc() ],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,loc='lower right')
    plt.savefig('./Testeo/'+ file_name + '.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()

    csv_file = open('./csv_files/' + file_name + '.csv', "w")
    csv_file.write('#n,'+ p1.desc()+','+ p2.desc() + '\n')
    for i in xrange(0,plotRange/500):
        csv_file.write(str(i*500))
        csv_file.write(',')
        csv_file.write(str(y1[i]))
        csv_file.write(',')
        csv_file.write(str(y2[i]))
        csv_file.write('\n')
    csv_file.close()

if __name__ == '__main__':
    train_count=200000
    p1 = QLearningPlayer(q_init=0.0,epsilon=0.1)
    p2 = RandomPlayer()    
    
    # p1 = QLearningPlayer(q_init=0.0,epsilon=0.1)
    # p2 = RandomPlayer()
    # p3 = QLearningPlayer(q_init=0.0,epsilon=0.1)

    # train((lambda player1,player2: Connect4(player1,player2)),train_count,p1,p2,'QL_q_init_0_epsilon_10p_vs_Random_Normal')
    # train((lambda player1,player2: Connect4WithBlock(player1,player2)),train_count,p3,p2,'QL_q_init_0_epsilon_10p_vs_Random_WithBlock')

    # p1.epsilon = 0
    # p3.epsilon = 0
    # train((lambda player1,player2: Connect4(player1,player2)),train_count,p1,p3,'Normal_Trained_vs_WithBlockTrained_not_exploring')

    # p1 = QLearningPlayer(q_init=0.0,epsilon=0.1)
    # p2 = RandomPlayer()
    # p3 = QLearningPlayer(q_init=0.0,epsilon=0.1)

    # train((lambda player1,player2: Connect4(player1,player2)),train_count,p1,p2,'QL_q_init_0_epsilon_10p_vs_Random_Normal')
    # train((lambda player1,player2: Connect4WithBlock(player1,player2)),train_count,p3,p2,'QL_q_init_0_epsilon_10p_vs_Random_WithBlock')

    # train((lambda player1,player2: Connect4(player1,player2)),train_count,p1,p3,'Normal_Trained_vs_WithBlockTrained_exploring')
    # p1 = QLearningPlayer(q_init=0.0,epsilon=0.1)
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.2)

    # train(train_count,p1,p2,'Bot_epsilon_10p_vs_Bot_epsilon_20p')

    # p1 = QLearningPlayer(q_init=0.0,epsilon=0.1)
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.3)

    # train(train_count,p1,p2,'Bot_epsilon_10p_vs_Bot_epsilon_30p')

    # p1 = QLearningPlayer(q_init=0.0,epsilon=0.1)
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.4)

    # train(train_count,p1,p2,'Bot_epsilon_10p_vs_Bot_epsilon_40p')

    # p1 = RandomPlayer()
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.1)

    # train(train_count,p1,p2,'Random_vs_Bot_epsilon_10p')

    # p1 = RandomPlayer()
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.2)

    # train(train_count,p1,p2,'Random_vs_Bot_epsilon_20p')

    # p1 = RandomPlayer()
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.3)

    # train(train_count,p1,p2,'Random_vs_Bot_epsilon_30p')


    # p1 = RandomPlayer()
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.4)

    # train(train_count,p1,p2,'Random_vs_Bot_epsilon_40p')

    # p1 = RandomPlayer()
    # #p1 = QLearningPlayer()
    # p2 = QLearningPlayer(q_init=0.0,epsilon=0.5)

    # train(train_count,p1,p2,'Random_vs_Bot_epsilon_50p')

