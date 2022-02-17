from bst import from_array
import numpy as np
import cProfile

def gen_dataset():
    dataset = []
    x = 100
    for n in range(1, 10):
        ds = np.random.default_rng().choice(0x7FFFFFFF, size=x, replace=False)
        ds.sort()
        dataset.append(ds)
        x = x*2
        print('Data generation:', n, "%")
    return dataset

dataset = gen_dataset()

for data in dataset:
    cProfile.run('from_array(data)')

