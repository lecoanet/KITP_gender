
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import Generator, PCG64

max_authors = 6
num_papers = 18

num_authors =  np.array([4, 2, 3, 2, 2, 2, 5, 5, 2, 4, 6, 2, 1, 3, 1, 1, 3, 1])
first_author = np.array([1, 0, 0,-1,-1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1])
num_male =     np.array([4, 1, 1, 0, 1, 1, 3, 5, 2, 4, 4, 2, 0, 3, 1, 1, 3, 1])

order = np.argsort(-num_authors)
num_authors = num_authors[order]
first_author = first_author[order]
num_male = num_male[order]
num_coauthor_male = np.copy(num_male)
num_coauthor_male[first_author==1] -= 1

rng = Generator(PCG64(42))

num_realizations = 10000

all_male_list = []
all_female_list = []

for n in range(num_realizations):
    all_male = 0
    all_female = 0
    for i in range(num_papers):
        # right (null)
        extra_authors = num_authors[i] - 1
        if first_author[i] == 1:
            n_male = 1
        else:
            n_male = 0
        if extra_authors > 0:
            nums = rng.uniform(size=extra_authors)
            extra_male = np.sum(nums > 17/45)
            n_male += extra_male
    
        if n_male == num_authors[i] or (first_author[i] == 0 and n_male == num_authors[i]-1):
            all_male += 1
        elif n_male == 0:
            all_female += 1
    all_male_list.append(all_male)
    all_female_list.append(all_female)

all_male = np.array(all_male_list)
all_female = np.array(all_female_list)

print(np.mean(all_male))
print(np.mean(all_female))
print(1 + 17/45*3 + (17/45)**2)

for i in range(3, 15):
    print(i, np.sum(all_male==i)/num_realizations)

for i in range(1, 6):
    print(i, np.sum(all_female==i)/num_realizations)

