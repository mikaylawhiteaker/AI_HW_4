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
        super(AIPlayer, self).__init__(inputPlayerId, "Ai")
        self.population = []
        self.pop_index = 0
        self.fitness = []
        # self.const_letters = ['A', 'T', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'F', 'F']
        self.init_population(10)
        self.moves = 0

    ##
    # init_population
    #
    # This function initializes the agents gene population with random genes
    # the size of the population is defined by the size parameter
    #
    def init_population(self, size):
        self.fitness = [-1] * size
        for i in range(0, size):
            gene = []
            for j in range(0, 13):
                pick = None
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
        self.moves = 0
        gene = self.population[self.pop_index]
        if currentState.phase == SETUP_PHASE_1:
            moves = []
            for i in range(0, 11):
                location = ord(gene[i]) - 65
                moves.append(((location % 10), int(location / 10)))
            return moves
        elif currentState.phase == SETUP_PHASE_2:
            while not self.valid_gene(currentState, gene):
                for n in range(11, 13):
                    pick = None
                    while pick is None:
                        # Choose any x location
                        x = random.randint(0, 9)
                        # Choose any y location on your side of the board
                        y = random.randint(6, 9)
                        location = y * 10 + x + 65
                        if chr(location) not in gene:
                            pick = location
                            gene[n] = chr(pick)
            moves = []
            for i in range(11, 13):
                location = ord(gene[i]) - 65
                x = location % 10
                y = int(location / 10)
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
        self.moves += 1
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0, len(moves) - 1)]

        # don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0, len(moves) - 1)]

        return selectedMove

    #
    #
    #
    #
    #
    ##
    def mating(self, parent1, parent2):
        # Create two child genes
        child1 = []
        child2 = []

        # Set mutation chance, percent out of 100
        mutationChance = 40  # percent

        # TODO: use this code below to make the mating faster
        '''
        # Should not have to worry about bad placements for first 7 elements
        child1.append(parent1[0:7])
        child2.append(parent2[0:7])    
        
        '''
        # Crossover
        for j in range(0, 13):
            ranMutation = random.randint(0, 100)  # random chance of Mutation
            if j <= 6:
                # Should not have to worry about bad placements for first 7 elements
                if mutationChance > ranMutation:
                    child1.append(self.create_mutation(parent1[j]))
                    child2.append(self.create_mutation(parent2[j]))
                else:
                    child1.append(parent1[j])
                    child2.append(parent2[j])
            else:
                if parent2 not in child1:
                    if mutationChance > ranMutation:
                        child1.append(self.create_mutation(parent2[j]))
                        child2.append(self.create_mutation(parent1[j]))
                    else:
                        child1.append(parent2[j])
                        child2.append(parent1[j])
                else:
                    if mutationChance > ranMutation:
                        child1.append(self.create_mutation(parent1[j]))
                        child2.append(self.create_mutation(parent2[j]))
                    else:
                        child1.append(parent1[j])
                        child2.append(parent2[j])

        print("=====Mating of two genes=====")
        # print("test: " + self.print_gene(parent1))
        print("P1: " + str(parent1))
        print("P2: " + str(parent2))
        print("C1: " + str(child1))
        print("C2: " + str(child2))

        pass

    def create_mutation(self, gene_char):
        print("mutation")
        location = ord(gene_char) - 65
        x = (location % 10) + random.randint(-1, 1)
        y = int(location / 10) + random.randint(-1, 1)
        return chr(y * 10 + x + 65)







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
    # eval_fitness
    #
    # This function determines the fitness of the current gene
    #
    def eval_fitness(self, hasWon):
        # gene = self.population[self.pop_index]
        # fitness = self.fitness[self.pop_index]
        # if len(set(gene)) == len(gene):
        #     fitness += 1
        # else:
        #     fitness -= 10
        # TODO: should we count the number of moves it took.  the more turns, the better the gene is theoretically.
        if hasWon:
            self.fitness[self.pop_index] += 1
        else:
            self.fitness[self.pop_index] -= 1

    ##
    # registerWin
    #
    # This agent learns from the past games
    #
    def registerWin(self, hasWon):
        # 1. update the fitness of the current gene
        self.eval_fitness(hasWon)
        # 2. Judge whether the current gene's fitness has been fully evaluated. If so, advance to
        # the next gene. ????
        # TODO: go to next gene to evaluate for next game. If at end of stack then generate two new genes based on fitness
        #
        if self.pop_index + 1 == len(self.population):
            # self.create_new_pop()
            self.pop_index = 0
        else:
            self.pop_index += 1
        print("=====Fitness Scores Round " + str(self.pop_index) + "=====")
        print(self.fitness)
        print(self.print_gene(self.population[self.pop_index]))
        self.mating(self.population[0], self.population[1])
        # TODO: Print out highest fitness score using asciiPrintState(state)
        # TODO: Output piped to file

    ##
    # valid_gene
    #
    # checks if the given gene is valid in the context of the current state
    #
    #
    def valid_gene(self, currentState, gene):
        for i in range(0, 13):
            if gene.count(gene[i]) > 1:  # If duplicate characters, return false
                return False
        for n in range(11, 13):
            location = ord(gene[n]) - 65
            x = location % 10
            y = int(location / 10)
            # Check if valid food placement based on enemy constructs
            if currentState.board[x][y].constr is not None:
                return False
        return True

    # Writes to an output file.
    def print_gene(self, gene):
        file = open('output.txt', 'w')
        print("=====Gene=====")
        file.write("=====Gene=====")
        file.write("\n")
        print("original gene: " + str(gene))
        file.write("original gene: " + str(gene))
        file.write("\n")
        anthill = ord(gene[0]) - 65
        print("Anthill: [" + str(anthill % 10) + ", " + str(int(anthill / 10)) + "]")
        file.write("Anthill: [" + str(anthill % 10) + ", " + str(int(anthill / 10)) + "]")
        file.write("\n")
        tunnel = ord(gene[1]) - 65
        print("Tunnel: [" + str(tunnel % 10) + ", " + str(int(tunnel / 10)) + "]")
        file.write("Tunnel: [" + str(tunnel % 10) + ", " + str(int(tunnel / 10)) + "]")
        file.write("\n")
        grass1 = ord(gene[2]) - 65
        print("grass 1: [" + str(grass1 % 10) + ", " + str(int(grass1 / 10)) + "]")
        file.write("grass 1: [" + str(grass1 % 10) + ", " + str(int(grass1 / 10)) + "]")
        file.write("\n")
        grass2 = ord(gene[3]) - 65
        print("grass 2: [" + str(grass2 % 10) + ", " + str(int(grass2 / 10)) + "]")
        file.write("grass 2: [" + str(grass2 % 10) + ", " + str(int(grass2 / 10)) + "]")
        file.write("\n")
        grass3 = ord(gene[4]) - 65
        print("grass 3: [" + str(grass3 % 10) + ", " + str(int(grass3 / 10)) + "]")
        file.write("grass 3: [" + str(grass3 % 10) + ", " + str(int(grass3 / 10)) + "]")
        file.write("\n")
        grass4 = ord(gene[5]) - 65
        print("grass 4: [" + str(grass4 % 10) + ", " + str(int(grass4 / 10)) + "]")
        file.write("grass 4: [" + str(grass4 % 10) + ", " + str(int(grass4 / 10)) + "]")
        file.write("\n")
        grass5 = ord(gene[6]) - 65
        print("grass 5: [" + str(grass5 % 10) + ", " + str(int(grass5 / 10)) + "]")
        file.write("grass 5: [" + str(grass5 % 10) + ", " + str(int(grass5 / 10)) + "]")
        file.write("\n")
        grass6 = ord(gene[7]) - 65
        print("grass 6: [" + str(grass6 % 10) + ", " + str(int(grass6 / 10)) + "]")
        file.write("grass 6: [" + str(grass6 % 10) + ", " + str(int(grass6 / 10)) + "]")
        file.write("\n")
        grass7 = ord(gene[8]) - 65
        print("grass 7: [" + str(grass7 % 10) + ", " + str(int(grass7 / 10)) + "]")
        file.write("grass 7: [" + str(grass7 % 10) + ", " + str(int(grass7 / 10)) + "]")
        file.write("\n")
        grass8 = ord(gene[9]) - 65
        print("grass 8: [" + str(grass8 % 10) + ", " + str(int(grass8 / 10)) + "]")
        file.write("grass 8: [" + str(grass8 % 10) + ", " + str(int(grass8 / 10)) + "]")
        file.write("\n")
        grass9 = ord(gene[10]) - 65
        print("grass 9: [" + str(grass9 % 10) + ", " + str(int(grass9 / 10)) + "]")
        file.write("grass 9: [" + str(grass9 % 10) + ", " + str(int(grass9 / 10)) + "]")
        file.write("\n")
        food1 = ord(gene[11]) - 65
        print("food 1: [" + str(food1 % 10) + ", " + str(int(food1 / 10)) + "]")
        file.write("food 1: [" + str(food1 % 10) + ", " + str(int(food1 / 10)) + "]")
        file.write("\n")
        food2 = ord(gene[12]) - 65
        print("food 2: [" + str(food2 % 10) + ", " + str(int(food2 / 10)) + "]")
        file.write("food 2: [" + str(food2 % 10) + ", " + str(int(food2 / 10)) + "]")
        file.write("\n")



