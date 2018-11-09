import random
import sys
import os
sys.path.append("..")  # so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *

##############################
#
# Author: Mikayla Whiteaker
# Author: Chris Lytle
#
# Version: November 2018
#
##############################

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
        super(AIPlayer, self).__init__(inputPlayerId, "Natural Selection")
        self.population = []  # List of genes to test
        self.pop_index = 0  # Index of current population
        self.fitness = []  # list of fitness scores for each population
        self.moves = 0  # number of moves per game
        self.booger_const = [(9,9), (9-5, 9-1),
                    (9-0,9-3), (9-1,9-2), (9-2,9-1), (9-3,9-0), \
                    (9-0,9-2), (9-1,9-1), (9-2,9-0), \
                    (9-0,9-1), (9-1,9-0) ]  # Locations of boogers
        self.games_per_gene = 10
        self.fitness_list_per_gene = []
        self.currentState = []
        self.size = 500
        self.init_population(self.size)


    ##
    # init_population
    #
    # Description:
    # This function initializes the agents gene population with random genes
    # the size of the population is defined by the size parameter
    #
    # Parameter:
    #   size - the number of genes in a population
    #
    def init_population(self, size):
        self.fitness = [0] * size  # Set all fitness scores to 0
        self.currentState = [None] * size
        for i in range(0, size):
            gene = []
            for j in range(0, 13):
                pick = None
                # Choose random location while
                while pick is None:
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
                    # If location not in gene already and not on booger's construct
                    if chr(location) not in gene and (x, y) not in self.booger_const:
                        pick = location
                gene.append(chr(pick))
            self.population.append(gene)

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
        self.moves = 0  # reset move counter to 0
        gene = self.population[self.pop_index]
        if currentState.phase == SETUP_PHASE_1:
            moves = []
            for i in range(0, 11):
                location = ord(gene[i]) - 65
                moves.append(((location % 10), int(location / 10)))  # Convert gene to locations
            return moves
        elif currentState.phase == SETUP_PHASE_2:
            moves = []
            for i in range(11, 13):
                location = ord(gene[i]) - 65  # convert gene to locations
                x = location % 10
                y = int(location / 10)
                # print((x, y))
                if currentState.board[x][y].constr is None:
                    move = (x, y)
                    moves.append(move)
            return moves
        else:
            return [(0, 0)]

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
        self.currentState[self.pop_index] = currentState
        self.moves += 1
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0, len(moves) - 1)]
        # don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0, len(moves) - 1)]
        return selectedMove

    ##
    # mating
    #
    # Description:
    # Mates two parents with each other, then creates two different child genes.
    # It then applies random mutations to the child genes.  Then returns the
    # two children.
    #
    # Parameters:
    #   parent1 - gene with best fitness score
    #   parent2 - gene with second best fitness score
    # Return:
    #   [child1 child2]
    #
    def mating(self, parent1, parent2):
        # Create two child genes
        child1 = []
        child2 = []

        # Crossover
        cross = random.randint(1, 13)
        child1.extend(parent1[:cross])
        child1.extend(parent2[cross:])
        child2.extend(parent2[:cross])
        child2.extend(parent1[cross:])

        # Apply mutations
        self.mutate_gene(child1)
        self.mutate_gene(child2)

        return [child1, child2]

    ##
    # create mutation
    #
    # Description:
    #   creates a change on a gene to slitly change its value
    #
    # Parameter:
    #   gene_char - char character from gene
    #
    # Returns:
    #   modified char charicter
    def create_mutation(self, gene_char):
        location = ord(gene_char) - 65
        x = (location % 10) + random.randint(-1, 1)
        y = int(location / 10) + random.randint(-1, 1)
        return chr(y * 10 + x + 65)

    ##
    # mutate gene
    #
    # Description:
    #
    # Parameter:
    #
    # Returns:
    #
    def mutate_gene(self, gene):
        rtrnGene = []
        mutationChance = 40
        for i in range(0, 13):
            ranMutation = random.randint(0, 100)  # random number to decide mutation
            if mutationChance < ranMutation:
                if i < (13 - 2):
                    tempGene = self.create_mutation(gene[i])
                    location = ord(tempGene) - 65
                    x = (location % 10)
                    y = int(location / 10)
                    if legalCoord((x, y)) and y <= 3:
                        rtrnGene.append(tempGene)
                    else:
                        rtrnGene.append(gene[i])
                else:
                    tempGene = self.create_mutation(gene[i])
                    location = ord(tempGene) - 65
                    x = (location % 10)
                    y = int(location / 10)
                    if (x, y) not in self.booger_const and legalCoord((x, y)) and y >= 6:
                        rtrnGene.append(tempGene)
                    else:
                        rtrnGene.append(gene[i])
            else:
                rtrnGene.append(gene[i])

        return rtrnGene

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
    # eval fitness
    #
    # Description: This function determines the fitness of the current gene
    #
    # Parameter:
    #   hasWon - has this player one
    #
    def eval_fitness(self, hasWon):
        fitness = self.moves / 400  # the number of moves divided by 400
        if hasWon:
            fitness += 1  # add 1 if won
        else:
            fitness -= 1  # subtract 1 if lost
        self.fitness_list_per_gene.append(fitness)  # add to fitness list per gene

    ##
    # create new pop
    #
    # Description: This method creates a new population and resets everything else
    #
    def create_new_pop(self):
        new_pop = []
        sorted_fitness = list(reversed(sorted(self.fitness)))
        for i in range(0, int(self.size/2)):
            i1 = self.fitness.index(sorted_fitness[i*2])
            i2 = self.fitness.index(sorted_fitness[i*2+1])
            new_pop.extend(self.mating(self.population[i1], self.population[i2]))
        for gene in new_pop:
            while not self.valid_gene(gene):
                for i in range(0, 11):
                    if gene.count(gene[i]) > 1:  # If duplicate characters, return false
                        pick = None
                        while pick is None:
                            # Choose any x location
                            x = random.randint(0, 9)
                            # Choose any y location on your side of the board
                            y = random.randint(0, 3)
                            location = y * 10 + x + 65
                            if chr(location) not in gene:
                                pick = location
                                gene[i] = chr(pick)
                for n in range(11, 13):
                    location = ord(gene[n]) - 65
                    x = location % 10
                    y = int(location / 10)
                    # Check if valid food placement based on enemy constructs
                    if (x, y) in self.booger_const or gene.count(gene[n]) > 1:
                        pick = None
                        while pick is None:
                            # Choose any x location
                            new_x = random.randint(0, 9)
                            # Choose any y location on your side of the board
                            new_y = random.randint(6, 9)
                            new_location = new_y * 10 + new_x + 65
                            if chr(new_location) not in gene and (new_x,new_y) not in self.booger_const:
                                pick = new_location
                                gene[n] = chr(pick)

        self.population = new_pop
        self.fitness = [0] * len(self.fitness)

    ##
    # registerWin
    #
    # This agent learns from the past games
    #
    def registerWin(self, hasWon):
        # 1. update the fitness of the current gene
        self.eval_fitness(hasWon)
        # 2. Judge whether the current gene's fitness has been fully evaluated. If so, advance to
        # the next gene.
        if len(self.fitness_list_per_gene) < self.games_per_gene:  # If gene hasn't been evaluated enough
            pass  # Play again with same gene
        elif self.pop_index + 1 == len(self.population):  # If at the end of the population size
            self.print_fitest()
            self.fitness[self.pop_index] = sum(self.fitness_list_per_gene) / len(self.fitness_list_per_gene)
            self.create_new_pop()  # create a new one
            self.pop_index = 0  # reset pop index
            self.fitness_list_per_gene.clear()  # clear fitness list per gene and go to next gene
        else:  # if played all games for one gene, find the average of all fitness scores for that gene
            self.fitness[self.pop_index] = sum(self.fitness_list_per_gene) / len(self.fitness_list_per_gene)
            self.pop_index += 1
            self.fitness_list_per_gene.clear()  # clear fitness list per gene and go to next gene

    ##
    # valid gene
    #
    # Description: checks if the given gene is valid in the context of the current state
    #
    # Parameter:
    #   gene - the gene to be evaluated
    #
    # Returns:
    #   true - if valid
    #   false - id not valid
    #
    def valid_gene(self, gene):
        for i in range(0, 13):
            if gene.count(gene[i]) > 1:  # If duplicate characters, return false
                return False
        for n in range(11, 13):
            location = ord(gene[n]) - 65
            x = location % 10
            y = int(location / 10)
            if not legalCoord((x, y)):  # If coordinates invalid, false
                return False
            if (x, y) in self.booger_const:  # If coordinates on (X, Y)
                return False
        return True


    def print_fitest(self):
        orig_stdout = sys.stdout
        # print("what")

        filename = 'fittest.txt'
        if os.path.exists(filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        file = open(filename, append_write)
        sys.stdout = file
        index = self.fitness.index(max(self.fitness))
        asciiPrintState(self.currentState[index])
        file.write("\n\n")
        sys.stdout = orig_stdout
        file.close()
