from countdown.solver import Solver, Expression, is_subset


def main():
    solver = Solver()

    numbers = [9, 6, 4, 3, 3, 50]
    target = 330
    print('Numbers: {}'.format(numbers))

    possible_numbers = solver.answers(numbers, target)



    # print('Numbers in; {}'.format(numbers))
    # for value, expressions in possible_numbers.items():
    #     print('Answers for: {}'.format(value))
    #     for exp in expressions:
    #         print('\t{}'.format(exp))

if __name__ == '__main__':
    main()


