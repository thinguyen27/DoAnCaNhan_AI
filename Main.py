import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import random
from Solver import *  # Đảm bảo rằng bạn có các thuật toán từ Solver.py

# Cấu hình cửa sổ Tkinter
root = tk.Tk()
root.title("Giải đố 8-Puzzle + Thuật toán CSP")
root.geometry("800x600")

# Khởi tạo trạng thái ban đầu
INITIAL_STATE = ("2", "6", "5", "", "8", "7", "4", "3", "1")
GOAL_STATE = ("1", "2", "3", "4", "5", "6", "7", "8", "")

# Tạo frame chính
frame_main = tk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

# Tạo frame để hiển thị các bước
frame_steps = tk.Frame(frame_main)
frame_steps.pack(side=tk.RIGHT, padx=10, pady=10)

steps_text = tk.Text(frame_steps, width=30, height=25, wrap=tk.WORD, state=tk.DISABLED)
steps_text.grid(row=0, column=0, padx=10, pady=10)
steps_text.insert(tk.END, "Bảng các bước giải sẽ hiển thị ở đây.\n")

# Tạo canvas cho bảng 3x3
canvas = tk.Canvas(frame_main, width=400, height=400)
canvas.pack(side=tk.LEFT, padx=10, pady=10)

# Vẽ bảng 3x3
def draw_puzzle(state):
    canvas.delete("all")  # Xóa canvas
    tile_size = 120
    for i in range(3):
        for j in range(3):
            value = state[i * 3 + j]
            x, y = j * tile_size, i * tile_size
            color = "lightblue" if value != "" else "red"
            canvas.create_rectangle(x, y, x + tile_size, y + tile_size, fill=color, outline="black", width=2)
            if value != "":
                canvas.create_text(x + tile_size // 2, y + tile_size // 2, text=value, font=("Arial", 24))

# Cập nhật hộp văn bản các bước
def update_steps(solution_path):
    steps_text.config(state=tk.NORMAL)  # Cho phép chỉnh sửa
    steps_text.delete(1.0, tk.END)  # Xóa nội dung cũ
    steps_text.insert(tk.END, "Các bước giải:\n")
    for i, state in enumerate(solution_path):
        steps_text.insert(tk.END, f"Bước {i + 1}: {state}\n")
    steps_text.config(state=tk.DISABLED)  # Vô hiệu chỉnh sửa

# Hàm giải bài toán và cập nhật trạng thái
current_step = 0
solution_path = []

def solve_puzzle():
    global current_step, solution_path
    
    algorithm = algorithm_combobox.get()  # Lấy thuật toán được chọn
    start_time = time.time()
    
    # Chạy thuật toán đã chọn
    #Uninformed Search
    if algorithm == "BFS":
        solution_path = bfs_solve(INITIAL_STATE)
    elif algorithm == "DFS":
        solution_path = dfs_solve(INITIAL_STATE)
    elif algorithm == "UCS":
        solution_path = ucs_solve(INITIAL_STATE)
    elif algorithm == "IDS":
        solution_path = ids_solve(INITIAL_STATE)
    #Informed Search
    elif algorithm == "Greedy":
        solution_path = greedy_search_solve(INITIAL_STATE)
    elif algorithm == "A*":
        solution_path = a_star_solve(INITIAL_STATE)
    elif algorithm == "IDA*":
        solution_path = ida_star_solve(INITIAL_STATE)
    #Local Search
    elif algorithm == "Simulated Annealing":
        solution_path = simulated_annealing(INITIAL_STATE)
    elif algorithm == "Beam Search":
        solution_path = beam_search(INITIAL_STATE)
    elif algorithm == "Stochastic Hill Climbing":
        solution_path = stochastic_hill_climbing(INITIAL_STATE)
    elif algorithm == "Steepest Ascent Hill Climbing":
        solution_path = steepest_ascent_hill_climbing(INITIAL_STATE)   
    elif algorithm == "Simple Hill Climbing":
        solution_path = simple_hill_climbing(INITIAL_STATE) 
    elif algorithm == "Genetic Algorithm":
        solution_path = genetic_algorithm_solve(INITIAL_STATE)
    #Complex Environment
    elif algorithm == "And-Or Graph Search":
        solution_path = and_or_search_solve(INITIAL_STATE)
    elif algorithm == "Belief-Based Search":
        solution_path = belief_based_search_solve(INITIAL_STATE)
    #CSPS
    elif algorithm == "Backtracking with CSP":
        # Implement CSP solving logic if required
        solution_path = []  # Replace with actual logic if needed
    else:
        solution_path = []
    
    # Cập nhật các bước giải
    update_steps(solution_path)
    
    # Bắt đầu cập nhật trạng thái theo chu kỳ
    current_step = 0
    update_puzzle_state()
    end_time = time.time()
    runtime = end_time - start_time
    if(solution_path[len(solution_path)-1]==GOAL_STATE):
        messagebox.showinfo("Hoàn tất", f"Thuật toán {algorithm} hoàn thành!\nThời gian: {runtime:.4f} giây")
    else:
        messagebox.showinfo("No solution",f"Không tìm ra bài giải")

# Cập nhật trạng thái bảng theo chu kỳ
def update_puzzle_state():
    global current_step
    if current_step < len(solution_path):
        draw_puzzle(solution_path[current_step])  # Vẽ trạng thái hiện tại
        current_step += 1
        root.after(200, update_puzzle_state)  # Lên lịch cập nhật sau 0.2 giây

# Thêm ComboBox để chọn thuật toán
algorithm_combobox = ttk.Combobox(frame_main, values=[
    "BFS", "DFS", "UCS", "IDS", "Greedy", "A*", 
    "IDA*", "Simulated Annealing", "Beam Search", 
    "Stochastic Hill Climbing", "Steepest Ascent Hill Climbing", 
    "Simple Hill Climbing", "Genetic Algorithm", "And-Or Graph Search", 
    "Belief-Based Search", "Backtracking with CSP"
], width=20)
algorithm_combobox.set("BFS")  # Thuật toán mặc định
algorithm_combobox.pack(side=tk.TOP, padx=10, pady=10)

# Thêm nút "Solve"
solve_button = tk.Button(frame_main, text="Solve", width=15, command=solve_puzzle)
solve_button.pack(side=tk.TOP, padx=10, pady=5)

# Hàm khởi tạo lại trạng thái ngẫu nhiên
def randomize_state():
    global INITIAL_STATE  # Đảm bảo rằng ta đang thay đổi trạng thái ban đầu
    # Danh sách các di chuyển khả thi
    moves = [1, -1, 3, -3]  # Phải, Trái, Xuống, Lên (theo chỉ số)
    state = list(INITIAL_STATE)
    
    # Xáo trộn trạng thái bằng các di chuyển ngẫu nhiên
    blank_index = state.index("")  # Tìm vị trí ô trống
    for _ in range(100):  # Thực hiện 100 di chuyển ngẫu nhiên
        move = random.choice(moves)
        new_blank_index = blank_index + move
        if 0 <= new_blank_index < 9 and (blank_index % 3 != 2 or move != 1) and (blank_index % 3 != 0 or move != -1):
            state[blank_index], state[new_blank_index] = state[new_blank_index], state[blank_index]
            blank_index = new_blank_index
    
    # Cập nhật trạng thái ban đầu
    INITIAL_STATE = tuple(state)
    draw_puzzle(INITIAL_STATE)  # Vẽ lại bảng với trạng thái mới

# Thêm nút "Randomize"
random_button = tk.Button(frame_main, text="Randomize", width=15, command=randomize_state)
random_button.pack(side=tk.TOP, padx=10, pady=5)

# Vẽ bảng lần đầu tiên
draw_puzzle(INITIAL_STATE)

# Chạy ứng dụng Tkinter
root.mainloop()
