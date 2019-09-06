"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

To select an agent, use the '-p' option when running pacman.py.
Arguments can be passed to your agent using '-a'.
For example, to load a SearchAgent that uses depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch

Commands to invoke other search strategies can be found in the project description.

Please only change the parts of the file you are asked to.
Look for the lines that say:
"*** Your Code Here ***"

Good luck and happy searching!
"""

import game
import search
import searchAgents
import util

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.

    See the searchAgents.PositionSearchProblem class for an example of
    a working SearchProblem.
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.height - 2
        right = self.walls.width - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))

        self._expanded = 0  # Number of search nodes expanded

        # *** Your Code Here ***

        # you need to know pacman's  position, list of visited corners, 
        # list of corners left to visit

    def startingState(self):
        """
        Returns the start state (in your state space, not the full Pacman state space)
        """
        # *** Your Code Here ***
        return (self.startingPosition, [])

        util.raiseNotDefined()

    def isGoal(self, state):
        """
        Returns whether this search state is a goal state of the problem
        """

        # *** Your Code Here ***
        (currentState, currentVisited) = state
        return all(elem in currentVisited for elem in self.corners)
        util.raiseNotDefined()

    def successorStates(self, state):
        successors = []
        (currentState, currentVisited) = state
        for action in [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]:
            x, y = currentState
            dx, dy = game.Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                if nextState in self.corners:
                    if nextState not in currentVisited:
                        nextVisited = currentVisited.copy()
                        nextVisited.append(nextState)
                        successors.append( ( (nextState, nextVisited), action, 1) )
                        #print ("nextVisited:", nextVisited)
                else:
                    successors.append( ( (nextState, currentVisited), action, 1) )
            """
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                if (nextx, nexty) in self.corners:
                    if nextState not in currentVisited:
                        nextVisited = list(currentVisited)
                        nextVisited.append(nextState)
                        successors.append( ((nextState, nextVisited), action, 1) )
                else:
                    nextVisited = list(currentVisited)
                    successors.append( ((nextState, nextVisited), action, 1) )
            """
        self._expanded += 1
        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None:
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = game.Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

        state:   The current search state (a data structure you chose in your search problem)

        problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem; i.e.
    it should be admissible.  (You need not worry about consistency for
    this heuristic to receive full credit.)
    """

    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid (game.py)

    # *** Your Code Here ***
    (currentState, currentVisited) = state
    x, y = currentState
    unvisited = []
    maximum = 0
    for corner in corners:
        if corner not in currentVisited:
            unvisited.append(corner)
    if unvisited:
        for corner in unvisited:
            a, b = corner
            distance = (abs(a - x) + abs(b - y))
            if distance > maximum:
                maximum = distance
    return maximum

    """
    minimum = 1000000000000000000
    for corner in unvisited:
        a, b = corner
        distance = (abs(a - x) + abs(b - y))
        if distance < minimum:
             minimum = distance
    return minimum
    """

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
        problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state

    # *** Your Code Here ***
    walls = problem.walls
    x, y = position
    #print (walls)
    #print ("position:", position)
    #print (foodGrid)

    food = foodGrid.asList()
    maximum = 0

    #problem.heuristicInfo['wallCount'] = problem.walls.count()
    #print (problem.heuristicInfo['wallCount'])
    """
    unvisited = []
    for corner in corners:
        if corner not in currentVisited:
            unvisited.append(corner)
    """
    if food:
        for pellet in food:
            a, b = pellet
            distance = (abs(a - x) + abs(b - y))
            if distance > maximum:
                maximum = distance
    return maximum

    util.raiseNotDefined()

class ClosestDotSearchAgent(searchAgents.SearchAgent):
    """
    Search for all food using a sequence of searches
    """

    def registerInitialState(self, state):
        self.actions = []
        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self.actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState
        """

        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        return search.uniformCostSearch(problem)

        util.raiseNotDefined()
        return None

class AnyFoodSearchProblem(searchAgents.PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but
    has a different goal test, which you need to fill in below.  The
    state space and successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(searchAgents.PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in
    the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        """
        Stores information from the gameState.  You don't need to change this.
        """

        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited = {}
        self._visitedlist = []
        self._expanded = 0

    def isGoal(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """

        x, y = state

        # *** Your Code Here ***
        foodAsList = self.food.asList()
        if state in foodAsList:
            return True
        return False

        util.raiseNotDefined()

class ApproximateSearchAgent(game.Agent):
    """
    Implement your contest entry here.  Change anything but the class name.
    """

    def registerInitialState(self, state):
        """
        This method is called before any moves are made.
        """

        # *** Your Code Here ***
        util.raiseNotDefined()

    def getAction(self, state):
        """
        From game.py:
        The game.Agent will receive a GameState and must return an action from
        game.Directions.{North, South, East, West, Stop}
        """

        # *** Your Code Here ***
        util.raiseNotDefined()
        return None
