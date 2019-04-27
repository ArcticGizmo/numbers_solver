from random import randint

SMALL_NUMBERS = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
LARGE_NUMBERS = [25, 50, 75, 100]
MAX_NUMBERS = 6


def get_numbers(n_large):
    if n_large > 4:
        n_large = 4

    n_small = MAX_NUMBERS - n_large

    large_numbers = _select_n(LARGE_NUMBERS, n_large)
    small_numbers = _select_n(SMALL_NUMBERS, n_small)

    selection = sorted(large_numbers + small_numbers)

    target = randint(101, 1000)

    return selection, target



def _select_n(choice_list, n):
    selection = []
    choices = choice_list[0:-1]

    for _ in range(0, n):
        index = randint(0, len(choices) - 1)

        selected = choices.pop(index)

        selection.append(selected)

    return selection



