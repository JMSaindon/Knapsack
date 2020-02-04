import numpy as np
import matplotlib.pyplot as plt

class Parameters:
    Seed = 9876
    MaxFill = 60
    NumberOfPopulations = 100
    NumberOfGenerations = 100
    PopulationSize = 50
    MutationRate = 5

    # Objects configuration
    NumberOfObjects = 40
    InfCostObjects = 20
    MaxCostObjects = 300
    InfWeightObjects = 1
    MaxWeightObjects = 6
    Objects = None

    def __init__(self):
        np.random.seed(self.Seed)
        self.Objects = GenObjects(self.NumberOfObjects, self.InfCostObjects, self.MaxCostObjects, self.InfWeightObjects, self.MaxWeightObjects)


class Object:
    def __init__(self, id, cost, weight):
        self._id = id
        self._cost = cost
        self._weight = weight

    def __str__(self):
        return "(id : " + str(self._id) + ", cost : " + str(self._cost) + ", weight : " + str(self._weight) + ")"

def GenObjects(nb_objects, infCost, maxCost, infWeight, maxWeight):
    """Génère nb_objects objets avec des coûts et des poids aléatoires"""
    objects = [Object(i, np.random.randint(infCost, maxCost), np.random.randint(infWeight, maxWeight)) for i in range(nb_objects)]
    return objects

# tests
# objects = GenObjects(20,0,100,0,100)
# print("Objects available to choose at the begining :")
# for obj in objects:
#     print(str(obj))


class Individual:
    _param = None
    _pack = None
    _sumObj = 0
    _sumWeight = 0
    _sumCost = 0

    def __init__(self, param):
        self._param = param

    def setPack(self, pack):
        self._pack = pack
        self.computeStats()
        return self

    def fillRandomly(self):
        self._pack = np.zeros(len(self._param.Objects))
        self._sumObj = 0
        self._sumWeight = 0
        self._sumCost = 0
        objectsRemaining = [i for i in range(len(self._param.Objects))]
        while(len(objectsRemaining) > 0):
            i = np.random.randint(0, len(objectsRemaining))
            if (self._sumWeight + self._param.Objects[objectsRemaining[i]]._weight < self._param.MaxFill):
                self._sumObj += 1
                self._sumWeight += self._param.Objects[objectsRemaining[i]]._weight
                self._sumCost += self._param.Objects[objectsRemaining[i]]._cost
                self._pack[objectsRemaining[i]] = 1
            del objectsRemaining[i]
        return self

    def computeStats(self):
        self._sumObj = 0
        self._sumWeight = 0
        self._sumCost = 0
        for k in range(len(self._pack)):
            if self._pack[k] == 1:
                self._sumWeight += self._param.Objects[k]._weight
                self._sumCost += self._param.Objects[k]._cost
                self._sumObj += 1

    def fit(self):
        return 0 if self._sumWeight > self._param.MaxFill else self._sumCost

    def mutate(self):
        """retourne l'individu ayant subi une mutation"""

        i = np.random.randint(0, len(self._pack))

        if self._pack[i] == 0:
            self._pack[i] = 1
            self._sumWeight += self._param.Objects[i]._weight
            self._sumCost += self._param.Objects[i]._cost
            self._sumObj += 1
        else:
            self._pack[i] = 0
            self._sumWeight -= self._param.Objects[i]._weight
            self._sumCost -= self._param.Objects[i]._cost
            self._sumObj -= 1

        self.computeStats()
        return self

    def __str__(self):
        chromosome = ""
        for k in range(len(self._param.Objects)):
            if self._pack[k] == 0:
                chromosome += "-"
            else:
                chromosome += "X"
        size = " (Size = " + str(self._sumObj) + ")"
        weight = " (Weight = " + str(self._sumWeight) + ")"
        cost = " (Cost = " + str(self._sumCost) + ")"
        return chromosome + size + weight + cost

# tests
# param = Parameters()
# individual = Individual(param).fillRandomly()
# print(str(individual))
# print(individual.fit())



