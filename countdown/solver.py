from itertools import permutations
from collections import defaultdict


class Expression(object):

    def __init__(self, value, a, b, operator, func):
        self.a = a
        self.b = b
        self.value = value
        self.operator = operator
        self.func = func

    @property
    def a_val(self):
        if isinstance(self.a, Expression):
            return self.a.a_val
        return self.a

    @property
    def b_val(self):
        if isinstance(self.b, Expression):
            return self.b.b_val
        return self.b

    def as_equation(self):
        a = self.a.as_equation() if isinstance(self.a, Expression) else [self.a]
        b = self.b.as_equation() if isinstance(self.b, Expression) else [self.b]

        equation = '({} {} {})'.format(a, self.operator, b)
        return equation

    def numbers(self):
        """ :type: list[int]"""
        a_nums = self.a.numbers() if isinstance(self.a, Expression) else [self.a]
        b_nums = self.b.numbers() if isinstance(self.b, Expression) else [self.b]

        numbers = a_nums + b_nums
        return numbers

    def as_step(self):
        a = self.a_val if isinstance(self.a, int) else self.a.value
        b = self.b_val if isinstance(self.b, int) else self.b.value

        return '{} {} {} = {}'.format(a, self.operator, b, self.value)

    def steps(self):
        if isinstance(self.a, int) and isinstance(self.b, int):
            return [self.as_step()]

        a_step = [] if isinstance(self.a, int) else self.a.steps()
        b_step = [] if isinstance(self.b, int) else self.b.steps()

        return [self.as_step()] + a_step + b_step

    def ordered_steps(self):
        return reversed(self.steps())

    def __str__(self):
        return '''{} = {} | {}'''.format(self.as_equation(), self.value, sorted(self.numbers()))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False

        if sorted(self.numbers()) != sorted(other.numbers()):
            return False

        if self.as_equation() == other.as_equation():
            return True

        if self.operator != other.operator:
            return False

        if other.operator in ['+', '*']:
            a_equal = self.a == other.a
            b_equal = self.b == other.b

            if a_equal or b_equal:
                return True

        return False


class Solver(object):

    def __init__(self):
        self._ops = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x // y if (x % y) == 0 else 0
        }

        self.last_answer = None

    def answers(self, numbers, target):
        """ :rtype: Expression """
        n_numbers = len(numbers)

        # get all permutations for pairs of two numbers
        partials_map = defaultdict(list)

        # create the initial set of expressions for the given permutation
        for (a, b) in permutations(numbers, 2):
            for op, func in self._ops.items():
                value = func(a, b)
                if is_valid_value(value):
                    expression = Expression(value, a, b, op, func)
                    partials_map[value].append(expression)

        partials_map = filter_duplicates(partials_map)

        iteration = 0
        while iteration < n_numbers - 2:
            iteration += 1
            partials_map, target_found = process(numbers, self._ops, partials_map, target)

            if target_found:
                break


        # get the value closet to the target
        best_value = None
        deviation = 1E1000
        for value in sorted(partials_map.keys()):
            if value == target:
                best_value = target
                deviation = 0

            dev = abs(target - value)
            if (best_value is None) or (dev < deviation):
                best_value = value
                deviation = dev

        # get the best expression
        best_expression = None
        for expression in partials_map[best_value]:
            if (best_expression is None) or (len(expression.numbers()) < len(best_expression.numbers())):
                best_expression = expression

        self.last_answer = best_expression
        return best_expression


def process(numbers, operations, partials_map, target):
    new_partials_map = defaultdict(list)  # because you cant add during iteration
    for _, expressions in partials_map.items():
        for expression in expressions:
            for num in numbers:
                if not is_subset(numbers, expression.numbers() + [num]):
                    continue

                for op, func in operations.items():
                    value = func(expression.value, num)
                    if is_valid_value(value):
                        new_expression = Expression(value, expression, num, op, func)
                        new_partials_map[value].append(new_expression)

                        if value == target:
                            partials_map = merge_maps(partials_map, new_partials_map)
                            partials_map = filter_duplicates(partials_map)
                            return partials_map, True

    partials_map = merge_maps(partials_map, new_partials_map)
    partials_map = filter_duplicates(partials_map)

    return partials_map, False


def is_valid_value(value):
    if value <= 0:
        return False
    return True


def is_subset(available, selected):
    av_freq = _list_to_freq(available)
    sel_freq = _list_to_freq(selected)

    # ensure the selected has no more keys than available
    if len(sel_freq.keys()) > len(av_freq.keys()):
        return False

    # check key values to ensure that selected is not higher for any given key
    for value, freq in av_freq.items():
        if sel_freq[value] > freq:
            return False

    return True


def _list_to_freq(arr):
    freq = defaultdict(int)

    for v in arr:
        freq[v] += 1

    return freq


def merge_maps(map1, map2):
    merged = defaultdict(list)

    for key, expressions in map1.items():
        merged[key].extend(expressions)

    for key, expressions in map2.items():
        merged[key].extend(expressions)

    return merged


def _print_map(value_map):
    for value, expressions in value_map.items():
        print('Answers for: {}'.format(value))
        for exp in expressions:
            print('\t{}'.format(exp))


def filter_duplicates(expression_map):
    # this might need to become a prefix notation check

    new_partial_map = defaultdict(list)
    for value, expressions in expression_map.items():
        filtered_expression = []
        for e in expressions:
            if e not in filtered_expression:
                filtered_expression.append(e)
        new_partial_map[value] = filtered_expression

    return new_partial_map


