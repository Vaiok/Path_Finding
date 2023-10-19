import { Problem } from "./problem.mjs";
import { bestFirst } from "./search_algorithm.mjs";

function gbAgent(stateSpace, start, goal) {
	// AI agent that creates problem object and runs search algorithm
    function costFunction(node1, node2) {
        // Calculate distance to goal and add to distance traveled so far
        const state1 = JSON.parse(node1.state);
        const state2 = JSON.parse(node2.state);
        const heuristic1 = Math.hypot(Math.abs(state1['x'] - goal['x']) +
                                      Math.abs(state1['y'] - goal['y']));
        const heuristic2 = Math.hypot(Math.abs(state2['x'] - goal['x']) +
                                      Math.abs(state2['y'] - goal['y']));
        return (node2.pathCost + heuristic2) - (node1.pathCost + heuristic1);
    }
    const problem = new Problem(stateSpace, start, goal);
    return bestFirst(problem, costFunction);
}

export { gbAgent };