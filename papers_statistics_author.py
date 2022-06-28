
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import Generator, PCG64

num_authors =  np.array([4, 1, 2, 2, 2, 2, 5, 5, 2, 4, 6, 2, 1, 3, 1, 1, 3, 1])
num_papers = len(num_authors)

rng = Generator(PCG64(42))

num_realizations = 10000

all_male_list = []
all_female_list = []

for n in range(num_realizations):
    all_male = 0
    all_female = 0
    for i in range(num_papers):
        authors = num_authors[i]
        nums = rng.uniform(size=authors)
        num_male = np.sum(nums > 17/45)

        if num_male == authors:
            all_male += 1
        if num_male == 0:
            all_female += 1

    all_male_list.append(all_male)
    all_female_list.append(all_female)

all_male = np.array(all_male_list)
all_female = np.array(all_female_list)

print(np.mean(all_male))
print(np.mean(all_female))

for i in range(0, 18):
    print(i, np.sum(all_male==i)/num_realizations)

for i in range(0, 15):
    print(i, np.sum(all_female==i)/num_realizations)

