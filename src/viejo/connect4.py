from __future__ import print_function
import random



class Connect4:
    def __init__(self, player1, player2,width=4,height=5):
        self.board = [ [ -1 for _ in
        range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.player1, self.player2 = player1, player2
        self.red = 0
        self.blue = 1
        self.occupancy = [0]*width

    def play_game(self):
        #Selecciono color  de jugadores 0 = rojo, 1 = azul
        player_1_color = random.choice([self.red,self.blue])
        self.player1.start_game(player_1_color)
        self.player2.start_game(1-player_1_color)
        player_1_turn = random.choice([True,False])
        while True: #yolo
            if player_1_turn:
                player, color, other_player = self.player1, player_1_color, self.player2
            else:
                player, color, other_player = self.player2, 1-player_1_color , self.player1
            if player.breed == "human":
                self.display_board()
            new_pos = player.move(self.possible_moves())
            self.move(new_pos)
            self.board[new_pos[0]][new_pos[1]] = color
            if self.player_wins(color,new_pos):
                player.reward(1, self.board)
                other_player.reward(-1, self.board)
                break
            if self.board_full(): # tie game
                player.reward(0.5, self.board)
                other_player.reward(0.5, self.board)
                break
            other_player.reward(0, self.board)
            player_1_turn = not player_1_turn

    def player_wins(self, color,new_pos):
        #Arma fila vertical
        print('new_pos=',new_pos)
        if new_pos[0] >= 3 and all([ self.board[new_pos[0]-i][new_pos[1]]==color for i in range(0,4) ]):
            print('Player Wins vertical Line!!!')
            return True 
        #Arma linea horizontal
        init=max(0,new_pos[1]-3)
        end=min(self.height-4,new_pos[1])
        for i in range(init,end+1):
            if all([item==color for item in self.board[new_pos[0]][i:i+4]]):
                print('Player Wins Horizontal Line!!!')
                return True
        #Arma diagonal pendiente positiva
        dr = new_pos[0] - max(0,new_pos[0]-3)
        dc = new_pos[1] - max(0,new_pos[1]-3)
        delta = min(dr,dc)
        init=(new_pos[0]-delta,new_pos[1]-delta)
        while init[0]+3 <= self.height-1 and init[1]+3 <= self.width-1 and (init[0] <= new_pos[0] and init[1] <= new_pos[1]): 
            if all([self.board[init[0]+i][init[1]+i]==color for i in range(0,4) ]):
                print('Player Wins Positive Diagonal Line!!!')
                return True
            print(init[0])
            print(init[1])
            init= (init[0] + 1,init[1] + 1)
        #Arma diagonal pendiente negativa
        dr = min(self.height-1,new_pos[0]+3)-new_pos[0]
        dc = new_pos[1] - max(0,new_pos[1]-3)
        delta = min(dr,dc)
        init=(new_pos[0]+delta,new_pos[1]-delta)
        while init[0]-3 >= 0  and init[1]+3 <= self.width-1 and (init[0] >= new_pos[0] and init[1] <= new_pos[1]): 
            if all([self.board[init[0]-i][init[1]+i]==color for i in range(0,4) ]):
                print('Player Wins Negative Diagonal Line!!!')
                return True
            init= (init[0] - 1,init[1] + 1)

        return False

    def board_full(self):
        return not any([item!=-1 for sublist in self.board for item in sublist])

    def display_board(self):
        #print(self.board)
        for row in range(0,self.height):
            print('|',end='')
            for col in range(0,self.width):
                if self.board[self.height-1-row][col] != -1:
                    print(self.board[self.height-1-row][col],'|',end='')
                else:
                    print('  |',end='')
            print('')
    def possible_moves(self):
        return [(self.occupancy[c],c) for c in range(0,self.width) if self.occupancy[c] < self.height ]
    def move(self,new_pos):
        self.occupancy[new_pos[1]] += 1

#TODO todo para abajo

class Player(object):
    def __init__(self):
        self.breed = "human"

    def start_game(self, char):
        print("\nNew game!")

    def move(self,possible_moves):
        print('Move inside Human')
        my_move = -1;
        while my_move < 0 or my_move > len(possible_moves)-1    :
            print('Select item from move list: ',possible_moves)
            print('Enter value from 0 to ',len(possible_moves)-1,' :',end='')
            my_move = int(raw_input("Your move? "))
        return possible_moves[my_move]

    def reward(self, value, board):
        print('Got Reward', value)


class RandomPlayer(Player):
    def __init__(self):
        self.breed = "random"

    def reward(self, value, board):
        pass

    def start_game(self, char):
        pass

    def move(self, possible_moves):
        print('possible_moves:',possible_moves)
        return random.choice(possible_moves)


# class MinimaxPlayer(Player):
#     def __init__(self):
#         self.breed = "minimax"
#         self.best_moves = {}

#     def start_game(self, char):
#         self.me = char
#         self.enemy = self.other(char)

#     def other(self, char):
#         return 'O' if char == 'X' else 'X'

#     def move(self, board):
#         if tuple(board) in self.best_moves:
#             return random.choice(self.best_moves[tuple(board)])
#         if len(self.available_moves(board)) == 9:
#             return random.choice([1,3,7,9])
#         best_yet = -2
#         choices = []
#         for move in self.available_moves(board):
#             board[move-1] = self.me
#             optimal = self.minimax(board, self.enemy, -2, 2)
#             board[move-1] = ' '
#             if optimal > best_yet:
#                 choices = [move]
#                 best_yet = optimal
#             elif optimal == best_yet:
#                 choices.append(move)
#         self.best_moves[tuple(board)] = choices
#         return random.choice(choices)

#     def minimax(self, board, char, alpha, beta):
#         if self.player_wins(self.me, board):
#             return 1
#         if self.player_wins(self.enemy, board):
#             return -1
#         if self.board_full(board):
#             return 0
#         for move in self.available_moves(board):
#             board[move-1] = char
#             val = self.minimax(board, self.other(char), alpha, beta)
#             board[move-1] = ' '
#             if char == self.me:
#                 if val > alpha:
#                     alpha = val
#                 if alpha >= beta:
#                     return beta
#             else:
#                 if val < beta:
#                     beta = val
#                 if beta <= alpha:
#                     return alpha
#         if char == self.me:
#             return alpha
#         else:
#             return beta

#     def player_wins(self, char, board):
#         for a,b,c in [(0,1,2), (3,4,5), (6,7,8),
#                       (0,3,6), (1,4,7), (2,5,8),
#                       (0,4,8), (2,4,6)]:
#             if char == board[a] == board[b] == board[c]:
#                 return True
#         return False

#     def board_full(self, board):
#         return not any([space == ' ' for space in board])

#     def reward(self, value, board):
#         pass


# class MinimuddledPlayer(MinimaxPlayer):
#     def __init__(self, confusion=0.1):
#         super(MinimuddledPlayer, self).__init__()
#         self.breed = "muddled"
#         self.confusion = confusion
#         self.ideal_player = MinimaxPlayer()

#     def start_game(self, char):
#         self.ideal_player.me = char
#         self.ideal_player.enemy = self.other(char)

#     def move(self, board):
#         if random.random() > self.confusion:
#             return self.ideal_player.move(board)
#         else:
#             return random.choice(self.available_moves(board))


# class QLearningPlayer(Player):
#     def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.9):
#         self.breed = "Qlearner"
#         self.harm_humans = False
#         self.q = {} # (state, action) keys: Q values
#         self.epsilon = epsilon # e-greedy chance of random exploration
#         self.alpha = alpha # learning rate
#         self.gamma = gamma # discount factor for future rewards

#     def start_game(self, char):
#         self.last_board = (' ',)*9
#         self.last_move = None

#     def getQ(self, state, action):
#         # encourage exploration; "optimistic" 1.0 initial values
#         if self.q.get((state, action)) is None:
#             self.q[(state, action)] = 1.0
#         return self.q.get((state, action))

#     def move(self, board):
#         self.last_board = tuple(board)
#         actions = self.available_moves(board)

#         if random.random() < self.epsilon: # explore!
#             self.last_move = random.choice(actions)
#             return self.last_move

#         qs = [self.getQ(self.last_board, a) for a in actions]
#         maxQ = max(qs)

#         if qs.count(maxQ) > 1:
#             # more than 1 best option; choose among them randomly
#             best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
#             i = random.choice(best_options)
#         else:
#             i = qs.index(maxQ)

#         self.last_move = actions[i]
#         return actions[i]

#     def reward(self, value, board):
#         if self.last_move:
#             self.learn(self.last_board, self.last_move, value, tuple(board))

#     def learn(self, state, action, reward, result_state):
#         prev = self.getQ(state, action)
#         maxqnew = max([self.getQ(result_state, a) for a in self.available_moves(state)])
#         self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)


# p1 = RandomPlayer()
# p1 = MinimaxPlayer()
# p1 = MinimuddledPlayer()
p1 = Player()
p2 = RandomPlayer()

for i in xrange(0,200000):
    t = Connect4(p1, p2)
    t.play_game()

# p1 = Player()
# p2.epsilon = 0

# while True:
#     t = Connect4(p1, p2)
# t.play_game()
