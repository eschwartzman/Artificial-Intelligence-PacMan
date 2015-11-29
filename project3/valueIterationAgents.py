# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
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
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.V_values = util.Counter() # A Counter is a dict with default 0
    self.Q_values = util.Counter()
    self.best_action = util.Counter()
    "*** YOUR CODE HERE ***"
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    for states in self.mdp.getStates():
      self.V_values[states] = 0

    for steps in range (0, self.iterations):
      temp = self.V_values.copy()
      for states in self.V_values:
        sum_over_states = -float("inf")
        for action in self.mdp.getPossibleActions(states):
          value = 0
          for transition in self.mdp.getTransitionStatesAndProbs(states, action):
            value += (transition[1]* (self.mdp.getReward(states, action, transition[0])+(self.discount*temp[transition[0]]) ) )
          if sum_over_states < value:
            sum_over_states = value
            self.best_action[states] = action
        if (sum_over_states != -float("inf")):
          self.V_values[states] = sum_over_states
    return self.V_values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"

    for states in self.mdp.getStates():
      for actions in self.mdp.getPossibleActions(states):
        self.Q_values[(states, actions)] = 0

    temp = self.V_values.copy()
    for states, actions in self.Q_values:
      value = 0
      for transition in self.mdp.getTransitionStatesAndProbs(states, actions):
        value += (transition[1] * (self.mdp.getReward(states, actions, transition[0])+(self.discount*temp[transition[0]])))
      self.Q_values[states, actions] = value
    return self.Q_values[state, action]

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    if self.mdp.isTerminal(state) == True:
      return None
    return self.best_action[state]

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
