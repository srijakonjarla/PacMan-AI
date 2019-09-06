import random
import util
import captureAgents
import math
from game import Directions

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
        first = 'MyReflexCaptureAgent', second = 'MyReflexCaptureAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers. isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class MyReflexCaptureAgent(captureAgents.CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """
    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        IMPORTANT: This method may run for at most 15 seconds.
        """
        captureAgents.CaptureAgent.registerInitialState(self, gameState)

        # self.index ->  Team blue is 0 and 2, Red is 1 and 3

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s, a).
        """
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        # print('eval time for agent %d: %.4f' % (self.index, time.time() - start))

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != util.nearestPoint(pos):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        self.determineStrategy(gameState)
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def determineStrategy(self, gameState):
        myState = gameState.getAgentState(self.index)
        if myState.scaredTimer > 1:
            self.isOnOffense = True
        else:
            myPos = myState.getPosition()
            theirFood = self.getFood(gameState).asList()
            distToTheirFood = 1000
            bestAttacker = self.index
            if len(theirFood) > 0:
                for memberIndex in self.getTeam(gameState):
                    pos = gameState.getAgentState(memberIndex).getPosition()
                    minDistance = min([self.getMazeDistance(pos, food) for food in theirFood])
                    if minDistance < distToTheirFood:
                        distToTheirFood = minDistance
                        bestAttacker = memberIndex

            self.isOnOffense = (bestAttacker == self.index)


    def getFeatures(self, gameState, action):
        """
        Returns a counter of features for the state
        """
        if self.isOnOffense:
            return self.getOffensiveFeatures(gameState, action)
        else:
            return self.getDefensiveFeatures(gameState, action)

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.
        They can be either a counter or a dictionary.
        """
        if self.isOnOffense:
            return self.offensiveWeights(gameState, action)
        else:
            return self.defensiveWeights(gameState, action)

    def getOffensiveFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        myOldState = successor.getAgentState(self.index)
        myOldPos = myOldState.getPosition()
        myNewState = successor.getAgentState(self.index)
        myNewPos = myNewState.getPosition()

        # Compute distance to the nearest food
        foodList = self.getFood(successor).asList()
        if len(foodList) > 0:  # This should always be True, but better safe than sorry
            minDistance = min([self.getMazeDistance(myNewPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        scaryGhostDistance = 3

        oldOpponents = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        oldVisibleOpponents = [a for a in oldOpponents if a.getPosition() != None]
        if myNewState.isPacman:
            # Figure out if we are eating a ghost
            for opponent in oldVisibleOpponents:
                if not opponent.isPacman and myNewPos == opponent.getPosition():
                    # Colliding with ghost!
                    if opponent.scaredTimer > 0 and opponent.scaredTimer < 30:
                        # Not worth eating ghost too early after scaring.
                        features["ateGhost"] = 1
                    else:
                        features["suicideAsPacman"] = 1

            newOpponents = [successor.getAgentState(i) for i in self.getOpponents(successor)]
            newVisibleGhosts = [a for a in newOpponents if not a.isPacman and a.getPosition() != None]

            if myOldState.isPacman:
                # Don't try to cross over when a ghost is nearby!
                scaryGhostDistance = 5

            # Compute distance to the nearest ghost
            for ghost in newVisibleGhosts:
                newDist = self.getMazeDistance(myNewPos, ghost.getPosition())
                # Danger depends on how much longer the ghost is scared.
                # One that is scared for longer than it takes to close the gap
                # is not dangerous
                if ghost.scaredTimer <= newDist:
                    scaryGhostDistance = min(newDist, scaryGhostDistance)
        else: #Ghost, but on offense
            # Figure out if we are eating a pacman
            for opponent in oldVisibleOpponents:
                if opponent.isPacman and myNewPos == opponent.getPosition():
                    # Colliding with pacman!
                    if myOldState.scaredTimer > 0:
                        features["suicideAsGhost"] = 1
                    else:
                        features["atePacman"] = 1

        features['inverseDistToScaryGhost'] = 5 - scaryGhostDistance

        if action == Directions.STOP:
            features['stop'] = 1

        return features

    def offensiveWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'inverseDistToScaryGhost': -10,
            'ateGhost': 100, # encourages pacman to eat ghosts
            'atePacman': 500, # encourages ghost to eat pacman
            'suicideAsPacman': 0, # encourages pacman to stay alive while pacman
            # Suiciding as pacman allows for faster respawn (when cornered)
            'suicideAsGhost': -1000, # encourages pacman to stay alive while ghost
            'stop': -60,
        }

    def getDefensiveFeatures(self, gameState, action):
        """
        updates: removed the old distancetoFood feature, replaced it with average feature.
        removed the myFood variable since it was a redundant variable. We no longer use
        mindistance feature to stay near the food, we use averageDistance. We now add
        the capsule distance to average distance as well, and we removed the capsule
        feature. Sometimes capsule distances acts kind of odd, maybe comment it in and out as you
        see fit?
        """
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myNewPos = myState.getPosition()
        ourFood = self.getFoodYouAreDefending(gameState).asList()
        ourCapsules = self.getCapsulesYouAreDefending(gameState)
        ourStuff = ourFood + ourCapsules

        if len(ourStuff) == 0:
            return features # We lost

        #feature so we stick around our food
        distancesToOurStuff = [self.getMazeDistance(myNewPos, thing) for thing in ourStuff]
        avgDistanceToOurStuff = sum(distancesToOurStuff) / len(ourStuff)

        # here we want to add the capsuledistance to our average distance
        features['avgDistToOurStuff'] = avgDistanceToOurStuff

        # Compute whether we're on the right side to defend
        if myState.isPacman:
            # Try to get back on defensive side.
            # "I'm going ghost!" (He's a phantom!)
            features['onDefensiveSide'] = 0
        else:
            features['onDefensiveSide'] = 1

        # Compute distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        features['numInvaders'] = len(invaders)

        if len(invaders) > 0:
            dists = [self.getMazeDistance(myNewPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if action == Directions.STOP:
            features['stop'] = 1

        lastDirection = gameState.getAgentState(self.index).configuration.direction
        rev = Directions.REVERSE[lastDirection]
        left = Directions.LEFT[lastDirection]
        right = Directions.RIGHT[lastDirection]

        # Once our distance is close enough to the food,
        # then we can move around more freely to stay in that area
        dirMod = 1 if (avgDistanceToOurStuff <= 3) else 2
        if action == rev:
            features['reverse'] = 1 * dirMod
        if action == left or action == right:
            features['turningLeftOrRight'] = 1 * dirMod

        return features

    def defensiveWeights(self, gameState, action):
        return {
            'avgDistToOurStuff': -3,
            'numInvaders': -1000,
            'onDefensiveSide': 100,
            'invaderDistance': -100,
            'stop': -100,
            'reverse': -2,
            'turningLeftOrRight': -1
        }

"""""
def scoreEvaluationFunction(currentGameState):

    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This evaluation is based on game score, food proximity,
        number of threats, and closeness to nearby threats

    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    threatCount = 0
    nearestThreat = (None, 999999)
    fear = 0
    for ghostState in newGhostStates:
        scared = ghostState.scaredTimer
        if scared is 0:
            threatCount += 1

        pos = ghostState.configuration.getPosition()
        dist = util.manhattanDistance(pos, newPos)

        if dist <=4 and scared < dist/2 : # Be afraid.
            if dist < nearestThreat[1]:
                nearestThreat = (ghostState, dist)
                fear = (5 / (dist+1)) * 20

    nearestFood = nearestTarget(newPos, currentGameState.getFood().asList())

    foodProximity = (10 / (nearestFood[1]+1))

    # print("Fear: {}  Food: {}".format(fear, foodProximity))

    return currentGameState.getScore() - fear + foodProximity - (threatCount * 5)
