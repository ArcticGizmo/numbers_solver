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

    print('Solution: {}'.format(str(best_answer)))


    # solver = Solver()
    #
    # numbers = [9, 6, 4, 3, 3, 50]
    # target = 330
    # print('Numbers: {}'.format(numbers))
    #
    # possible_numbers = solver.answers(numbers, target)


if __name__ == '__main__':
    main()


