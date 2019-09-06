######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
    """
    Description:
    I was playing around with the Noise and increased and decreased it to see what the
    effects were on the grid. I found that 0.0 gave me the results I want.
    """

    answerDiscount = 0.9
    answerNoise = 0.2

    """ YOUR CODE HERE """
    answerNoise = 0.0

    """ END CODE """

    return answerDiscount, answerNoise

def question3a():
    """
    Description:
    I played around with the living reward and found that increasing it made it go
    to the terminal state with reward "10". So decreasing it slowly gave me the results
    I wanted. -2.0 was also the min reward on the path to +1.0.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """
    answerLivingReward = -2.0

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    """
    Description:
    I found that reducing the discount made the rewards a lot smaller and the optimal
    policy be towards the closest positive reward.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """
    answerDiscount = 0.3

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    """
    Description:
    I found this answer while I was looking for 3a. Also, the probability of going down is less
    than going up. So, I had to make the reward just negative enough but not too much to go to the
    nearest exit.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """
    answerLivingReward = -1.0
    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    """
    Description:
    The default parameter values solves this problem already.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    """
    Description:
    I found that making the reward a large positive number made the optimal policy to go up always
    because its probability is higher.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """
    answerLivingReward = 2.0
    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerEpsilon = None
    answerLearningRate = None

    """ YOUR CODE HERE """

    """ END CODE """

    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
