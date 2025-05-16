import heapq
import random
import math
from collections import deque

GOAL_STATE = ("1", "2", "3", "4", "5", "6", "7", "8", "")

# ======= Các hàm hỗ trợ =======
def get_blank_index(state):
    if "" not in state:
        raise ValueError("State does not contain a blank tile.")
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

def genetic_algorithm(initial_state, goal_state = GOAL_STATE):
    def flatten(state):
        return [num for row in state for num in row]

    def hamming_distance(state):
        flat_s = flatten(state)
        flat_g = flatten(goal_state)
        return sum(1 for a, b in zip(flat_s, flat_g) if a != b and a != 0)

    def generate_candidate():
        path = [initial_state]
        current = initial_state
        visited = {current}

        for _ in range(30):
            blank_index = get_blank_index(current)
            neighbors = []
            for move in get_neighbors(blank_index):
                new_state = swap_positions(current, blank_index, move)
                if new_state not in visited:
                    neighbors.append(new_state)

            if not neighbors:
                break

            current = random.choice(neighbors)
            visited.add(current)
            path.append(current)

        return path


    def evaluate(candidate):
        return -hamming_distance(candidate[-1])

    def crossover(p1, p2):
        if len(p1) < 3 or len(p2) < 3:
            return p1[:]  # hoặc return p2[:], hoặc chọn random giữa 2

        split = random.randint(1, min(len(p1), len(p2)) - 2)
        return p1[:split] + p2[split:]


    def mutate(candidate):
        idx = random.randint(1, len(candidate) - 1)
        base = candidate[idx - 1]
        visited = set(candidate[:idx])

        blank_index = get_blank_index(base)  # Lấy vị trí ô trống
        neighbors = []
        for move in get_neighbors(blank_index):
            new_state = swap_positions(base, blank_index, move)
            if new_state not in visited:
                neighbors.append(new_state)

        if not neighbors:
            return candidate
        new_state = random.choice(neighbors)
        return candidate[:idx] + [new_state]



    population = [generate_candidate() for _ in range(30)]

    for _ in range(200):
        population.sort(key=evaluate, reverse=True)
        next_gen = population[:2]
        while len(next_gen) < 30:
            p1, p2 = random.sample(population[:5], 2)
            child = crossover(p1, p2)
            if random.random() < 0.2:
                child = mutate(child)
            next_gen.append(child)
        population = next_gen

    best = max(population, key=evaluate)
    if best[-1] == goal_state:
        return best
    return None

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
    steps = []  # Lưu lại các bước trong quá trình backtracking

    def is_consistent(var, value, assignment):
        # Kiểm tra tính nhất quán của giá trị
        for (v1, v2) in constraints:
            if v1 == var and v2 in assignment and assignment[v2] == value:
                return False
            if v2 == var and v1 in assignment and assignment[v1] == value:
                return False
        return True

    def backtrack(assignment):
        # Nếu tất cả các biến đã được gán giá trị, trả về kết quả
        if len(assignment) == len(variables):
            # Construct state as a tuple of length 9
            state = [''] * 9  # Tạo một danh sách có 9 ô trống
            for var in variables:
                index = ord(var) - ord('X')  # Dùng chỉ số của biến (X, Y, Z, ...)
                state[index] = assignment.get(var, '')  # Gán giá trị cho ô tương ứng
            steps.append(tuple(state))  # Lưu trạng thái dưới dạng tuple
            return assignment

        # Lựa chọn biến chưa được gán giá trị (biến đầu tiên trong danh sách variables)
        var = next(v for v in variables if v not in assignment)

        # Thử tất cả các giá trị có thể cho biến này
        for value in domains[var]:
            if is_consistent(var, value, assignment):
                new_assignment = assignment.copy()  # Sao chép assignment hiện tại
                new_assignment[var] = value  # Gán giá trị cho biến

                result = backtrack(new_assignment)  # Tái gọi backtrack cho assignment mới
                if result:
                    return result  # Nếu tìm thấy kết quả, trả về

        # Nếu không tìm được kết quả hợp lệ, quay lại (backtrack)
        return None

    result = backtrack({})  # Bắt đầu với assignment rỗng
    return steps if result else None  # Trả về các bước nếu có kết quả, nếu không trả về None



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


# Backtracking với Forward Checking
def forward_checking(variables, domains, constraints):
    """
    Hàm Forward Checking kiểm tra tính nhất quán của các giá trị trong miền của các biến còn lại.
    """
    for var in variables:
        if len(domains[var]) == 0:  # Nếu không còn giá trị hợp lệ trong miền của biến
            return False
        for value in domains[var]:
            # Kiểm tra các biến hàng xóm trong danh sách ràng buộc
            for (v1, v2) in constraints:
                if v1 == var:
                    # Loại bỏ giá trị xung đột trong miền của biến v2
                    if value in domains[v2]:
                        domains[v2].remove(value)
                elif v2 == var:
                    # Loại bỏ giá trị xung đột trong miền của biến v1
                    if value in domains[v1]:
                        domains[v1].remove(value)
    return True

def backtracking_with_forward_checking(variables, domains, constraints, assignment={}):
    """
    Thuật toán Backtracking với Forward Checking để giải quyết CSP.
    """
    if len(assignment) == len(variables):  # Nếu tất cả các biến đã được gán giá trị
        return assignment

    # Chọn biến chưa gán giá trị (ở đây tôi sẽ chọn biến đầu tiên chưa được gán)
    var = next(v for v in variables if v not in assignment)

    # Thử tất cả các giá trị có thể cho biến này
    for value in domains[var]:
        # Gán giá trị cho biến
        assignment[var] = value

        # Forward checking
        new_domains = {k: set(v) for k, v in domains.items()}  # Sao chép các miền
        if forward_checking(variables, new_domains, constraints):
            # Nếu forward checking thành công, tiếp tục với các biến còn lại
            result = backtracking_with_forward_checking(variables, new_domains, constraints, assignment)
            if result:
                return result  # Nếu tìm thấy giải pháp, trả về

        # Nếu không tìm thấy giải pháp, quay lại và thử giá trị khác
        del assignment[var]

    return None  # Nếu không tìm thấy giải pháp nào