"""

# class AlphaBetaAgent(captureAgents.CaptureAgent):
#     """
#     Minimax agent with alpha-beta pruning
#     """
#     def registerInitialState(self, gameState):
#         """
#         This method handles the initial setup of the
#         agent to populate useful fields (such as what team
#         we're on).
#
#         IMPORTANT: This method may run for at most 15 seconds.
#         """
#         captureAgents.CaptureAgent.registerInitialState(self, gameState)
#
#         # self.index ->  Team blue is 0 and 2, Red is 1 and 3
#         self.evaluationFunction = util.lookup("scoreEvaluationFunction")
#         self.treeDepth = 3
#
#     def chooseAction(self, gameState):
#         """
#         Returns the minimax action using self.treeDepth and self.evaluationFunction
#         """
#         bestMove = self.minimax(gameState, self.treeDepth, -math.inf, math.inf, 0)
#         return bestMove[0]
#
#     def minimax(self, gameState, depth, alpha, beta, agent):
#         isWin = len(self.getFood(gameState).asList()) <= 2
#         isLose = len(self.getFoodYouAreDefending(gameState).asList()) <= 2
#
#         if depth is 0 or isWin or isLose:
#             return (None, self.evaluationFunction(gameState))
#
#         nextAgent = agent+1 if agent+1 < gameState.getNumAgents() else 0
#         nextDepth = depth-1 if nextAgent is 0 else depth
#
#         print("Searching depth: {}".format(depth))
#
#         if agent is self.index: # Maximize
#             print("MAX")
#             maxEval = (None, -math.inf)
#             for action in gameState.getLegalActions(agent):
#                 if action is Directions.STOP:
#                     continue
#                 childState = gameState.generateSuccessor(agent, action)
#                 childEval = self.minimax(childState, nextDepth, alpha, beta, nextAgent)
#                 if childEval[1] > maxEval[1]:
#                     maxEval = (action, childEval[1])
#                 alpha = max(alpha, maxEval[1])
#                 if beta <= alpha:
#                     break
#             return maxEval
#
#         else: # Minimize
#             print("MIN: {}".format(gameState))
#             minEval = (None, math.inf)
#
#             for action in gameState.getLegalActions(agent):
#                 if action is Directions.STOP:
#                     continue
#                 childState = gameState.generateSuccessor(agent, action)
#                 childEval = self.minimax(childState, nextDepth, alpha, beta, nextAgent)
#                 if childEval[1] < minEval[1]:
#                     minEval = (action, childEval[1])
#                 beta = max(beta, minEval[1])
#                 if beta <= alpha:
#                     break
#             return minEval

class DummyAgent(captureAgents.CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        """
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        """


        captureAgents.CaptureAgent.registerInitialState(self, gameState)

        """
        Your initialization code goes here, if you need any.
        """

    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)

        """
        You should change this in your own agent.
        """

        return random.choice(actions)
