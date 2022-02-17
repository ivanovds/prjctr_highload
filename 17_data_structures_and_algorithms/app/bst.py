from __future__ import print_function
from pybst.rdbtree import RBTree
import pdb
import random
import cProfile, pstats
import sys

def insert(bst, array):
    for value in array:
        bst.insert(value, value)

def search(bst, n, limit):
    for _ in range(n):
        value = random.randint(0, limit)
        bst.get_node(value)

def test_delete(bst, n, limit):
    for i in range(n):
        value = random.randint(0, limit)
        bst.delete(value)

    # assert(1 == 1)

if __name__ == "__main__":
    unique_values_number = int(sys.argv[1]) # 100
    search_iterations = 10000
    n_experiments = 20
    insert_durations = []
    search_durations = []

    # cProfile.run('test_delete(bst, n, limit)')
    for i in range(n_experiments):
        array = range(unique_values_number)
        random.shuffle(array)

        bst = RBTree()

        profiler = cProfile.Profile()
        profiler.enable()
        insert(bst, array)
        profiler.disable()
        total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
        insert_durations.append(total_tt)

        # Test search complexity
        profiler = cProfile.Profile()
        profiler.enable()
        search(bst, search_iterations, unique_values_number)
        profiler.disable()
        total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
        search_durations.append(total_tt)

    print(unique_values_number,
        "unique values.",
        n_experiments,
        "experiments.",
        "Median Insert Duration: ",
        sorted(insert_durations)[n_experiments / 2 - 1],
        "Median Search Duration: ",
        sorted(search_durations)[n_experiments / 2 - 1])
