import random
import sys

sys.path.append("..")  # so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *



############################
##### NOTES ################
############################

# gene[0] - location of anthill
# gene[1] - location of tunnel
# gene[2-10] - location of grass
# gene[11 & 12] - location of enemy foods



##
# AIPlayer
# Description: The responsbility of this class is to interact with the game by
# deciding a valid move based on a given game state. This class has methods that
# will be implemented by students in Dr. Nuxoll's AI course.
#
# Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    # __init__
    # Description: Creates a new Player
    #
    # Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer, self).__init__(inputPlayerId, "Ai")
        self.population = []
        self.pop_index = 0
        self.fitness = []
        # self.const_letters = ['A', 'T', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'F', 'F']
        self.init_population(10)


    def init_population(self, size):
        self.fitness = -1 * size
        for i in range(0, size):
            gene = []
            for j in range(0, 13):
                pick = None

                while pick == None:
                    if j < (13 - 2):
                        # Choose any x location
                        x = random.randint(0, 9)
                        # Choose any y location on your side of the board
                        y = random.randint(0, 3)
                    else:
                        # Choose any x location
                        x = random.randint(0, 9)
                        # Choose any y location on your side of the board
                        y = random.randint(6, 9)
                    location = y * 10 + x + 65
                    if chr(location) not in gene:
                        pick = location

                gene.append(chr(pick))
            self.population.append(gene)
        print(self.population)

    ##
    # getPlacement
    #
    # Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    # Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    # Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        gene = self.population[self.pop_index]
        if currentState.phase == SETUP_PHASE_1:
            moves = []
            for i in range(0, 11):
                location = ord(gene[i]) - 65
                moves.append(((location % 10), int(location / 10)))
            return moves
        elif currentState.phase == SETUP_PHASE_2:
            moves = []
            for i in range(11, 13):
                location = ord(gene[i]) - 65
                moves.append(((location % 10), int(location / 10)))
            return moves
        else:
            return [(0, 0)]

        # numToPlace = 0
        # # implemented by students to return their next move
        # if currentState.phase == SETUP_PHASE_1:  # stuff on my side
        #     numToPlace = 11
        #     moves = []
        #     for i in range(0, numToPlace):
        #         move = None
        #         while move == None:
        #             # Choose any x location
        #             x = random.randint(0, 9)
        #             # Choose any y location on your side of the board
        #             y = random.randint(0, 3)
        #             # Set the move if this space is empty
        #             if currentState.board[x][y].constr == None and (x, y) not in moves:
        #                 move = (x, y)
        #                 # Just need to make the space non-empty. So I threw whatever I felt like in there.
        #                 currentState.board[x][y].constr == True
        #         moves.append(move)
        #     return moves
        # elif currentState.phase == SETUP_PHASE_2:  # stuff on foe's side
        #     numToPlace = 2
        #     moves = []
        #     for i in range(0, numToPlace):
        #         move = None
        #         while move == None:
        #             # Choose any x location
        #             x = random.randint(0, 9)
        #             # Choose any y location on enemy side of the board
        #             y = random.randint(6, 9)
        #             # Set the move if this space is empty
        #             if currentState.board[x][y].constr == None and (x, y) not in moves:
        #                 move = (x, y)
        #                 # Just need to make the space non-empty. So I threw whatever I felt like in there.
        #                 currentState.board[x][y].constr == True
        #         moves.append(move)
        #     return moves
        # else:
        #     return [(0, 0)]

    ##
    # getMove
    # Description: Gets the next move from the Player.
    #
    # Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    # Return: The Move to be made
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0, len(moves) - 1)];

        # don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0, len(moves) - 1)];

        return selectedMove

    ##
    # getAttack
    # Description: Gets the attack to be made from the Player
    #
    # Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        # Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    # registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        # method templaste, not implemented
        pass
