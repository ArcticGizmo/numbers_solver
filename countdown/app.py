from countdown.solver import Solver
from random import randint
from countdown.generator import get_numbers
import sys


def run(n_large):
    selection, target = get_numbers(n_large)
    print('Numbers are: {} -> {}'.format(selection, target))

    solver = Solver()
    best_answer = solver.answers(selection, target)

    input('Hit enter to get solution')

    print('--- Solution --- ')
    print('Best Answer: {}'.format(best_answer.value))
    print('Numbers Used: {}'.format(best_answer.numbers()))
    for step in best_answer.ordered_steps():
        print(step)



if __name__ == '__main__':
    args = sys.argv

    n_large = randint(0, 5)
    if len(args) > 1:
        n_large = int(args[0])

    run(n_large)


