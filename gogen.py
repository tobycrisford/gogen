import string

def copy_positions(possible_positions):
    pos_copy = {}
    for l in possible_positions:
        pos_copy[l] = {p for p in possible_positions[l]}

    return pos_copy

def neighbours_single(position):

    result = set()
    for i in range(position[0] - 1, position[0] + 2):
        for j in range(position[1] - 1, position[1] + 2):
            if i == position[0] and j == position[1]:
                continue
            if i < 0 or j < 0:
                continue
            if i > 4 or j > 4:
                continue
            result.add((i,j))

    return result


def neighbours(positions):

    result = set()
    for pos in positions:
        result.update(neighbours_single(pos))

    return result

def solve_gogen(possible_positions_arg, connections):

    possible_positions = copy_positions(possible_positions_arg)
    
    while True:
        changed = False

        for l in possible_positions:
            if len(possible_positions[l]) == 1:
                for ll in possible_positions:
                    if ll == l:
                        continue
                    old_len = len(possible_positions[ll])
                    possible_positions[ll] = possible_positions[ll].difference(possible_positions[l])
                    if len(possible_positions[ll]) != old_len:
                        changed = True

        for c in connections:
            
            old_lens = (len(possible_positions[c[0]]), len(possible_positions[c[1]]))
            possible_positions[c[1]] = neighbours(possible_positions[c[0]]).intersection(possible_positions[c[1]])
            possible_positions[c[0]] = neighbours(possible_positions[c[1]]).intersection(possible_positions[c[0]])

            if len(possible_positions[c[0]]) == 0 or len(possible_positions[c[1]]) == 0:
                return []
            
            if any(len(possible_positions[c[i]]) != old_lens[i] for i in (0,1)):
                changed = True
        
        if not changed:
            break

    if all(len(possible_positions[l]) == 1 for l in possible_positions):
        return [{l: tuple(possible_positions[l])[0] for l in possible_positions}]
    
    min_length = 1000
    best_l = None
    for l in possible_positions:
        if len(possible_positions[l]) < min_length and len(possible_positions[l]) != 1:
            min_length = len(possible_positions[l])
            best_l = l
    
    solutions = []
    pos_set = possible_positions[best_l]
    for p in pos_set:
        possible_positions[best_l] = {p}
        solutions += solve_gogen(possible_positions, connections)
        
    return solutions

def parse_gogen_inputs(start_letters, words):

    possible_positions = {}
    possible_positions[start_letters[0]] = {(0,0)}
    possible_positions[start_letters[1]] = {(0,2)}
    possible_positions[start_letters[2]] = {(0,4)}
    possible_positions[start_letters[3]] = {(2,0)}
    possible_positions[start_letters[4]] = {(2,2)}
    possible_positions[start_letters[5]] = {(2,4)}
    possible_positions[start_letters[6]] = {(4,0)}
    possible_positions[start_letters[7]] = {(4,2)}
    possible_positions[start_letters[8]] = {(4,4)}

    all_positions = []
    for i in range(0,5):
        for j in range(0,5):
            all_positions.append((i,j))
    
    for l in set(string.ascii_lowercase).difference({'z'}):
        if not (l in possible_positions):
            possible_positions[l] = {p for p in all_positions}

    connections = []
    for word in words:
        for i in range(len(word)-1):
            connections.append((word[i],word[i+1]))

    return possible_positions, connections

def print_solutions(solutions):

    if len(solutions) == 0:
        print("No solution exists")
    for sol in solutions:
        pos_to_letter = {sol[l]: l for l in sol}
        for i in range(5):
            print('   '.join([pos_to_letter[(i,j)] for j in range(5)]))
        print("----------")

if __name__ == "__main__":

    start_letters = input("Enter 9 starting letters from left-right top-bottom, separated by space:").split(" ")
    words = input("Enter words, lowercase, separated by space:").split(" ")

    possible_positions, connections = parse_gogen_inputs(start_letters, words)

    solutions = solve_gogen(possible_positions, connections)
    print_solutions(solutions)