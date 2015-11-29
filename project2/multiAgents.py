# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    distance_to_food = []

    for food in newFood.asList():
      distance_to_food.append( (abs(newPos[0] - food[0]) + abs(newPos[1] - food[1]) ) )

    if len(distance_to_food) != 0:
      return ( (successorGameState.getScore() ) - (.5*min(distance_to_food) ) )
    else:
      return ( successorGameState.getScore() )

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)
    self.next_action= Directions.STOP

  "*** YOUR CODE HERE ***"
  def turnValue(self, gameState, turn):
    if (turn == self.depth * gameState.getNumAgents() or len(gameState.getLegalActions(0)) == 0):
      return self.evaluationFunction(gameState)
    agentIndex = turn%gameState.getNumAgents()
    if (agentIndex == 0):
      return self.maxValue(gameState, turn)
    else:
      return self.minValue(gameState, turn)

  def maxValue(self, gameState, turn):
    value = -float("inf")
    agentIndex = turn%gameState.getNumAgents()
    for action in gameState.getLegalActions(agentIndex):
      if action != Directions.STOP:
        successor = gameState.generateSuccessor(agentIndex, action)
        if (value < self.turnValue(successor, turn+1)):
          value = self.turnValue(successor, turn+1)
          if (turn == 0):
            self.next_action = action
    return value

  def minValue(self, gameState, turn):
    value = float("inf")
    agentIndex = turn%gameState.getNumAgents()
    for action in gameState.getLegalActions(agentIndex):
      if action != Directions.STOP:
        successor = gameState.generateSuccessor(agentIndex, action)
        value = min(value, self.turnValue(successor, turn+1))
    return value

  def turnValueAlpha(self, gameState, turn, alpha, beta):
    if (turn == self.depth * gameState.getNumAgents() or len(gameState.getLegalActions(0)) == 0):
      return self.evaluationFunction(gameState)
    agentIndex = turn%gameState.getNumAgents()
    if (agentIndex == 0):
      return self.maxValueAlpha(gameState, turn, alpha, beta)
    else:
      return self.minValueAlpha(gameState, turn, alpha, beta)

  def maxValueAlpha(self, gameState, turn, alpha, beta):
    value = -float("inf")
    agentIndex = turn%gameState.getNumAgents()
    for action in gameState.getLegalActions(agentIndex):
      if action != Directions.STOP:
        successor = gameState.generateSuccessor(agentIndex, action)
        if (value < self.turnValueAlpha(successor, turn+1, alpha, beta)):
          value = self.turnValueAlpha(successor, turn+1, alpha, beta)
          if (turn == 0):
            self.next_action = action
          if value >= beta:
            return value
          alpha = max(alpha, value)
    return value

  def minValueAlpha(self, gameState, turn, alpha, beta):
    value = float("inf")
    agentIndex = turn%gameState.getNumAgents()
    for action in gameState.getLegalActions(agentIndex):
      if action != Directions.STOP:
        successor = gameState.generateSuccessor(agentIndex, action)
        value = min(value, self.turnValueAlpha(successor, turn+1, alpha, beta))
        if value <= alpha:
          return value
        beta = min(beta,value)
    return value

  def turnValueExp(self, gameState, turn):
    if (turn == self.depth * gameState.getNumAgents() or len(gameState.getLegalActions(0)) == 0):
      return self.evaluationFunction(gameState)
    agentIndex = turn%gameState.getNumAgents()
    if (agentIndex == 0):
      return self.maxValueExp(gameState, turn)
    else:
      return self.expValue(gameState, turn)

  def maxValueExp(self, gameState, turn):
    value = -float("inf")
    agentIndex = turn%gameState.getNumAgents()
    for action in gameState.getLegalActions(agentIndex):
      if action != Directions.STOP:
        successor = gameState.generateSuccessor(agentIndex, action)
        if (value < self.turnValueExp(successor, turn+1)):
          value = self.turnValueExp(successor, turn+1)
          if (turn == 0):
            self.next_action = action
    return value

  def expValue(self, gameState, turn):
    value = 0
    agentIndex = turn%gameState.getNumAgents()
    for action in gameState.getLegalActions(agentIndex):
      if action != Directions.STOP:
        successor = gameState.generateSuccessor(agentIndex, action)
        p = 1.0 / len(gameState.getLegalActions(agentIndex))
        value += (p * self.turnValueExp(successor, turn+1))
    return value

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    self.turnValue(gameState, 0)
    return self.next_action


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    alpha = -float("inf")
    beta = float("inf")
    self.turnValueAlpha(gameState, 0, alpha, beta)
    return self.next_action

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    self.turnValueExp(gameState, 0)
    return self.next_action

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: As per the hints and suggestions, we chained together features we thought were important,
                 such as Pac-man's distance to ghosts, capsules, etc. We then weighted some of these according to how important
                 we thought the feature was, with the exact values coming from guess and check.
                 We also followed question 1 as a model.
  """
  "*** YOUR CODE HERE ***"
  pos = currentGameState.getPacmanPosition()
  food = currentGameState.getFood()
  capsules = currentGameState.getCapsules()
  scaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
  ghostPos = currentGameState.getGhostPositions()

  distance_to_food = []
  distance_to_capsules = []
  distance_to_ghost = []

  for foods in food.asList():
    distance_to_food.append( (abs(pos[0] - foods[0]) + abs(pos[1] - foods[1]) ) )

  for cap in capsules:
    distance_to_capsules.append( (abs(pos[0] - cap[0]) + abs(pos[1] - cap[1]) ) )

  for ghost in ghostPos:
    distance_to_ghost.append( (abs(pos[0] - ghost[0]) + abs(pos[1] - ghost[1]) ) )

  if len(distance_to_food) != 0 and len(distance_to_capsules) !=0 and len(distance_to_ghost) != 0:
    return (
               (.9*currentGameState.getScore() )
             - (.4*min(distance_to_food) )
             - (2.3*min(distance_to_capsules) )
             - (3.8*min(distance_to_ghost) )
           )
  else:
    return ( (.97*currentGameState.getScore() ) - (min(scaredTimes) ) )

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

