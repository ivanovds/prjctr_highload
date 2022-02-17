import random
import cProfile, pstats
import sys

# source: https://stackabuse.com/counting-sort-in-python/
def counting_sort(inputArray):
    # Find the maximum element in the inputArray
    maxElement = max(inputArray)

    countArrayLength = maxElement+1

    # Initialize the countArray with (max+1) zeros
    countArray = [0] * countArrayLength

    # Step 1 -> Traverse the inputArray and increase
    # the corresponding count for every element by 1
    for el in inputArray:
        countArray[el] += 1

    # Step 2 -> For each element in the countArray,
    # sum up its value with the value of the previous
    # element, and then store that value
    # as the value of the current element
    for i in range(1, countArrayLength):
        countArray[i] += countArray[i-1]

    # Step 3 -> Calculate element position
    # based on the countArray values
    outputArray = [0] * len(inputArray)
    i = len(inputArray) - 1
    while i >= 0:
        currentEl = inputArray[i]
        countArray[currentEl] -= 1
        newPosition = countArray[currentEl]
        outputArray[newPosition] = currentEl
        i -= 1

    return outputArray

# Python uses Timsort algorithm https://en.wikipedia.org/wiki/Timsort
def timsort(array):
    return sorted(array)

def measure(array, n_experiments=10):
    counting_sort_durations = []
    timsort_durations = []

    for i in range(n_experiments):
        profiler = cProfile.Profile()
        profiler.enable()
        array1 = counting_sort(array)
        profiler.disable()
        total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
        counting_sort_durations.append(total_tt)

        profiler = cProfile.Profile()
        profiler.enable()
        array2 = timsort(array)
        profiler.disable()
        total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
        timsort_durations.append(total_tt)

        assert(array1 == array2)

    if len(array) > 10:
        text = "Array length: " + str(len(array))
    else:
        text = "Array: " + str(array)

    print(text,
        "Median CountingSort Duration: ",
        sorted(counting_sort_durations)[n_experiments / 2 - 1],
        "Median Timsort Duration: ",
        sorted(timsort_durations)[n_experiments / 2 - 1])

if __name__ == "__main__":
    # array = [2,2,0,6,1,9,9,10000000000]
    # ERROR: 137

    measure([2,2,0,6,1,9,9])

    array = range(1000)
    random.shuffle(array)
    measure(array)

    array = range(10000)
    random.shuffle(array)
    measure(array)

    measure([1, 100000])
    measure([1, 1000000])
    measure([1, 10000000])
