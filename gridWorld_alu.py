import numpy as np
import random
from collections import defaultdict
import pylab


class SubClassResponsability(Exception):
    pass

""" Clase que implementa un gridWorld"""
class gridWorld():
	def __init__(self,width=3, height=2,goals=None,positive=100,select_action='random',alpha=0.9,gamma=0.9,strategy=None):
                if strategy is None:
                    raise Exception("You need to specify an Strategy to chose next move")

		"""Seteo los parametros"""
		self.height=height
		self.width=width
		self.positive=positive
		self.select_action=select_action
		self.alpha=alpha
		self.gamma=gamma
		self.learning_step=0
                self.strategy = strategy
		
		"""Represento Q como una lista de filas de celdas de Q
		Es decir, en self.Q[0][1] esta la celda que corresponde al estado
		[0,1]. La celdas son diccionarios de acciones posibles y sus 
		valores. 
		
		Por ejemplo, self.Q[0][0] podria ser: {'right':0.8, 'down':0.3'}
		o si el estado [0,2] es terminal, self.Q[0][2]: {'stay':100}
		
		Esta definido con un defaultdict para facilidad, podria 
		inicialiazarse explicitamente
		"""
		
		self.Q = [ [ defaultdict(lambda :random.random()) for _ in 
		range(self.width)] for _ in range(self.height)]
		
		if goals==None:	self.goals=[[0,self.width-1]]
		else: self.goals=list(goals)
		
			
		
	""" Devuelve las posibles acciones a hacer teniendo en cuenta los
	bordes y los terminales """
	def possibleActions(self,state):
		row,col = state 
		res=[]
		if row>0: res.append('up')
		if row<self.height-1: res.append('down')
                if col > 0: res.append('left')
                if col < self.width -1: res.append('right')
                return res
		
		
	""" Dado un estado y una accion devuelve un estado nuevo despues de
	hacer hecho la accion"""
	def move(self,state,action):
		new_state= list(state)
		if action=='up': new_state[0]-=1
		if action=='down': new_state[0]+=1
                if action=='left': new_state[1]-=1
                if action=='right': new_state[1]+=1
                return new_state
		
		
		
	""" Me dice si state es terminal"""	
	def isTerminal(self,state):
		return state in self.goals
		
		
	""" Funcion recompenza, tengo una reward positiva si desde state
	usando action llego a un estado terminal """	
	def reward(self,state, action):
		if self.isTerminal(self.move(state,action)): 
			return self.positive
		return 0
		
	
	""" Funcion que aprende, implementa Qlearning (diapos teorica)"""
	def learn(self,state):
		self.learning_step+=1
		
		# Repito hasta que state sea terminal
		while not self.isTerminal(state) :
		        print state	
			# 1) Listo las posibles acciones que puedo hacer teniendo
			# encuenta el estado de donde estoy
                        actions = self.possibleActions(state)
		
			# 2) Elijo la MEJOR accion dentro de las posibles

                        action,reward = self.strategy.next_move(self,actions,state)
		        new_state = self.move(state,action)
			# 3) Calculo el nuevo valor de Q(s,a)
                        new_state_Qs = list(self.Q[new_state[0]][new_state[1]].values())
                        if len(new_state_Qs) > 0:
                            new_state_max_Q = max(new_state_Qs)
                        else: new_state_max_Q = 0
                        self.Q[state[0]][state[1]][action] = self.Q[state[0]][state[1]][action] + self.alpha * ( reward + self.gamma * new_state_max_Q   - self.Q[state[0]][state[1]][action])
			
	
			# 4) Actualizo s
			state = new_state
	
		
	
	""" Funcion para plotear la Q"""
	def draw(self):
		def ifExceptReturnNan(dic,k):
			try: return dict(dic)[k]
			except: return np.nan


		matrix_right= np.array([[ ifExceptReturnNan(cel,'right') for cel in row] for row in self.Q])
		matrix_left= np.array([[ ifExceptReturnNan(cel,'left') for cel in row] for row in self.Q])
		matrix_up= np.array([[ ifExceptReturnNan(cel,'up') for cel in row] for row in self.Q])
		matrix_down= np.array([[ ifExceptReturnNan(cel,'down') for cel in row] for row in self.Q])
		matrix_stay= np.array([[ ifExceptReturnNan(cel,'stay') for cel in row] for row in self.Q])

		fig = pylab.figure(figsize=2*np.array([self.width,self.height]))
		for i in range(matrix_right.shape[0]):
			for j in range(matrix_right.shape[1]):
				if not np.isnan(matrix_stay[i][j]): pylab.text(j-.5, self.height- i-.5,'X')
				else:
					pylab.text(j+0.2-.5, self.height-  i-.5,str(matrix_right[i][j])[0:4]+">")
					pylab.text(j-0.3-.5, self.height-i-.5,"<"+str(matrix_left[i][j])[0:4])

					pylab.text(j-.5, self.height- i+.1-.5,str(matrix_up[i][j])[0:4])
					pylab.text(j-.5, self.height- i-.1-.5,str(matrix_down[i][j])[0:4])
                                if self.isTerminal((j,i)):
                                    pylab.text(j,self.height-i-.5,i,"Goal")

		pylab.xlim(-1,self.width-1)
		pylab.ylim(0,self.height)
		pylab.xticks(range(self.width),map(str,range(self.width)))
		pylab.yticks(range(self.height+1),list(reversed(map(str,range(self.height+1)))))
		pylab.grid(color='r', linestyle='-', linewidth=2)
		pylab.title('Q (learning_step:%d)' % self.learning_step,size=16)
		fig.tight_layout()		


class Strategy():
    def next_move(self,possible_actions,state):
        raise SubClassResponsability()

class RandomStrategy(Strategy):
    def next_move(self,grid_world,possible_actions,state):
        selected_action = possible_actions[random.randrange(0,len(possible_actions),1)]
        reward = grid_world.reward(state,selected_action)
        return (selected_action,reward)


class GreedyStrategy(Strategy):
    def __init__(self,epsilon=0.1):
        self.epsilon = epsilon
        print self.epsilon
    def next_move(self,grid_world,possible_actions,state):
        reward = None
        if random.random() < self.epsilon:
            print "Selecting at random"
            selected_action  = possible_actions[random.randrange(0,len(possible_actions),1)]
            print selected_action
            reward = grid_world.reward(state,selected_action)
        else:
            for action in possible_actions:
                current_reward = grid_world.reward(state,action)
                if reward is None or current_reward > reward:
                     selected_action = action
                     reward = current_reward                         

        return (selected_action,reward)



if __name__ == "__main__":
	
	# Ejemplo de 4x4 con goal en el medio
	# gw =gridWorld(height=4,width=4,goals=[[2,2]])
	
	
	# Ejemplo de gridWorld  de 2x3 
	gw =gridWorld(height=4,width=4,goals=[[2,2]],strategy=GreedyStrategy(0.4))
	#gw =gridWorld(height=4,width=4,goals=[[2,2]],strategy=RandomStrategy())

	# Entreno 1K veces
	for epoch in range(1000):
                print "Iteracion =",epoch
		# Ploteo la matrix a los 10,200, y 999 epochs
		if epoch==10: gw.draw()
		if epoch==200: gw.draw()
		if epoch==999: gw.draw()

		# Elijo un state random para empezar
		start_state = [ random.randint(0,gw.height-1),random.randint(0,gw.width-1)]
		
		# Entreno
		gw.learn(start_state)
		
		if epoch%1000==0: print  epoch
	pylab.show()

