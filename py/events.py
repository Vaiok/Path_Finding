from agent import gb_agent
from canvas_events import cnvs_clck_fn

def clr_grph_fn(data, cnvs):
    '''Resets the data, first for the canvas then the graph'''
    for item in data['edges']: cnvs.delete(item['line'])
    for item in data['nodes']: cnvs.delete(item['dot'])
    data['edges'].clear()
    data['nodes'].clear()
    data['edge_node'] = data['start'] = data['goal'] = None

def build_state_space(data, cnvs):
    '''
    If start or goal are not set ignore the click
    Otherwise set their states and build the state space for AI agent
    '''
    if not data['start'] or not data['goal']:
        print('Must select a start node and goal node')
        return None, None, None
    start = (data['start']['x'], data['start']['y'])
    goal = (data['goal']['x'], data['goal']['y'])
    state_space = []
    for node in data['nodes']:
        act = []
        for edge in data['edges']:
            # Reset all line colors
            cnvs.itemconfigure(edge['line'], fill='red')
            # Turn all edges into actions
            if node == edge['node1']:
                act.append({
                    'dest': {'x': edge['node2']['x'], 'y': edge['node2']['y']},
                    'id': edge['line']
                })
            elif node == edge['node2']:
                act.append({
                    'dest': {'x': edge['node1']['x'], 'y': edge['node1']['y']},
                    'id': edge['line']
                })
        # Turn all nodes into states
        state_space.append({
            'state': {'x': node['x'], 'y': node['y']}, 'actions': act
        })
    return state_space, start, goal

def fnd_pth_fn(data, cnvs):
    '''
    Build state space, run AI agent, and test if agent search is successful
    If it is traverse the state/node chain, turning all actions/edges cyan
    '''
    state_space, start, goal = build_state_space(data, cnvs)
    if state_space:
        node = gb_agent(state_space, start, goal)
        if node == 'failure': print('No available path from start to goal')
        else:
            while node.parent != None:
                cnvs.itemconfigure(node.action['id'], fill='cyan')
                node = node.parent

def hlp_bttn_fn(hlp_txt):
    '''Toggles visibility of help text'''
    if hlp_txt.grid_info(): hlp_txt.grid_remove()
    else: hlp_txt.grid()

def bind_events(cnvs, hlp_txt, radio_mode, clr_grph, fnd_pth, hlp_bttn):
    '''Initialize data for graph then bind events to functions'''
    data = {
        'dot_size': 20, 'nodes': [], 'edges': [],
        'edge_node': None, 'start': None, 'goal': None
    }
    cnvs.bind('<1>', lambda evnt: cnvs_clck_fn(evnt, data, cnvs, radio_mode))
    clr_grph.bind('<1>', lambda evnt: clr_grph_fn(data, cnvs))
    fnd_pth.bind('<1>', lambda evnt: fnd_pth_fn(data, cnvs))
    hlp_bttn.bind('<1>', lambda evnt: hlp_bttn_fn(hlp_txt))