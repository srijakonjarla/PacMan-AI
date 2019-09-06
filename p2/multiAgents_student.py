import random

import game
import util

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """

    return currentGameState.getScore()

class MultiAgentSearchAgent(game.Agent):
    """
    This class provides some common elements to all of your multi-agent searchers.
    Any methods defined here will be available to the
    MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.
    Please do not remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.
    It's only partially specified, and designed to be extended.
    Agent (game.py) is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn)
        self.treeDepth = int(depth)

class ReflexAgent(game.Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit, so long as you don't touch the method headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some game.Directions.X for some X in the set {North, South, West, East, Stop}
        """

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        #print ("legal moves:", *legalMoves)
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print ("scores:", *scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        #print ("bestIndices", *bestIndices)
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        # *** Add more of your code here if you want to ***

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # *** Your Code Here ***
        food = oldFood.asList() #hold coordinates of the food pellet
        x, y = newPosition
        distancesFromFood = []
        distancesFromGhost = []
        reward = 0

        for pellet in food:
            a, b = pellet
            distance = (abs(a - x) + abs(b - y))
            distancesFromFood.append(distance)

        #print ("food:", *distancesFromFood)

        closestPelletDistance = min(distancesFromFood)
        reward += (10 - closestPelletDistance)

        for ghostState in newGhostStates:
            a, b = ghostState.getPosition()
            distance = (abs(a - x) + abs(b - y))
            distancesFromGhost.append(distance)

        #print ("ghost:", *distancesFromGhost)

        for dist in distancesFromGhost:
            if dist >= 2:
                reward += dist
            else:
                reward -= (40 + dist)

        return successorGameState.getScore() + reward

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.treeDepth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

        game.Directions.STOP:
            The stop direction, which is always legal

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        # *** Your Code Here ***
        """
        NOTES TO SELF:
        minimax for this q:
            -need to return an action
            -you need to iterate until treedepth = 0
            -the self.evaluationfunction gives you the utlity
            -the iteration goes: max, then min but min is all the ghosts iterated
            so you need to check the index of the ghost against the number of agents
            -the max and call min those many times
            -the best action once the terminal test is true is automatically stop
            -max and min return the max utility and the min utility respectively each depth
            -the final getaction needs to return the best action
            1. in get action, return action
            2. in the minimax function, check if its a terminal state, then check what the agent
            index is
                - if it's 0 then calculate the max and if it's anything other than 0 calculate
                the min and iterate the min until the index is greater than the number of ghosts
                there are
                -in max and min return a utility value that corresponds with an action
                -use a tuple to do that ??
                -everytime you call minimax use the newGameState which is the successor
                -everytime you do a min call, increase the agentIndex
                -everytime you do a max call, decrease the depth
                -v would correspond to a utility value but in this case a utility value and 
                its action?
        """

        #Used Pseudocode from minimax wikipedia page
        depth = self.treeDepth
        (score, best) = self.minimax(gameState, depth, 0, True)
        return best

    def minimax(self, gameState, depth, agentIndex, maximizingPlayer):
        check = gameState.getLegalActions(agentIndex)
        utility = self.evaluationFunction(gameState)
        numOfGhosts = gameState.getNumAgents()-1
        best = None
        #print("hello1")

        if depth == 0 or check == []:
        #    print("hello2")
            return (utility, game.Directions.STOP)

        if maximizingPlayer == True:
        #    value = float("-inf")
            actions = gameState.getLegalActions(0)
        #    print("hello3")
            for action in actions:
        #        print(value)
        #        print("hello4")
                nextGameState = gameState.generateSuccessor(0, action)
                (value, nextAction) = self.minimax(nextGameState, depth-1, 1, False)
        #        print(value)
        #        print("im here")
                if best is None or best[0] < value:
                    best = (value, action)
        else:
        #    value = float("inf")
            actions = gameState.getLegalActions(agentIndex)
        #    print("hello5")
            for action in actions:
        #        print("hello6")
                nextGameState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex < numOfGhosts:
        #            print("hello7")
                    (value, nextAction) = self.minimax(nextGameState, depth, agentIndex+1, False)
        #            print(value)
                    if best is None or best[0] > value:
                        best = (value, action)
                else:
        #            print("hello8")
                    (value, nextAction) = self.minimax(nextGameState, depth, 0, True)
        #            print(value)
                    if best is None or best[0] > value:
                        best = (value, action)

        return best

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.treeDepth and self.evaluationFunction
        """

        # *** Your Code Here ***
        depth = self.treeDepth
        (score, best) = self.alphaBeta(gameState, depth, float("-inf"), float("inf"), 0, True)
        return best
    
    def alphaBeta(self, gameState, depth, a, b, agentIndex, maximizingPlayer):
        check = gameState.getLegalActions(agentIndex)
        utility = self.evaluationFunction(gameState)
        numOfGhosts = gameState.getNumAgents()-1
        best = None

        if depth == 0 or check == []:
            return (utility, game.Directions.STOP)

        if maximizingPlayer == True:
            actions = gameState.getLegalActions(0)
            for action in actions:
                nextGameState = gameState.generateSuccessor(0, action)
                (value, nextAction) = self.alphaBeta(nextGameState, depth, a, b, 1, False)
                if best is None or best[0] < value:
                    best = (value, action)
                a = max(a, value)
                if a >= b:
                    break
        else:
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nextGameState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex < numOfGhosts:
                    (value, nextAction) = self.alphaBeta(nextGameState, depth, a, b, agentIndex+1, False)
                    if best is None or best[0] > value:
                        best = (value, action)
                    b = min(b, value)
                    if a >= b:
                        break
                else:
                    (value, nextAction) = self.alphaBeta(nextGameState, depth-1, a, b, 0, True)
                    if best is None or best[0] > value:
                        best = (value, action)
                    b = min(b, value)
                    if a >= b:
                        break

        return best

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.treeDepth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        depth = self.treeDepth
        (score, best) = self.minimax(gameState, depth, 0, True)
        return best

    def minimax(self, gameState, depth, agentIndex, maximizingPlayer):
        check = gameState.getLegalActions(agentIndex)
        utility = self.evaluationFunction(gameState)
        numOfGhosts = gameState.getNumAgents()-1
        best = None

        if depth == 0 or check == []:
            return (utility, game.Directions.STOP)

        if maximizingPlayer == True:
            actions = gameState.getLegalActions(0)
            for action in actions:
                nextGameState = gameState.generateSuccessor(0, action)
                (value, nextAction) = self.minimax(nextGameState, depth, 1, False)
                if best is None or best[0] < value:
                    best = (value, action)
        else:
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nextGameState = gameState.generateSuccessor(agentIndex, action)
                total = 0
                if agentIndex < numOfGhosts:
                    (value, nextAction) = self.minimax(nextGameState, depth, agentIndex+1, False)
                    total += value
                    average = total/len(actions)
                    best = (average, action)
                else:
                    (value, nextAction) = self.minimax(nextGameState, depth-1, 0, True)
                    total += value
                    average = total/len(actions)
                    best = (average, action)

        return best

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    # *** Your Code Here ***
    reward = 0
    x, y = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    ghostPositions = []
    for ghostState in ghostStates:
            ghostPositions.append(ghostState.getPosition())
    pacmanActions = currentGameState.getLegalActions(0)
    foodGrid = currentGameState.getFood()
    food = foodGrid.asList()
    distancesFromFood = []
    distancesFromGhost = []

    if len(food) > 0:
        for pellet in food:
            a, b = pellet
            distance = (abs(a - x) + abs(b - y))
            distancesFromFood.append(distance)

    for ghost in ghostPositions:
        a, b = ghost
        distance = (abs(a - x) + abs(b - y))
        distancesFromGhost.append(distance)

    if len(distancesFromFood) == 0:
        closestPelletDistance = 0
    else:
        closestPelletDistance = min(distancesFromFood)
    reward += (20 - closestPelletDistance)
    
    for dist in distancesFromGhost:
        if dist >= 2:
            reward += dist
        else:
            reward -= (400 + dist)

    return currentGameState.getScore() + reward


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
        Returns an action.
        You can use any method you want and search to any depth you want.
        Just remember that the mini-contest is timed, so you have to trade off speed and computation.

        Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
        just make a beeline straight towards Pacman (or away from him if they're scared!)
        """

        # *** Your Code Here ***
        util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
