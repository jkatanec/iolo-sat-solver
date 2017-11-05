import sys
from copy import *
from multiprocessing import Pool

import numpy as np

import interfacing


def simplify(clauses, variables, var, negation, usables):
    var_index = var - 1
    if negation:
        for cl in variables[var_index][1]:
            for var2 in clauses[cl][0]:
                variables[var2 - 1][0].remove(cl)
                # if now empty remove var2 from usables 0
                if len(variables[var2 - 1][0]) + len(variables[var2 - 1][1]) == 0:
                    usables[0].remove(var2 - 1)
            for var2 in clauses[cl][1]:
                if var2 != var:
                    variables[var2 - 1][1].remove(cl)
                    # if now empty remove var2 from usables 0
                    if len(variables[var2 - 1][0]) + len(variables[var2 - 1][1]) == 0:
                        usables[0].remove(var2 - 1)
            clauses[cl][:] = [[], []]
            # if was on remove cl from usables 1
            try:
                usables[1].remove(clauses[cl])
            except ValueError:
                pass
        for cl in variables[var_index][0]:
            clauses[cl][0].remove(var)
            if len(clauses[cl][0]) + len(clauses[cl][1]) == 0:
                return False
            # if now literal add cl to usables 1
            if len(clauses[cl][1]) + len(clauses[cl][0]) == 1:
                usables[1].append(clauses[cl])
    else:
        for cl in variables[var_index][0]:
            for var2 in clauses[cl][0]:
                if var2 != var:
                    variables[var2 - 1][0].remove(cl)
                    # if now empty remove var2 from usables 0
                    if len(variables[var2 - 1][0]) + len(variables[var2 - 1][1]) == 0:
                        usables[0].remove(var2 - 1)
            for var2 in clauses[cl][1]:
                variables[var2 - 1][1].remove(cl)
                # if now empty remove var2 from usables 0
                if len(variables[var2 - 1][0]) + len(variables[var2 - 1][1]) == 0:
                    usables[0].remove(var2 - 1)
            clauses[cl][:] = [[], []]
            # if was on remove cl from usables 1
            try:
                usables[1].remove(clauses[cl])
            except ValueError:
                pass
        for cl in variables[var_index][1]:
            clauses[cl][1].remove(var)
            if len(clauses[cl][1]) + len(clauses[cl][0]) == 0:
                return False
            # if now literal add cl to usables 1
            if len(clauses[cl][1]) + len(clauses[cl][0]) == 1:
                usables[1].append(clauses[cl])
    # remove var from usables 0
    usables[0].remove(var_index)
    return True


def unit_clauses(variables, clauses, valuation, usables):
    if len(usables[1][0][0]) == 1:  # l
        var = usables[1][0][0][0]
        valuation.add(var)
        works = simplify(clauses, variables, var, False, usables)
        if not works:
            return False
    else:  # not(l)
        var = usables[1][0][1][0]
        valuation.add(-var)
        works = simplify(clauses, variables, var, True, usables)
    return works


def choose_literal(variables, clauses, valuation, usables, depth):
    if depth != 0:
        valuation_1 = test_chosen_literal((variables, clauses, valuation, usables, False, depth, 0))
        if len(valuation_1) != 0:
            return valuation_1
        return test_chosen_literal((variables, clauses, valuation, usables, True, depth, 0))
    else:
        with Pool() as p:
            results = p.imap_unordered(test_chosen_literal, [(variables, clauses, valuation, usables, i % 2 == 0, depth,
                                                              int(np.floor(i / 2))) for i in range(2 * len(usables))])
            k = 0
            while k <= len(usables):
                k += 1
                res = next(results)
                if len(res) > 0:
                    p.terminate()
                    return res
            return set([])


def test_chosen_literal(params):
    variables, clauses, valuation, usables, negated, depth, k = params
    clauses_copy = deepcopy(clauses)
    variables_copy = deepcopy(variables)
    usables_copy = deepcopy(usables)
    works = simplify(clauses_copy, variables_copy, usables[0][k] + 1, negated, usables_copy)
    if works:
        valuation_copy = copy(valuation)
        if negated:
            valuation_copy.add(-usables[0][k] - 1)
        else:
            valuation_copy.add(usables[0][k] + 1)
        valuation_copy = solve(variables_copy, clauses_copy, valuation_copy, usables_copy, depth + 1)
        if len(valuation_copy) != 0:
            return valuation_copy
    return set([])


def solve(variables, clauses, valuation, usables, depth):
    while len(usables[1]) > 0:
        selects = unit_clauses(variables, clauses, valuation, usables)
        if not selects:
            return set([])
    if sum([len(clauses[i][0]) + len(clauses[i][1]) for i in range(len(clauses))]) == 0:
        return valuation
    return choose_literal(variables, clauses, valuation, usables, depth)


def call_initial_solver(input_file, output_file):
    variables, clauses = interfacing.dimacs_read(input_file)
    valuation = set([])
    usables = [[], []]
    for index, variable in enumerate(variables):
        if len(variable[0]) + len(variable[1]) > 0:
            usables[0].append(index)
    for clause in clauses:
        if len(clause[0]) + len(clause[1]) == 1:
            usables[1].append(clause)
    valuation = solve(variables, clauses, valuation, usables, 0)
    interfacing.dimacs_write(output_file, valuation)


if __name__ == "__main__":
    call_initial_solver(sys.argv[1], sys.argv[2])
