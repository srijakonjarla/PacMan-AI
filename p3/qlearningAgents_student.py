import featureExtractors
import learningAgents
import util, random

class QLearningAgent(learningAgents.ReinforcementAgent):
    """
    Q-Learning Agent

    Functions you should fill in:
        - getQValue
        - getAction
        - getValue
        - getPolicy
        - update

    Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discountRate (discount rate)

    Functions you should use
        - self.getLegalActions(state) which returns legal actions for a state
    """

    def __init__(self, **args):
        """
        You can initialize Q-values here...
        """

        super().__init__(**args)

        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we never seen
        a state or (state,action) tuple
        """

        """
        Description:
        Simply returned the qValues variable I initialized above.
        """

        """ YOUR CODE HERE """
        return self.qValues[(state, action)]
        """ END CODE """

    def getValue(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions. Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """

        """
        Description:
        OUt of the allowed actions I checked which QValue is largest and returned that.
        """

        """ YOUR CODE HERE """
        actions = self.getLegalActions(state)

        if not actions:
            return 0.0

        value = float("-inf")
        for action in actions:
            qValue = self.getQValue(state, action)
            if qValue > value:
                value = qValue
        return value
        """ END CODE """

    def getPolicy(self, state):
        """
        Compute the best action to take in a state. Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """

        """
        Description:
        Finds the maxQValue and returns the corresponding action. 
        Picks a random policy of there is a tie.
        """

        """ YOUR CODE HERE """
        actions = self.getLegalActions(state)

        if not actions:
            return None

        policy = None
        maxqValue = float("-inf")
        actionList = []
        for action in actions:
            qValue = self.getQValue(state, action)
            if qValue == maxqValue:
                actionList.append(action)
                policy = random.choice(actionList)
            if qValue > maxqValue:
                actionList = []
                maxqValue = qValue
                policy = action
                actionList.append(action)

        #print ("getPolicy:", policy)
        return policy
        """ END CODE """

    def getAction(self, state):
        """
        Compute the action to take in the current state. With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise. Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.

        HINT: You might want to use util.flipCoin(prob)
        HINT: To pick randomly from a list, use random.choice(list)
        """

        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None

        """
        Description:
        Randomly picks an action from allowed actions or it picks the best policy.
        """

        """ YOUR CODE HERE """
        if not legalActions:
            return None

        random1 = util.flipCoin(self.epsilon)

        if random1:
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)
        """ END CODE """
        #print ("getAction:", action)

        return action

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here

        NOTE: You should never call this function,
        it will be called on your behalf
        """

        """
        Description:
        Used textbook equation on page 844
        Q(s, a) ← Q(s, a) + α(R(s) + γ Q(s, a) − Q(s, a))
        """

        """ YOUR CODE HERE """
        newValue = self.getValue(nextState)
        discount = self.discountRate * newValue
        alpha = self.alpha
        qVal = self.getQValue(state, action)
        value = self.getValue(state)

        self.qValues[(state, action)] += alpha*(reward + discount - value)
       # self.qValues[(state, action)] = qVal + reward + discount
        """ END CODE """

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as QLearningAgent, but with different default parameters.
    """

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
                python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha - learning rate
        epsilon - exploration rate
        gamma - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """

        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0 # This is always Pacman

        super().__init__(**args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman. Do not change or remove this
        method.
        """

        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    ApproximateQLearningAgent

    You should only have to overwrite getQValue
    and update. All other QLearningAgent functions
    should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor)()
        super().__init__(**args)

        # You might want to initialize weights here.
        self.weights = util.Counter()

    def getQValue(self, state, action):
        """
        Should return Q(state,action) = w * featureVector
        where * is the dotProduct operator
        """

        """
        Description:
        Takes each feature and multiplies the value corresponded to it by the weight of the feature.
        """

        """ YOUR CODE HERE """
        feats = self.featExtractor.getFeatures(state, action)
        qValue = 0
        #print ("feats:", feats)
        for feature in feats:
            #print ("feature:", feature)
            #print ("value:", value)
            #print ("feats:", feats[(feature, value)])
            #print ("weight:", self.weights[feature])
            value = feats[feature]
            qValue += self.weights[feature] * value
        #print ("qvalue:", qValue)
        return qValue
        """ END CODE """

    def update(self, state, action, nextState, reward):
        """
        Should update your weights based on transition
        """

        """
        Description:
        Finds the weight of each feature given its state and next state. 
        """

        """ YOUR CODE HERE """
        newValue = self.getValue(nextState)
        discount = self.discountRate * newValue
        alpha = self.alpha
        qValue = self.getValue(state)
        feats = self.featExtractor.getFeatures(state, action)

        for feature in feats:
            self.weights[feature] += alpha*(reward + discount - qValue)*feats[feature]
            #print ("weight:", self.weights[feature])
        """ END CODE """

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            pass