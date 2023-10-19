function createNode(evnt, data) {
    // Ignore click if close enough to existing node, otherwise create new node
    for (let node of data['nodes']) {
        if (Math.abs(node['x'] - evnt.offsetX) < data['dotSize'] &&
            Math.abs(node['y'] - evnt.offsetY) < data['dotSize']) {
            return;
        }
    }
    data['nodes'].push({'x': evnt.offsetX, 'y': evnt.offsetY});
}
function createEdge(evnt, data) {
    // If click overlaps a node, select node as start or end of new edge
    for (let node of data['nodes']) {
        if (Math.abs(node['x'] - evnt.offsetX) < data['dotSize']/2 &&
            Math.abs(node['y'] - evnt.offsetY) < data['dotSize']/2) {
            // Make node the start node for new edge if there is no start
            if (!data['edgeNode']) {
                data['edgeNode'] = node;
                return;
            }
            // Prevent edges from a node to itself
            if (data['edgeNode'] === node) {return;}
            // Prevent duplicate edges
            else {
                for (let edge of data['edges']) {
                    if (edge['node1'] === node &&
                        edge['node2'] === data['edgeNode'] ||
                        edge['node1'] === data['edgeNode'] &&
                        edge['node2'] === node) {
                        return;
                    }
                }
            }
            // Make node the end node for new edge, then create edge
            data['edges'].push({'node1': data['edgeNode'], 'node2': node});
            data['edgeNode'] = null;
        }
    }
}
function findItem(evnt, data) {
    // Test each node and edge returning any that overlaps with the click
    for (let node of data['nodes']) {
        if (Math.abs(node['x'] - evnt.offsetX) < data['dotSize']/2 &&
            Math.abs(node['y'] - evnt.offsetY) < data['dotSize']/2) {
            return node;
        }
    }
    for (let edge of data['edges']) {
        const en1 = edge['node1'], en2 = edge['node2'];
        let xPrcnt = 0, yPrcnt = 1;
        // Test if click lies between x and y values of both ends of the line
        if (Math.min(en1['x'], en2['x']) - 2 <= evnt.offsetX &&
            evnt.offsetX <= Math.max(en1['x'], en2['x']) + 2 &&
            Math.min(en1['y'], en2['y']) - 2 <= evnt.offsetY &&
            evnt.offsetY <= Math.max(en1['y'], en2['y']) + 2) {
            // Line is almost completely vertical or horizontal
            if (Math.abs(en1['x'] - en2['x']) < data['dotSize']/2 ||
                Math.abs(en1['y'] - en2['y']) < data['dotSize']/2) {
                return edge;
            }
            // Line goes between top left to bottom right
            else if (en1['x'] < en2['x'] && en1['y'] < en2['y'] ||
                en1['x'] > en2['x'] && en1['y'] > en2['y']) {
                xPrcnt = (en2['x'] - evnt.offsetX) / (en2['x'] - en1['x']);
                yPrcnt = (en2['y'] - evnt.offsetY) / (en2['y'] - en1['y']);
            }
            // Line goes between bottom left to top right
            else if (en1['x'] < en2['x'] && en1['y'] > en2['y'] ||
                en1['x'] > en2['x'] && en1['y'] < en2['y']) {
                xPrcnt = (en2['x'] - evnt.offsetX) / (en2['x'] - en1['x']);
                yPrcnt = (evnt.offsetY - en2['y']) / (en1['y'] - en2['y']);
            }
            // If xPrcnt and yPrcnt are the same, click was on the line vector
            if (Math.abs(xPrcnt - yPrcnt) < 0.1) {return edge;}
        }
    }
}

function deleteItem(data, item) {
    // Reset path, check for item in nodes and edges, then delete item if found
    data['edgePath'] = [];
    if (data['nodes'].includes(item)) {
        // Before deleting node, find and delete edges connected to it
        const dependantEdges = [];
        for (let edge of data['edges']) {
            if (item === edge['node1'] || item === edge['node2']) {
                dependantEdges.push(edge);
            }
        }
        for (let edge of dependantEdges) {deleteItem(data, edge);}
        data['nodes'] = data['nodes'].filter((elem) => elem !== item);
        // Reset data value if deleted node was start, goal, or selected for edge
        if (item === data['edgeNode']) {data['edgeNode'] = null;}
        if (item === data['start']) {data['start'] = null;}
        if (item === data['goal']) {data['goal'] = null;}
    }
    if (data['edges'].includes(item)) {
        data['edges'] = data['edges'].filter((elem) => elem !== item);
    }
}

function selectStart(evnt, data) {
    // Test each node setting any that overlap with click as the start
    for (let node of data['nodes']) {
        if (Math.abs(node['x'] - evnt.offsetX) < data['dotSize']/2 &&
            Math.abs(node['y'] - evnt.offsetY) < data['dotSize']/2) {
            // If new start is goal, clear goal before updating start
            if (node === data['goal']) {data['goal'] = null;}
            data['start'] = node;
        }
    }
}

function selectGoal(evnt, data) {
    // Test each node setting any that overlap with click as the goal
    for (let node of data['nodes']) {
        if (Math.abs(node['x'] - evnt.offsetX) < data['dotSize']/2 &&
            Math.abs(node['y'] - evnt.offsetY) < data['dotSize']/2) {
            // If new goal is start, clear start before updating goal
            if (node === data['start']) {data['start'] = null;}
            data['goal'] = node;
        }
    }
}

function cnvsClckFn(evnt, data) {
    // Matches the selected radio mode to its corresponding function
    const inputTags = document.querySelectorAll('input');
    for (let tag of inputTags) {
        if (tag.checked) {
            switch (tag.value) {
                case 'nodes':
                    createNode(evnt, data);
                    break;
                case 'edges':
                    createEdge(evnt, data);
                    break;
                case 'delete':
                    let item = findItem(evnt, data);
                    deleteItem(data, item);
                    break;
                case 'start':
                    selectStart(evnt, data);
                    break;
                case 'goal':
                    selectGoal(evnt, data);
                    break;
                default:
                    console.log('Invalid Radio Mode Value Of: ', tag.value);
            }
        }
    }
}

export { cnvsClckFn };