class Problem {
    // Class that holds and calculates problem specific information
    constructor(stateSpace, start, goal) {
        this.states = stateSpace;
        this.initial = JSON.stringify(start);
        this.goal = goal;
    }
    actions(strState) {
        // Find current state in state space then return that states actions
        const state = JSON.parse(strState);
        for (let spState of this.states) {
            if (spState['state']['x'] === state['x'] &&
                spState['state']['y'] === state['y']) {
                return spState['actions'];
            }
        }
    }
    actionCost(strState1, strState2) {
        // Calculate and return distance between current node and next node
        const state1 = JSON.parse(strState1), state2 = JSON.parse(strState2);
        return Math.hypot(Math.abs(state1['x'] - state2['x']) +
                          Math.abs(state1['y'] - state2['y']));
    }
    isGoal(strState) {
        // Return whether the current state and goal state match
        const state = JSON.parse(strState);
        if (state['x'] === this.goal['x'] && state['y'] === this.goal['y']) {
            return true;
        }
        else {return false;}
    }
    result(action) {
        // Return next state(dest) after taking action in current state
        return JSON.stringify({'x': action['x'],
                               'y': action['y']});
    }
}

export { Problem };