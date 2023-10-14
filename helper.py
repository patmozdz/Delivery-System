import random
import itertools
from package import main


def run_random():
    elements = [35, 12, 24, 22, 21, 39, 33, 7, 23, 11, 1, 2, 27, 10, 26, 5, 8, 17, 4]
    elements_copy = elements.copy()
    print(f'Current min: {main(elements_copy)}')

    total = float('inf')
    while total > 80:
        elements_copy = elements.copy()
        random.shuffle(elements_copy)
        print(f'Running scramble: {elements_copy}')
        total = main(elements_copy)
        print(f'Total found: {total}')

    else:
        print(f'Achieved {total}!\nFor permutation: {elements_copy}')


def run_permutations():
    elements = [35, 12, 24, 22, 21, 39, 33, 7, 23, 11, 1, 2, 27, 10, 26, 5, 8, 17, 4]

    lowest_arrangement = elements
    lowest_total = main(elements)
    for permutation in itertools.permutations(elements):
        print('Current lowest total:', lowest_total)
        print('Running permutation:', permutation)
        total = main(permutation)
        print('Total:', total)
        if total < lowest_total:
            lowest_total = total
            lowest_arrangement = permutation
            print('New lowest total:', lowest_total)
            print('New lowest arrangement:', lowest_arrangement)


run_random()
