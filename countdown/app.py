from countdown.solver import Solver, Expression
from countdown.generator import get_numbers


def main():
    n_large = 3

    selection, target = get_numbers(n_large)
    print('Numbers are: {} -> {}'.format(selection, target))

    solver = Solver()

    best_answer = solver.answers(selection, target)

    print('Best answer found: {}'.format(best_answer.value))

    input('Hit enter to get solution')

    print('--- Solution --- ')
    print('Numbers Used: {}'.format(best_answer.numbers()))
    for step in best_answer.ordered_steps():
        print(step)



if __name__ == '__main__':
    main()


