from problem import Problem
from search_algorithm import best_first

def gb_agent(state_space, start, goal):
    '''AI agent that creates problem object and runs search algorithm'''
    def cost_function(node):
        '''Calculate distance to goal and add to distance traveled so far'''
        heuristic = ((abs(node.state[0] - goal[0])**2) +
                     (abs(node.state[1] - goal[1])**2))**0.5
        return node.path_cost + heuristic

    problem = Problem(state_space, start, goal)
    return best_first(problem, cost_function)