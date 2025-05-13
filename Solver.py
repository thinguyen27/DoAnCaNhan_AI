import heapq
import random
import math
from collections import deque

GOAL_STATE = ("1", "2", "3", "4", "5", "6", "7", "8", "")

# ======= Các hàm hỗ trợ =======
def get_blank_index(state):
    return state.index("")

def get_neighbors(index):
    moves = {
        0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
        3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
        6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
    }
    return moves[index]

def swap_positions(state, blank_index, move):
    state = list(state)
    state[blank_index], state[move] = state[move], state[blank_index]
    return tuple(state)

def manhattan_distance(state):
    distance = 0
    for i, value in enumerate(state):
        if value == "":
            continue
        target_index = GOAL_STATE.index(value)
        x1, y1 = i % 3, i // 3
        x2, y2 = target_index % 3, target_index // 3
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# ======= Các thuật toán giải 8-Puzzle =======

def bfs_solve(initial_state):
    queue = deque([(initial_state, [])])
    visited = set([initial_state])
    while queue:
        current_state, path = queue.popleft()
        if current_state == GOAL_STATE:
            return path
        blank_index = get_blank_index(current_state)
        for move in get_neighbors(blank_index):
            new_state = swap_positions(current_state, blank_index, move)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, path + [new_state]))
    return None

def dfs_solve(initial_state):
    stack = [(initial_state, [], 0)]
    visited = set([initial_state])
    while stack:
        current_state, path, depth = stack.pop()
        if current_state == GOAL_STATE:
            return path
        if depth >= 50:
            continue
        blank_index = get_blank_index(current_state)
        for move in reversed(get_neighbors(blank_index)):
            new_state = swap_positions(current_state, blank_index, move)
            if new_state not in visited:
                visited.add(new_state)
                stack.append((new_state, path + [new_state], depth + 1))
    return None

def ids_solve(initial_state):
    def dfs_limited(state, path, depth, limit):
        if state == GOAL_STATE:
            return path
        if depth == limit:
            return None
        blank_index = get_blank_index(state)
        for move in get_neighbors(blank_index):
            new_state = swap_positions(state, blank_index, move)
            if new_state not in path:
                result = dfs_limited(new_state, path + [new_state], depth + 1, limit)
                if result:
                    return result
        return None

    limit = 0
    while True:
        result = dfs_limited(initial_state, [], 0, limit)
        if result:
            return result
        limit += 1

def ucs_solve(initial_state):
    queue = [(0, initial_state, [])]
    visited = set([initial_state])
    while queue:
        cost, current_state, path = heapq.heappop(queue)
        if current_state == GOAL_STATE:
            return path
        blank_index = get_blank_index(current_state)
        for move in get_neighbors(blank_index):
            new_state = swap_positions(current_state, blank_index, move)
            if new_state not in visited:
                visited.add(new_state)
                heapq.heappush(queue, (cost + 1, new_state, path + [new_state]))
    return None

def greedy_search_solve(initial_state):
    queue = [(manhattan_distance(initial_state), initial_state, [])]
    visited = set([initial_state])
    while queue:
        _, current_state, path = heapq.heappop(queue)
        if current_state == GOAL_STATE:
            return path
        blank_index = get_blank_index(current_state)
        for move in get_neighbors(blank_index):
            new_state = swap_positions(current_state, blank_index, move)
            if new_state not in visited:
                visited.add(new_state)
                heapq.heappush(queue, (manhattan_distance(new_state), new_state, path + [new_state]))
    return None

def a_star_solve(initial_state):
    queue = [(manhattan_distance(initial_state), 0, initial_state, [])]
    visited = set([initial_state])
    while queue:
        f, g, current_state, path = heapq.heappop(queue)
        if current_state == GOAL_STATE:
            return path
        blank_index = get_blank_index(current_state)
        for move in get_neighbors(blank_index):
            new_state = swap_positions(current_state, blank_index, move)
            if new_state not in visited:
                visited.add(new_state)
                new_g = g + 1
                new_f = new_g + manhattan_distance(new_state)
                heapq.heappush(queue, (new_f, new_g, new_state, path + [new_state]))
    return None

def ida_star_solve(initial_state):
    def search(path, g, threshold):
        current = path[-1]
        f = g + manhattan_distance(current)
        if f > threshold:
            return f
        if current == GOAL_STATE:
            return path
        min_cost = float('inf')
        blank_index = get_blank_index(current)
        for move in get_neighbors(blank_index):
            next_state = swap_positions(current, blank_index, move)
            if next_state not in path:
                result = search(path + [next_state], g + 1, threshold)
                if isinstance(result, list):
                    return result
                min_cost = min(min_cost, result)
        return min_cost

    threshold = manhattan_distance(initial_state)
    path = [initial_state]
    while True:
        result = search(path, 0, threshold)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return None
        threshold = result

def simple_hill_climbing(initial_state):
    current_state = initial_state
    while True:
        blank_index = get_blank_index(current_state)
        neighbors = [swap_positions(current_state, blank_index, move) for move in get_neighbors(blank_index)]
        next_states = [s for s in neighbors if manhattan_distance(s) < manhattan_distance(current_state)]
        if not next_states:
            return [current_state]
        current_state = random.choice(next_states)
        if current_state == GOAL_STATE:
            return [current_state]

def stochastic_hill_climbing(initial_state):
    current_state = initial_state
    while True:
        blank_index = get_blank_index(current_state)
        neighbors = [swap_positions(current_state, blank_index, move) for move in get_neighbors(blank_index)]
        better = [s for s in neighbors if manhattan_distance(s) < manhattan_distance(current_state)]
        if not better:
            return [current_state]
        current_state = random.choice(better)
        if current_state == GOAL_STATE:
            return [current_state]

