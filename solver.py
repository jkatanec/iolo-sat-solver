import interfacing
from copy import *


def simplify(clauses, variables, var, negation):
    if negation:
        for cl in variables[var - 1][1]:
            for var2 in clauses[cl][0]:
                variables[var2 - 1][0].remove(cl)
            for var2 in clauses[cl][1]:
                if var2 != var:
                    variables[var2 - 1][1].remove(cl)
            clauses[cl][1] = []
            clauses[cl][0] = []
        for cl in variables[var - 1][0]:
            clauses[cl][0].remove(var)
            if len(clauses[cl][0]) + len(clauses[cl][1]) == 0:
                return False
    else:
        for cl in variables[var - 1][0]:
            for var2 in clauses[cl][0]:
                if var2 != var:
                    variables[var2 - 1][0].remove(cl)
            for var2 in clauses[cl][1]:
                variables[var2 - 1][1].remove(cl)
            clauses[cl][0] = []
            clauses[cl][1] = []
        for cl in variables[var - 1][1]:
            clauses[cl][1].remove(var)
            if len(clauses[cl][1]) + len(clauses[cl][0]) == 0:
                return False
    variables[var - 1][0] = []
    variables[var - 1][1] = []
    return True


def unit_clauses(variables, clauses, valuation):
    for clause in clauses:
        if len(clause[0]) + len(clause[1]) == 1:
            if len(clause[0]) == 1:  # l
                var = clause[0][0]
                valuation.add(var)
                works = simplify(clauses, variables, var, False)
                if not works:
                    return False
            else:  # not(l)
                var = clause[1][0]
                valuation.add(-var)
                works = simplify(clauses, variables, var, True)
                if not works:
                    return False
    return True


def check_empty(clauses):
    return sum([len(clauses[i][0]) + len(clauses[i][1]) for i in range(len(clauses))]) == 0


def choose_literal(variables, clauses, valuation):
    i = 0
    while len(variables[i][0]) + len(variables[i][1]) == 0:
        i += 1
    # suppose i+1 is true
    clauses_copy = deepcopy(clauses)
    variables_copy = deepcopy(variables)
    works = simplify(clauses_copy, variables_copy, i + 1, True)
    if works:
        valuation_copy = deepcopy(valuation)
        valuation_copy.add(i + 1)
        valuation_copy = solve(variables_copy, clauses_copy, valuation_copy)
        if len(valuation_copy) != 0:
            variables[:] = variables_copy
            clauses[:] = clauses_copy
            return valuation_copy
    # i + 1 can't be true
    clauses_copy = deepcopy(clauses)
    variables_copy = deepcopy(variables)
    works = simplify(clauses_copy, variables_copy, i + 1, False)
    if works:
        valuation_copy = deepcopy(valuation)
        valuation_copy.add(-i - 1)
        valuation_copy = solve(variables_copy, clauses_copy, valuation_copy)
        if len(valuation_copy) != 0:
            variables[:] = variables_copy
            clauses[:] = clauses_copy
            return valuation_copy
    return set([])


def solve(variables, clauses, valuation):
    valuation_size = -1
    while valuation_size != len(valuation):
        valuation_size = len(valuation)
        selects = unit_clauses(variables, clauses, valuation)
        if not selects:
            return set([])
    if check_empty(clauses):
        return valuation
    return choose_literal(variables, clauses, valuation)


def call_initial_solver(input_file, output_file):
    variables, clauses = interfacing.dimacs_read(input_file)
    valuation = set([])
    valuation = solve(variables, clauses, valuation)
    interfacing.dimacs_write(output_file, valuation)


# call_initial_solver("test1.txt", "test_output.txt")
