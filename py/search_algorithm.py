class Node:
    '''Class to hold data about the current state and path leading to it'''
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

def expand(problem, node):
    '''Loop through actions determining each next state and cost of action'''
    s1 = node.state
    for action in problem.actions(s1):
        s2 = problem.result(action)
        cost = node.path_cost + problem.action_cost(s1, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=cost)

def best_first(problem, f):
    '''
    Build node and add to frontier(potential moves) and reached
    Then search frontier for goal, return goal node or failure(frontier empty)
    If a node is not the goal, expand child nodes from it
    Test if a child node is a new state or a shorter path to an previous state
    If so add child node to reached and frontier, then sort frontier
    '''
    node = Node(state=problem.initial)
    frontier = [node]
    reached = {node.state: node}
    while len(frontier) > 0:
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.append(child)
                frontier.sort(key=f, reverse=True)
    return 'failure'