def steepest_ascent_hill_climbing(initial_state):
    current_state = initial_state
    while True:
        blank_index = get_blank_index(current_state)
        neighbors = [swap_positions(current_state, blank_index, move) for move in get_neighbors(blank_index)]
        if not neighbors:
            return [current_state]
        best = min(neighbors, key=manhattan_distance)
        if manhattan_distance(best) >= manhattan_distance(current_state):
            return [current_state]
        current_state = best
        if current_state == GOAL_STATE:
            return [current_state]

def simulated_annealing(initial_state):
    current = initial_state
    T = 1000
    iteration = 1
    while T > 1:
        blank_index = get_blank_index(current)
        neighbors = [swap_positions(current, blank_index, move) for move in get_neighbors(blank_index)]
        if not neighbors:
            return [current]
        next_state = random.choice(neighbors)
        delta_e = manhattan_distance(current) - manhattan_distance(next_state)
        if delta_e > 0 or random.uniform(0, 1) < math.exp(delta_e / T):
            current = next_state
        T = T / (1 + 0.001 * iteration)
        iteration += 1
        if current == GOAL_STATE:
            return [current]
    return [current]

def beam_search(initial_state, beam_width=3):
    queue = [(manhattan_distance(initial_state), initial_state, [])]
    while queue:
        queue = sorted(queue)[:beam_width]
        next_queue = []
        for _, current_state, path in queue:
            if current_state == GOAL_STATE:
                return path
            blank_index = get_blank_index(current_state)
            for move in get_neighbors(blank_index):
                new_state = swap_positions(current_state, blank_index, move)
                if new_state not in path:
                    heapq.heappush(next_queue, (manhattan_distance(new_state), new_state, path + [new_state]))
        queue = next_queue
    return None

def genetic_algorithm_solve(initial_state, population_size=100, generations=500, mutation_rate=0.1):
    def fitness(state):
        return -manhattan_distance(state)

    def mutate(state):
        blank_index = get_blank_index(state)
        neighbors = [swap_positions(state, blank_index, move) for move in get_neighbors(blank_index)]
        return random.choice(neighbors)

    def crossover(p1, p2):
        child = []
        for i in range(9):
            child.append(p1[i] if random.random() < 0.5 else p2[i])
        return tuple(child)

    population = [tuple(random.sample(initial_state, 9)) for _ in range(population_size)]
    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        if population[0] == GOAL_STATE:
            return [GOAL_STATE]
        next_generation = population[:10]
        while len(next_generation) < population_size:
            p1, p2 = random.choices(population[:50], k=2)
            child = crossover(p1, p2)
            if random.random() < mutation_rate:
                child = mutate(child)
            next_generation.append(child)
        population = next_generation
    return [population[0]]

def and_or_search_solve(initial_state, max_depth=50):
    stack = [(initial_state, [initial_state], 0)]
    visited = set()
    while stack:
        current_state, path, depth = stack.pop()
        if current_state == GOAL_STATE:
            return path
        if depth >= max_depth:
            continue
        visited.add(current_state)
        blank_index = get_blank_index(current_state)
        for move in get_neighbors(blank_index):
            next_state = swap_positions(current_state, blank_index, move)
            if next_state not in visited:
                stack.append((next_state, path + [next_state], depth + 1))
    return []

def belief_based_search_solve(initial_state):
    queue = [(0, initial_state, [])]
    visited = set([initial_state])
    while queue:
        _, current_state, path = heapq.heappop(queue)
        if current_state == GOAL_STATE:
            return path
        blank_index = get_blank_index(current_state)
        for move in get_neighbors(blank_index):
            new_state = swap_positions(current_state, blank_index, move)
            if new_state not in visited:
                visited.add(new_state)
                score = sum(1 for i in range(9) if new_state[i] == GOAL_STATE[i])
                heapq.heappush(queue, (-score, new_state, path + [new_state]))
    return None

# ======= Các thuật toán CSP =======

def graph_coloring_solver(graph, colors):
    steps = []

    def backtrack(assignment):
        if len(assignment) == len(graph):
            return assignment
        unassigned = [v for v in graph if v not in assignment]
        var = unassigned[0]
        for color in colors:
            if all(assignment.get(neigh) != color for neigh in graph[var]):
                new_assignment = assignment.copy()
                new_assignment[var] = color
                steps.append(new_assignment)  # lưu lại mỗi lần gán biến
                result = backtrack(new_assignment)
                if result:
                    return result
        return None

    result = backtrack({})
    return steps if result else None


def backtracking_search_csp(variables, domains, constraints):
    steps = []

    def is_consistent(var, value, assignment):
        for (v1, v2) in constraints:
            if v1 == var and v2 in assignment and assignment[v2] == value:
                return False
            if v2 == var and v1 in assignment and assignment[v1] == value:
                return False
        return True

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment
        var = next(v for v in variables if v not in assignment)
        for value in domains[var]:
            if is_consistent(var, value, assignment):
                new_assignment = assignment.copy()
                new_assignment[var] = value
                steps.append(new_assignment)  # lưu lại mỗi lần gán biến
                result = backtrack(new_assignment)
                if result:
                    return result
        return None

    result = backtrack({})
    return steps if result else None


def ac3(csp):
    queue = [(xi, xj) for xi in csp['variables'] for xj in csp['neighbors'][xi]]
    while queue:
        xi, xj = queue.pop(0)
        if revise(csp, xi, xj):
            if not csp['domains'][xi]:
                return False
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
    revised = False
    for x in csp['domains'][xi][:]:
        if not any(csp['constraints'](xi, x, xj, y) for y in csp['domains'][xj]):
            csp['domains'][xi].remove(x)
            revised = True
    return revised
