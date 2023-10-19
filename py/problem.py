class Problem:
    '''Class that holds and calculates problem specific information'''
    def __init__(self, state_space, start, goal):
        self.states = state_space
        self.initial = start
        self.goal = goal

    def actions(self, state):
        '''Find current state in state space then return that states actions'''
        for sp_state in self.states:
            if (sp_state['state']['x'] == state[0] and
                sp_state['state']['y'] == state[1]):
                return sp_state['actions']
            
    def action_cost(self, state1, state2):
        '''Calculate and return distance between current node and next node'''
        return ((abs(state1[0] - state2[0])**2) +
                (abs(state1[1] - state2[1])**2))**0.5

    def is_goal(self, state):
        '''Return whether the current state and goal state match'''
        if (state[0] == self.goal[0] and state[1] == self.goal[1]):
            return True
        else: return False

    def result(self, action):
        '''Return next state(dest) after taking action in current state'''
        return (action['dest']['x'], action['dest']['y'])