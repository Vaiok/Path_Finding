def create_node(evnt, data, cnvs):
    '''Ignore click if close enough to existing node, otherwise create new node'''
    for node in data['nodes']:
        if (abs(node['x'] - evnt.x) < data['dot_size'] and
            abs(node['y'] - evnt.y) < data['dot_size']):
            return
    new_dot = cnvs.create_oval(evnt.x - data['dot_size']/2,
                                evnt.y - data['dot_size']/2,
                                evnt.x + data['dot_size']/2,
                                evnt.y + data['dot_size']/2, fill='blue')
    data['nodes'].append({'x': evnt.x, 'y': evnt.y, 'dot': new_dot})
    
def create_edge(evnt, data, cnvs):
    '''If click overlaps a node, select node as start or end of new edge'''
    for node in data['nodes']:
        if (abs(node['x'] - evnt.x) < data['dot_size']/2 and
            abs(node['y'] - evnt.y) < data['dot_size']/2):
            # Make node the start node for new edge if there is no start
            if not data['edge_node']:
                data['edge_node'] = node
                return
            # Prevent edges from a node to itself
            if data['edge_node'] == node: return
            # Prevent duplicate edges
            else:
                for edge in data['edges']:
                    if (edge['node1'] == node and
                        edge['node2'] == data['edge_node'] or
                        edge['node1'] == data['edge_node'] and
                        edge['node2'] == node):
                        return
            # Make node the end node for new edge, then create edge
            new_line = cnvs.create_line(data['edge_node']['x'],
                                        data['edge_node']['y'],
                                        node['x'], node['y'], fill='red',
                                        width=data['dot_size']/4)
            data['edges'].append({'node1': data['edge_node'],
                                    'node2': node, 'line': new_line})
            data['edge_node'] = None

def find_item(evnt, data): 
    '''Test each node and edge returning any that overlaps with the click'''
    for node in data['nodes']:
        if (abs(node['x'] - evnt.x) < data['dot_size']/2 and
            abs(node['y'] - evnt.y) < data['dot_size']/2):
            return node
    for edge in data['edges']:
        en1, en2 = edge['node1'], edge['node2']
        x_prcnt, y_prcnt = 0, 1  
        # Test if click lies between x and y values of both ends of the line
        if (min(en1['x'], en2['x']) - 2 <= evnt.x <=
            max(en1['x'], en2['x']) + 2 and
            min(en1['y'], en2['y']) - 2 <= evnt.y <=
            max(en1['y'], en2['y']) + 2):
            # Line is almost completely vertical or horizontal
            if (abs(en1['x'] - en2['x']) < data['dot_size']/2 or
                abs(en1['y'] - en2['y']) < data['dot_size']/2):
                return edge
            # Line goes between top left to bottom right
            elif (en1['x'] < en2['x'] and en1['y'] < en2['y'] or
                  en1['x'] > en2['x'] and en1['y'] > en2['y']):
                x_prcnt = (en2['x'] - evnt.x) / (en2['x'] - en1['x'])
                y_prcnt = (en2['y'] - evnt.y) / (en2['y'] - en1['y'])
            # Line goes between bottom left to top right
            elif (en1['x'] < en2['x'] and en1['y'] > en2['y'] or
                  en1['x'] > en2['x'] and en1['y'] < en2['y']):
                x_prcnt = (en2['x'] - evnt.x) / (en2['x'] - en1['x'])
                y_prcnt = (evnt.y - en2['y']) / (en1['y'] - en2['y'])
            # If x_prcnt and y_prcnt are the same, click was on the line vector
            if abs(x_prcnt - y_prcnt) < 0.1: return edge
        
def delete_item(data, cnvs, item):
    '''Check for item in nodes and edges then delete item if found'''
    if item in data['nodes']:
        # Before deleting node, find and delete edges connected to it
        dependant_edges = []
        for edge in data['edges']:
            if item == edge['node1'] or item == edge['node2']:
                dependant_edges.append(edge)
        for edge in dependant_edges: delete_item(data, cnvs, edge)
        cnvs.delete(item['dot'])
        data['nodes'].remove(item)
        # Reset data value if deleted node was start, goal, or selected for edge
        if item == data['edge_node']: data['edge_node'] = None
        if item == data['start']: data['start'] = None
        if item == data['goal']: data['goal'] = None
    if item in data['edges']:
        cnvs.delete(item['line'])
        data['edges'].remove(item)

def select_start(evnt, data, cnvs):
    '''Test each node setting any that overlap with click as the start'''
    for node in data['nodes']:
        if (abs(node['x'] - evnt.x) < data['dot_size']/2 and
            abs(node['y'] - evnt.y) < data['dot_size']/2):
            # Reset old start color before updating new start color
            if data['start']:
                cnvs.itemconfigure(data['start']['dot'], fill='blue')
            cnvs.itemconfigure(node['dot'], fill='green')
            # If new start is goal, clear goal before updating start
            if node == data['goal']: data['goal'] = None
            data['start'] = node

def select_goal(evnt, data, cnvs):
    '''Test each node setting any that overlap with click as the goal'''
    for node in data['nodes']:
        if (abs(node['x'] - evnt.x) < data['dot_size']/2 and
            abs(node['y'] - evnt.y) < data['dot_size']/2):
            # Reset old goal color before updating new goal color
            if data['goal']:
                cnvs.itemconfigure(data['goal']['dot'], fill='blue')
            cnvs.itemconfigure(node['dot'], fill='magenta')
            # If new goal is start, clear start before updating goal
            if node == data['start']: data['start'] = None
            data['goal'] = node

def cnvs_clck_fn(evnt, data, cnvs, radio_mode):
    '''Matches the selected radio mode to its corresponding function'''
    match radio_mode.get():
        case 'nodes': create_node(evnt, data, cnvs)
        case 'edges': create_edge(evnt, data, cnvs)
        case 'delete':
            item = find_item(evnt, data)
            delete_item(data, cnvs, item)
        case 'start': select_start(evnt, data, cnvs)
        case 'goal': select_goal(evnt, data, cnvs)
        case _: print('Invalid Radio Mode Value Of: ', radio_mode.get())