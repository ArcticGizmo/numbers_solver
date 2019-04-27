from countdown.solver import Solver
from random import randint
from countdown.generator import get_numbers
import sys
from threading import Thread
from datetime import datetime


def run(n_large):
    # giev the user the numbers
    selection, target = get_numbers(n_large)
    print('Numbers are: {}'.format(selection, target))

    # start the solver in a different thread
    solver = Solver()
    solver_thread = Thread(target=solver.answers, args=(selection, target))
    solver_thread.start()

    # prompt the user to start the timer
    input('Hit enter to start timer')
    print('Target: {}'.format(target))
    timer()

    if solver_thread.is_alive():
        print('Awaiting solution')
        solver_thread.join()

    best_answer = solver.last_answer
    print('\n--- Solution --- ')
    print('Best Answer: {}'.format(best_answer.value))
    print('Numbers Used: {}'.format(best_answer.numbers()))
    for step in best_answer.ordered_steps():
        print(step)


def timer():
    start = datetime.now()

    input('\nEnter to stop')
    end = datetime.now()

    print('Time: {}'.format(end - start))


if __name__ == '__main__':
    args = sys.argv

    n_large = randint(0, 5)
    if len(args) > 1:
        n_large = int(args[0])

    run(n_large)


