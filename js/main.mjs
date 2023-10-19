import { gbAgent } from "./agent.mjs";
import { cnvsClckFn } from "./canvas_events.mjs";

function drwGrph(cnvs, drw, data) {
    // Calibrate and clear canvas, then draw nodes, edges, and the path
    cnvs.width = cnvs.clientWidth;
    cnvs.height = cnvs.clientHeight;
    drw.fillStyle = 'white';
    drw.fillRect(0, 0, cnvs.width, cnvs.height);
    for (let node of data['nodes']) {
        drw.fillStyle = 'blue';
        // If node is start or goal, set different color
        if (node === data['start']) {drw.fillStyle = 'green';}
        else if (node === data['goal']) {drw.fillStyle = 'magenta';}
        drw.beginPath();
        drw.arc(node['x'], node['y'], data['dotSize']/2, 0, Math.PI*2);
        drw.fill();
    }
    for (let edge of data['edges']) {
        drw.strokeStyle = 'red';
        drw.lineWidth = data['dotSize']/4;
        drw.beginPath();
        drw.moveTo(edge['node1']['x'], edge['node1']['y']);
        drw.lineTo(edge['node2']['x'], edge['node2']['y']);
        drw.stroke();
    }
    if (data['edgePath'].length > 1) {
        const dep = data['edgePath'];
        drw.strokeStyle = 'cyan';
        drw.beginPath();
        drw.moveTo(dep[0]['x'], dep[0]['y']);
        for (let path = 1; path < dep.length; path++) {
            drw.lineTo(dep[path]['x'], dep[path]['y']);
        }
        drw.stroke();
    }
};

function buildStateSpace(data) {
    /*
    If start or goal are not set ignore the click
    Otherwise set their states and build the state space for AI agent
    */
    if (!data['start'] || !data['goal']) {
        console.log('Must select a start node and goal node');
        return [null, null, null];
    }
    let start = {'x': data['start']['x'], 'y': data['start']['y']};
    let goal = {'x': data['goal']['x'], 'y': data['goal']['y']};
    let stateSpace = [];
    for (let node of data['nodes']) {
        const act = [];
        for (let edge of data['edges']) {
            // Turn all edges into actions
            if (node === edge['node1']) {
                act.push({'x': edge['node2']['x'], 'y': edge['node2']['y']});
            }
            else if (node === edge['node2']) {
                act.push({'x': edge['node1']['x'], 'y': edge['node1']['y']});
            }
        }
        // Turn all nodes into states
        stateSpace.push({
            'state': {'x': node['x'], 'y': node['y']}, 'actions': act
        });
    }
    return [stateSpace, start, goal];
}

function fndPthFn(data) {
    /*
    Build state space, run AI agent, and test if agent search is successful
    If so traverse the state/node chain, adding all actions/edges to edgePath
    */
    data['edgePath'] = [];
    let [stateSpace, start, goal] = buildStateSpace(data);
    if (stateSpace) {
        let node = gbAgent(stateSpace, start, goal)
        if (node === 'failure') {
            console.log('No available path from start to goal');
        }
        else {
            while (node.prnt !== null) {
                data['edgePath'].push(JSON.parse(node.state));
                node = node.prnt;
            }
            data['edgePath'].push(JSON.parse(node.state));
        }
    }
}

function startProgram() {
    // Initialize canvas and data for graph, then bind events to functions
    const cnvs = document.querySelector('#graphCnvs');
    const drw = cnvs.getContext('2d');
    cnvs.width = cnvs.clientWidth;
    cnvs.height = cnvs.clientHeight;
    const data = {
        'dotSize': 20, 'nodes': [], 'edges': [], 'edgePath': [],
        'edgeNode': null, 'start': null, 'goal': null
    };
    const clearGraph = document.querySelector('#clearGraph');
    const findRoute = document.querySelector('#findRoute');
    const helpBttn = document.querySelector('#helpBttn');
    document.addEventListener('contextmenu', (evnt) => evnt.preventDefault());
    window.addEventListener('resize', (evnt) => drwGrph(cnvs, drw, data));
    cnvs.addEventListener('click', (evnt) => {
        // Process canvas click then redraw
        cnvsClckFn(evnt, data);
        drwGrph(cnvs, drw, data);
    });
    clearGraph.addEventListener('click', (evnt) => {
        // Reset data then redraw
        data['nodes'] = [], data['edges'] = [], data['edgePath'] = [];
        data['edgeNode'] = null, data['start'] = null, data['goal'] = null;
        drwGrph(cnvs, drw, data);
    });
    findRoute.addEventListener('click', (evnt) => {
        fndPthFn(data);
        drwGrph(cnvs, drw, data);
    });
    helpBttn.addEventListener('click', (evnt) => {
        // Toggles visibility of help text
        const ht = document.querySelector('#helpTxt');
        ht.style.visibility = (ht.style.visibility === 'hidden') ?
            'visible' : 'hidden';
    });
}

startProgram();