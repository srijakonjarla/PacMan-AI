import learningAgents
import mdp
import util

class ValueIterationAgent(learningAgents.ValueEstimationAgent):
    """
    * Please read learningAgents.py before reading this.*

    A ValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs value iteration
    for a given number of iterations using the supplied
    discount factor.
    """

    def __init__(self, mdp, discountRate = 0.9, iters = 100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.

        Some useful mdp methods you will use:
            mdp.getStates()
            mdp.getPossibleActions(state)
            mdp.getTransitionStatesAndProbs(state, action)
            mdp.getReward(state, action, nextState)
        """

        super().__init__()

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = util.Counter() # A Counter is a dict with default 0

        """
        Description:
        Initializes values. Finds the QValues of and appends max QValue.
        """

        """ YOUR CODE HERE """
        #print ("init")
        currentStates = self.mdp.getStates()
        for x in range (self.iters):
            vals = self.values.copy()
            for state in currentStates:
                actions = mdp.getPossibleActions(state)
                qVals = []
                for action in actions:
                    qVals.append(self.getQValue(state, action))
        #        print (*qVals)
                if qVals:
                    vals[state] = max(qVals)
            self.values = vals
        """ END CODE """

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        #print ("getValue")
        return self.values[state]

    def getQValue(self, state, action):
        """
        The q-value of the state action pair
        (after the indicated number of value iteration passes).
        Note that value iteration does not
        necessarily create this quantity and you may have
        to derive it on the fly.
        """

        """
        Description:
        Used the equation given in lecture slides.
        """

        """ YOUR CODE HERE """
        #print ("getQValue")
        nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
        qValue = 0

    #    print (*nextStates)  
        for (nextState, nextProb) in nextStates:
            reward = self.mdp.getReward(state, action, nextState)
            value = self.getValue(nextState)
    #        print ("value:",value)
            discount = value * self.discountRate
    #        print ("discount:", discount)
    #        print ("nextProb", nextProb)
            qValue += nextProb * (reward+discount)
    #    print("exited for loop")
        return qValue

        """ END CODE """

    def getPolicy(self, state):
        """
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.
        Note that if there are no legal actions, which is the case at the
        terminal state, you should return None.
        """

        """
        Description:
        Found the corresponding action for the max QValue.
        """

        """ YOUR CODE HERE """
    #    print ("getPolicy")
        actions = self.mdp.getPossibleActions(state)

    #    print ("actions:", actions)

        if not actions:
            return None

        policy = None
        maxqValue = float("-inf")
        for action in actions:
    #        print("in get policy loop")
            qValue = self.getQValue(state, action)
            if qValue > maxqValue:
                maxqValue = qValue
                policy = action
    #        print("policy:", policy)
        return policy
        """ END CODE """

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
