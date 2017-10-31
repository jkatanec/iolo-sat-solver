
def dimacs_write(output_file, valuation):
    file = open(output_file, 'w')
    if valuation.isempty():
        file.write("0")
        return 0
    # TODO: valuation
    return 0


def dimacs_read(input_file):
    variables = None
    clauses = None
    clause_index = 0
    end_of_preamble = False
    with open(input_file) as f:
        for line in f:
            if line[0] == 'c':
                if end_of_preamble:
                    raise FormatError("problem line not at the end of preamble.")
                else:
                    continue
            if line[0] == 'p':
                var_number, clause_number = parse_problem_line(line)
                variables = [[[], []] for _ in range(var_number)]
                clauses = [[[], []] for _ in range(clause_number)]
                end_of_preamble = True
                continue
            # if no problem line is defined throw exception
            repeat = True
            index = 0
            # several clauses can be written in the same line
            while repeat:
                repeat = False
                if variables is None or clauses is None:
                    raise FormatError("problem line not defined.")
                variables, clauses, index, ends = clause_read(line, clause_index, variables, clauses, index)
                # one clause can be spread through several lines
                if ends:
                    clause_index += 1
                if index < len(line) - 1:
                    repeat = True
    return variables, clauses


def clause_read(line, clause_index, variables, clauses, index):
    i = index
    while i < len(line):
        i, num = check_symbol(line, i)
        if i > len(line):
            break
        if num == 0:
            return variables, clauses, i, True
        if num < 0:
            variables[-num - 1][1].append(clause_index)
            clauses[clause_index][1].append(-num)
        else:
            variables[num-1][0].append(clause_index)
            clauses[clause_index][0].append(num)
    return variables, clauses, i, False


def check_symbol(line, i):
    if i >= len(line):
        return i + 1, 0
    if line[i] == "0":
        return i + 1, 0
    if line[i].isspace():
        return check_symbol(line, i + 1)
    if line[i] == "-":
        j, num = check_symbol(line, i + 1)
        return j, -num
    return get_num(line, i)


def parse_problem_line(line):
    i = skip_whitespace(line, 1)
    if line[i:i+3] != "cnf":
        raise FormatError("format other than CNF defined.")
    i = skip_whitespace(line, i + 3)
    i, var_num = get_num(line, i)
    i = skip_whitespace(line, i)
    i, cla_num = get_num(line, i)
    return var_num, cla_num


# convert string to int
def get_num(line, i):
    num = 0
    if line[i] < "0" or line[i] > "9":
        raise FormatError("a clause contains invalid characters.")
    while "0" <= line[i] <= "9":
        num = 10 * num + ord(line[i]) - ord('0')
        i += 1
    return i, num


# iterate through whitespaces
def skip_whitespace(line, i):
    while line[i].isspace():
        i += 1
    return i


class FormatError(Exception):
    def __init__(self, expr):
        super(FormatError, self).__init__('Input file not of DIMACS CNF format: ' + expr)
