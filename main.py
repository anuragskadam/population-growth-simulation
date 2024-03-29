import random
import csv
import copy
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import *





LIST_SPECIES = ['Grass', 'Trees', 'Birds', 'Bugs', 'Tigers', 'Bears', 'Chicken', 'Buffaloes']
LIST_ATTRIBUTES = [[], []]


INITIAL_GENE_STATE = [[] for _ in LIST_SPECIES]
INITIAL_POPULATIONS = []

MUTATION_K = 10
MUTATION_PROB = 1 / MUTATION_K
MUTATION_AMP = 1


ALL_ORGANISMS = [[] for _ in LIST_SPECIES]


EATING_MATRIX = [[0, 0, 1, 1, 0, 1, 1, 1],
                 [0, 0, 0, 0, 0, 1, 0, 1],
                 [0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 1, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0]]



NO_OF_STEPS = 30
NO_OF_SIMULATIONS = 20



STEP_COUNTER = 0
SIMU_COUNTER = 0

MAKE_TOTAL_LIST_BOOL = 0

###

RESULT_ALL_ORGS = []

###

###

def sigmoid(x):
    return 1/(1 + np.exp(-x))


def list_printer(list_in, n_t='\t'):
    print('[', end='')
    for i in list_in:
        print(i, end=n_t)
    print(']')

###


def world_creator():

    with open('initial_states.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)
        counter = 0
        for line in csv_reader:

            if line[0] != 'permanent_attributes':
                LIST_ATTRIBUTES[counter].append(line[0])
                line.pop(0)
                for i, _ in enumerate(LIST_SPECIES):
                    INITIAL_GENE_STATE[i].append(int(line[i]))
            else:
                counter = 1

    INITIAL_POPULATIONS = [i[-1] for i in INITIAL_GENE_STATE]

    for species_no, population in enumerate(INITIAL_POPULATIONS):
        for _ in range(population):
            ALL_ORGANISMS[species_no].append(INITIAL_GENE_STATE[species_no])


world_creator()

NO_OF_SPECIES = len(LIST_SPECIES)
NO_OF_GENES = len(LIST_ATTRIBUTES[0])
NO_OF_PERMANENT_ATT = len(LIST_ATTRIBUTES[1])
NO_OF_TOT_ATT = NO_OF_GENES+NO_OF_PERMANENT_ATT

ALL_ORGANISMS_PERMANENT_COPY = copy.deepcopy(ALL_ORGANISMS)


def reproduction(popu):
    sex_rep = INITIAL_GENE_STATE[popu][-5]

    if sex_rep:
        couple = random.choices(ALL_ORGANISMS[popu], k=2)
        org1 = np.array(couple[0])
        org2 = np.array(couple[1])
        kid = list(np.add(org1, org2)/2)
        kid[-2] = 0
        return [kid for _ in range(int(INITIAL_GENE_STATE[popu][6]))]
    else:
        kid = random.choice(ALL_ORGANISMS[popu])
        kid[-2] = 0
        return [kid for _ in range(int(INITIAL_GENE_STATE[popu][6]))]


def mutator(a):
    out_list = []
    for i in a:
        while(1):
            random_int = random.randint(0, NO_OF_GENES-1)

            if i[random_int] != -1:

                mutation_val = MUTATION_AMP * \
                    random.choices([0, 1], k=1, weights=[MUTATION_K, 1])[0] * \
                    random.choices([-1, 1], k=1)[0]

                kiddy = i.copy()
                kiddy[random_int] += mutation_val
                out_list.append(kiddy)
                break

    return out_list


def eating(preda, pre):

    predator = ALL_ORGANISMS[preda]
    prey = ALL_ORGANISMS[pre]
    eating_coef = 1/15

    if prey and predator:
        eater = random.choice(predator)
        eatee = random.choice(prey)

        random.shuffle(ALL_ORGANISMS[pre])

        for _ in range(int((eater[-6]/80) * (eater[9]/eatee[9]) * len(prey) * eating_coef)):

            # prey-predator variables

            eatee = ALL_ORGANISMS[preda][0]
            e_factor = sigmoid(
                len(prey)) * sigmoid((eatee[1] - eater[1])) * sigmoid(eatee[0]) * sigmoid(eatee[2])

            if e_factor > 0.7:
                eatened = ALL_ORGANISMS[preda].pop(0)
                eater[-6] -= 10 * eatened[9]/eater[9]


def death():
    for n, i in enumerate(ALL_ORGANISMS):
        for j, k in enumerate(i):
            if k[-6] > 65 or k[-2] > k[-4]*100:
                # if n == 0 and j % 10 == 0:
                #     print(k[-2], LIST_SPECIES[n])
                ALL_ORGANISMS[n].pop(j)


def step():
    global STEP_COUNTER

    # reproduce and mutate

    repro_list_length = 5

    for n, popu in enumerate(ALL_ORGANISMS):
        species_kids = []
        for _ in range(repro_list_length):
            if popu and random.random() * 80 < popu[0][7]:
                species_kids += mutator(reproduction(n))

        ALL_ORGANISMS[n] += species_kids

    # eat

    if not STEP_COUNTER % 3:
        for predator, _ in enumerate(LIST_SPECIES):
            for prey, _ in enumerate(LIST_SPECIES):
                if EATING_MATRIX[prey][predator] == 1:
                    eating(predator, prey)

    # increase hunger

    for n, i in enumerate(ALL_ORGANISMS):
        if INITIAL_GENE_STATE[n][-6] != -1:
            for j in i:
                j[-6] -= 3

    # death
        death()

    for n, i in enumerate(ALL_ORGANISMS):
        for m, j in enumerate(i):
            ALL_ORGANISMS[n][m][-2] += 1
    STEP_COUNTER += 1


def main():
    global STEP_COUNTER, ALL_ORGANISMS

    for num in range(NO_OF_SIMULATIONS):
        simu_list = [[ALL_ORGANISMS]]
        print("Simulation no. = ", (num + 1), f'/{NO_OF_SIMULATIONS}')
        for n in range(NO_OF_STEPS):
            step()

            if MAKE_TOTAL_LIST_BOOL == 1:
                simu_list.append(ALL_ORGANISMS)
            print(f"\rStep no. = {n}/{NO_OF_STEPS}", end='')
        list_printer([len(i) for i in ALL_ORGANISMS])

        RESULT_ALL_ORGS.append([len(i) for i in ALL_ORGANISMS])

        STEP_COUNTER = 0
        ALL_ORGANISMS = copy.deepcopy(ALL_ORGANISMS_PERMANENT_COPY)


list_printer([len(i) for i in ALL_ORGANISMS])

main()



# plotter

while(1):
    a = int(input('Give input for no. of bins in histogram, else press 0 to end ->'))
    if a != 0:
        BINS = a
        n = int(8)
        for i in range(n):
            plt.figure(i)
            dataa = RESULT_ALL_ORGS[i]
            (mu, sigma) = norm.fit(dataa)
            x = np.linspace(min(dataa), max(dataa), BINS)
            y = norm.pdf(x, mu, sigma)
            l = plt.plot(x, y, 'r--', linewidth=2)
            plt.hist(dataa, bins=BINS, density=True, edgecolor='black')
            plt.title(LIST_SPECIES[i] +
                      "\nμ = {0:.2f}  σ = {1:.2f}".format(mu, sigma))
            plt.xlabel("Final Population")
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.tight_layout()
        plt.show()
    else:
        break

# with open(f"plotter_{NO_OF_STEPS}_{NO_OF_SIMULATIONS}.pickle", 'wb') as picky:
#     pickle.dump(RESULT_ALL_ORGS, picky)



