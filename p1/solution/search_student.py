"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

import util

# Called by search.depthFirstSearch.
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    """

    # *** Your Code Here ***

    # followed psuedocode from textbook pg. 77 function GRAPH_SEARCH(problem)
    # also used similar structure from successorStates(self, state) (FoodSearchProblem) from searchAgents.py

    startState = problem.startingState()
    path = util.Stack()
    path.push( (startState, [], 0) )
    visited = []

    actions = []
    actions2 = []

    while not path.isEmpty():

        (state, actions, cost) = path.pop()

        if problem.isGoal(state) is True:
            return actions

        if state not in visited:
            visited.append(state)

        #print ("actions:", actions)
        successors = problem.successorStates(state)
        for (nextState, nextAction, newCost) in successors:
            if nextState not in visited and nextState not in path.list:
                actions2 = actions.copy()
                actions2.append(nextAction)
                #print ("actions2:", actions2)
                #actions.append(nextAction)
                path.push( (nextState, actions2, newCost) )
                #path.push( (nextState, actions2, newCost) )

    return actions

    util.raiseNotDefined()


# Called by search.breadthFirstSearch.
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # used psuedocode from p. 81
    # structure from DFS alg above

    # *** Your Code Here ***
    startState = problem.startingState()
    if problem.isGoal(startState):
        return []
    path = util.Queue()
    path.push( (startState, [], 0) )
    #print ("path:", path.list)
    visited = []
    actions = []
    actions2 = []

    while not path.isEmpty():
        #print ("entered while loop")

        (state, actions, cost) = path.pop()
        #print ("im here")
        if state not in visited:
            visited.append(state)
        #print ("i'm also here")
        successors = problem.successorStates(state)
        #print ("im here too")
        #print ("successors:", successors)
        #print ("state:", state)
        for (nextState, nextAction, newCost) in successors:
            #print ("entered for loop")
            if nextState not in visited:
                if nextState not in path.list:
                    #print ("entered if statement")
                    visited.append(nextState)
                    actions2 = actions.copy()
                    actions2.append(nextAction)
                    #print ("isGoal:", problem.isGoal(nextState))
                    path.push( (nextState, actions2, newCost) )

            if problem.isGoal(nextState):
                return actions2
        #print ("path:", path.list)

    return actions2

    util.raiseNotDefined()

# Called by search.uniformCostSearch.
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    startState = problem.startingState()
    if problem.isGoal(startState):
        return []
    path = util.PriorityQueue()
    path.push( (startState, [], 0), 0)
    #print ("startState:", startState)
    pathList =[]
    pathList.append(startState)
    visited = []

    actions = []
    actions2 = []

    while not path.isEmpty():
        (state, actions, cost) = path.pop()
        #print ("pathList before remove:", pathList)
        #print ("state[0]:",state[0])
        pathList.remove(state)
        #print ("pathlist after remove:", pathList)

        if problem.isGoal(state):
            return actions

        if state not in visited:
            visited.append(state)

        successors = problem.successorStates(state)
        for(nextState, nextAction, newCost) in successors:
            actions2 = actions.copy()
            actions2.append(nextAction)
            priority = newCost + cost
            if nextState not in visited and nextState not in pathList:
                #print ("nextState1stif:", nextState)
                path.push( (nextState, actions2, priority), priority)
                pathList.append(nextState)
                #print ("pathListIn1stIf:",pathList)
            elif nextState in pathList and newCost > priority:
                #print ("nextState2ndif:", nextState)
                path.push( (nextState, actions2, priority), priority)
                pathList.append(nextState)
                #print ("pathListIn2ndIf:",pathList)
    return actions

    util.raiseNotDefined()

# Called by search.aStarSearch.
def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    startState = problem.startingState()
    if problem.isGoal(startState):
        return []
    path = util.PriorityQueue()
    path.push( (startState, [], 0), 0)
    #print ("startState:", startState)
    visited = []

    actions = []
    actions2 = []
    pathList =[]
    pathList.append(startState)

    while not path.isEmpty():
        (state, actions, cost) = path.pop()
        #print ("pathList before remove:", pathList)
        #print ("state[0]:",state[0])
        pathList.remove(state)
        #print ("pathlist after remove:", pathList)

        if problem.isGoal(state):
            return actions

        if state not in visited:
            visited.append(state)

        successors = problem.successorStates(state)
        for(nextState, nextAction, newCost) in successors:
            actions2 = actions.copy()
            actions2.append(nextAction)
            priority = cost + newCost
            heuristicPriority = cost + heuristic(nextState, problem)
            if nextState not in visited:
                if nextState not in pathList:
                    #print ("nextState1stif:", nextState)
                    path.push( (nextState, actions2, priority), heuristicPriority)
                    pathList.append(nextState)
                    #print ("pathListIn1stIf:",pathList)
            elif nextState in pathList:
                if newCost > priority:
                    #print ("nextState2ndif:", nextState)
                    path.push( (nextState, actions2, priority), heuristicPriority)
                    pathList.append(nextState)
                    #print ("pathListIn2ndIf:",pathList)
    return actions

    util.raiseNotDefined()
