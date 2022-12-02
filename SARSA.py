import numpy as np
import pandas as pd

ROWS = 4
COLS = 12
START_STATE = (3, 0)
TERMINAL_STATE = (3, 11)
NUM_EPISODES = 50
DISCOUNT_RATE = 0.5
MAX_ITER = 50

class Cliff:
    def __init__(self):
        self.board = np.ones([4,12])
        self.board = self.board*-1
        #create cliff with -1 
        self.board[3, 1:11] = -100
        self.board[TERMINAL_STATE[0]][TERMINAL_STATE[1]] = 100
        #print(self.board)

    '''def show(self):
        for i in range(0, ROWS):
            print('-------------------------------------------------')
            out = '| '
            token = ''
            for j in range(0, COLS):
                if self.board[i, j] == -100:
                    token = '*'
                if self.board[i, j] == -1:
                    token = ' '
                if (i, j) == self.pos:
                    token = 'S'
                if (i, j) == TERMINAL_STATE:
                    token = 'G'
                out += token + ' | '
            print(out)
        print('-------------------------------------------------')''' 


class Agent:
    def __init__(self):
        self.q = np.random.rand(ROWS, COLS, 4) #called like 1[row][col][direction]
        self.state = START_STATE
        self.done = False

    def resetState(self):
        self.state = START_STATE
        self.done = False

    def greedPolicy(self):
        action = 3
        v = -100
        if self.q[self.state[0]][self.state[1]][0] > v:
            v = self.q[self.state[0]][self.state[1]][0]
            action = 0
        if self.q[self.state[0]][self.state[1]][1] > v:
            v = self.q[self.state[0]][self.state[1]][1]
            action = 1
        if self.q[self.state[0]][self.state[1]][2] > v:
            v = self.q[self.state[0]][self.state[1]][2]
            action = 2
        if self.q[self.state[0]][self.state[1]][3] > v:
            self.q[self.state[0]][self.state[1]][3]
            action = 3
        return action

    #returns a new state after move
    def move(self, action, cliff):
        if action == 0:
            return(self.state[0]-1, self.state[1])
        elif action == 1:
            return(self.state[0], self.state[1]+1)
        elif action == 2:
            return(self.state[0]+1, self.state[1])
        else:
            return(self.state[0], self.state[1]-1)

    def updateQ(self, a_0, r ,s_1, a_1,  discount_rate=DISCOUNT_RATE):
       self.q[self.state[0]][self.state[1]][a_0] += r + (discount_rate * self.q[s_1[0]][s_1[1]][a_1] - self.q[self.state[0]][self.state[1]][a_0])

    def terminal(self, s, a):
        if(s == TERMINAL_STATE):
            print("Success")
            self.done = True
        elif(s_1[0]<0 or s_1[0] >= ROWS or s_1[1]<0 or s_1[1]>=COLS ):
            print("Failed")
            self.q[self.state[0]][self.state[1]][a] = -100
            self.done = True

i = 0
agent = Agent()
myCliff = Cliff()
while i < NUM_EPISODES:
    print(f"episode:{i}")
    agent.resetState()
    a_0 = agent.greedPolicy()
    iter = 0
    while agent.done == False & iter < MAX_ITER:
        print("inside")
        s_1 = agent.move(a_0, myCliff)
        agent.terminal(s_1, a_0) # because the first one didnt get rewarded it chooses a different direction but doesnt get to update q table because all other options are terminal
        if (agent.done == True): break
        print(s_1)
        print(a_0)
        r = myCliff.board[s_1[0]][s_1[1]]
        a_1 = agent.greedPolicy()
        agent.updateQ(a_0, r, s_1, a_1, iter)
        a_0 = a_1
        agent.state = s_1
        iter = iter + 1
    i = i + 1