class Population:
    _members = None
    _param = None

    def __init__(self, param):
        self._param = param

    def fillRandomly(self):
        self._members = [Individual(self._param).fillRandomly() for k in range(self._param.PopulationSize)]
        return self

    def reproduce(self, p1, p2):
        """retourne les 2 enfants possiblement créés avec un cross point central.
        D'autres méthodes de reproduction sont également envisageables"""

        crossPoint = len(self._param.Objects)//2
        parent1 = self._members[p1]
        parent2 = self._members[p2]
        pack1 = np.concatenate((parent1._pack[:crossPoint], parent2._pack[crossPoint:]))
        pack2 = np.concatenate((parent2._pack[:crossPoint], parent1._pack[crossPoint:]))
        child1 = Individual(self._param).setPack(pack1)
        child2 = Individual(self._param).setPack(pack2)
        return [child1, child2]

    def newGeneration(self):
        """fait évoluer la population vers la génération suivante"""

        n = len(self._members)
        fitness = np.array([self._members[k].fit() for k in range(n)])
        sumFit = sum(fitness)
        probaFit = fitness / sumFit
        popAfterReproduction = []
        OldPop = self._members.copy()
        childs = []

        while (len(OldPop) > n / 2):
            # select parent 1
            indexParent1 = np.random.choice(len(OldPop), p=probaFit)
            parent1 = OldPop[indexParent1]
            del OldPop[indexParent1]
            probaFit = np.delete(probaFit, indexParent1)
            probaFit = probaFit / sum(probaFit)
            popAfterReproduction.append(parent1)

            # select parent 2
            indexParent2 = np.random.choice(len(OldPop), p=probaFit)
            parent2 = OldPop[indexParent2]
            del OldPop[indexParent2]
            probaFit = np.delete(probaFit, indexParent2)
            probaFit = probaFit / sum(probaFit)
            popAfterReproduction.append(parent2)

            # Reproduction
            sons = self.reproduce(indexParent1, indexParent2)
            childs += sons

        # Add the population that have not participated in the reproduction
        for p in OldPop:
            popAfterReproduction.append(p)

        # Mutation phase
        for i in range(len(childs)):
            probaMutate = np.random.randint(0,100)
            if probaMutate < self._param.MutationRate:
                childs[i] = childs[i].mutate()

        popAfterReproduction += childs

        # Final selection part
        newPop = []
        fit = [popAfterReproduction[k].fit() for k in range(len(popAfterReproduction))]
        for k in range(n):
            probaMax = max(fit)
            indexMax = fit.index(probaMax)
            bestPeople = popAfterReproduction[indexMax]
            newPop.append(bestPeople)
            del fit[indexMax]
            del popAfterReproduction[indexMax]

        self._members = newPop
        return self

    def champion(self):
        """retourne l'individu ayant le meilleur coût"""
        costPop = [self._members[i]._sumCost for i in range(len(self._members))]
        costMax = max(costPop)
        indexMax = costPop.index(costMax)
        return self._members[indexMax]

    def __str__(self):
        s = ""
        for i in self._members:
            s += str(i) + "\n"
        return s


# tests
# param = Parameters()
# pop = Population(param).fillRandomly()
# sons = pop.reproduce(0,1)
# print(str(sons[0]))
# print(str(pop))
# print(str(pop.newGeneration()))

def GenerationN():
    """Retourne le champion initial d'une population et le champion final après N générations"""

    param = Parameters()
    pop = Population(param).fillRandomly()
    print("pop size :", param.PopulationSize)
    print("Init Champion  : " + str(pop.champion()))

    for k in range(param.NumberOfGenerations):
        pop.newGeneration()

    print("Final Champion : " + str(pop.champion()))

# GenerationN()

def BestPopParam(param):
    """Simule l'évolution d'un certain nombre de population sur plusieurs générations et affiche les paramètres menant à la meilleure solution"""

    stats = []
    bestParam = None
    best = None
    for k in range(param.NumberOfPopulations):
        seed = np.random.randint(0, 100000)
        param.Seed = seed
        np.random.seed(seed)
        param.PopulationSize = 20 + np.random.randint(1, 10) ** 3
        param.MutationRate = 1 + np.random.randint(1, 5) ** 2

        pop = Population(param).fillRandomly()

        for g in range(param.NumberOfGenerations):
            pop.newGeneration()

        champ = pop.champion()
        stats.append(champ._sumCost)
        if best == None:
            best = champ
            bestParam = (param.Seed, param.PopulationSize, param.MutationRate)
        else:
            if champ._sumCost > best._sumCost:
                best = champ
                bestParam = (param.Seed, param.PopulationSize, param.MutationRate)

        print(str(champ) + " (BestCost = " + str(best._sumCost) + ") " + str(k+1))

    print("\nBest solution :")
    print(str(best))
    print("Seed :", bestParam[0], ", Population size :", bestParam[1], ", Mutation rate :", bestParam[2])

    return best._sumCost, np.array(stats)

param = Parameters()
bestCost, stats = BestPopParam(param)


# # Vérification de la solution avec le module python knapsack
# # Attention execution très très longue
# import knapsack
#
# Weights = [] # équivalent de size  dans la documentation
# Costs = [] # équivalent de weight dans la documentation
# Capacity = param.MaxFill
#
# for o in param.Objects:
#     Weights.append(o._weight)
#     Costs.append(o._cost)
#
# print("\nSolution of the knapsack module :")
# bestCost = knapsack.knapsack(Weights, Costs).solve(Capacity)[0]
# print(bestCost)


# Affichage du graphique d'optimalité
ht = (stats/bestCost)*100
print("\nOptimality percentage :", np.mean(ht))
plt.bar(x=range(param.NumberOfPopulations), height=ht)
plt.xlabel('Populations générées aléatoirement')
plt.ylabel("Pourcentage d'optimalité de la population")
plt.title("Pourcentage d'optimalité des populations après " + str(param.NumberOfGenerations) + " générations et sur " + str(param.NumberOfPopulations) + " simulations")
plt.show()
