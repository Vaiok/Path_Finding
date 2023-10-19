class Node {
	// Class to hold data about the current state and path leading to it
	constructor(state, prnt=null, action=null, pathCost=0) {
		this.state = state;
		this.prnt = prnt;
		this.action = action;
		this.pathCost = pathCost;
	}
}

function* expand(problem, node) {
	// Loop through actions determining each next state and cost of action
	const s1 = node.state;
	for (let action of problem.actions(s1)) {
		const s2 = problem.result(action);
		const cost = node.pathCost + problem.actionCost(s1, s2);
		yield new Node(s2, node, action, cost);
	}
}

function bestFirst(problem, f) {
	/*
	Build node and add to frontier(potential moves) and reached
    Then search frontier for goal, return goal node or failure(frontier empty)
    If a node is not the goal, expand child nodes from it
    Test if a child node is a new state or a shorter path to an previous state
    If so add child node to reached and frontier, then sort frontier
	*/
	let node = new Node(problem.initial);
	const frontier = [node];
	const reached = {};
	reached[node.state] = node;
	while (frontier.length > 0) {
		node = frontier.pop();
		if (problem.isGoal(node.state)) {return node;}
		for (let child of expand(problem, node)) {
			const s = child.state;
			if (!Object.hasOwn(reached, s) || child.pathCost < reached[s].pathCost) {
				reached[s] = child;
				frontier.push(child);
				frontier.sort(f);
			}
		}
	}
	return 'failure';
}

export { bestFirst };