import time
import heapq
import csv
import os
from collections import deque
from itertools import count

#Config of Puzzle
N = 3
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
GOAL_FLAT = "123456780"
GOAL_POS = {}
for _i in range(N):
    for _j in range(N):
        GOAL_POS[GOAL[_i][_j]] = (_i, _j)

#Class for puzzle state
class Puzzle:
    def __init__(self, board, x, y, depth, path, cost=0):
        self.board = board
        self.x = x
        self.y = y
        self.depth = depth
        self.path = path
        self.cost = cost


#Print board
def print_board(board):
    for row in board:
        print(*row)
    print("--------")

#Available moves (Left, right, up, down)
row_moves = (0,0,-1,1)
col_moves = (-1,1,0,0)
move_names = ["Left","Right","Up","Down"]

#Check if move is valid
def isValidMove(new_x, new_y):
    return 0 <= new_x < N and 0 <= new_y < N

#Check if goal state is reached
def is_goal_state(board):
    return board == GOAL

#List to Tuple
def to_tuple(board):
    return tuple(map(tuple, board))

#Function to get the location of 0 in string from user_input
def get_xy(board):
    for i, row in enumerate(board,0):
        if 0 in row:
            x=i
            y=row.index(0)
    return x,y

#Turn str into 3x3 list
def str_to_board(str):
    board = []
    for i in range(0, 9, 3):
        board.append([int(str[j]) for j in range(i, i + 3)])
    return board

#Check if solvable
def is_solvable(problem_str):
    inversion = 0
    problem_str.replace("0","")

    for i in range(8):
        if int(problem_str[i])>int(problem_str[i+1]):
            inversion += 1
    
    return inversion % 2 == 0

#Swap value in puzzle
def swap(board, old_x, old_y, new_x, new_y):
    board[old_x][old_y], board[new_x][new_y] = board[new_x][new_y], board[old_x][old_y]

#Count misplaced tiles
def misplaced_tiles(board):
    total = 0
    for i in range(N):
        for j in range(N):
            v = board[i][j]
            if v != 0 and v != GOAL[i][j]:
                total += 1
    return total

def manhattan_distance(board):
    total = 0
    for i in range(N):
        for j in range(N):
            v = board[i][j]
            if v != 0:
                gi, gj = GOAL_POS[v]
                total += abs(gi - i) + abs(gj - j)
    return total

def get_neighbors(board, x, y):
    neighbors = []
    for i in range(4):
        nx, ny = x + row_moves[i], y + col_moves[i]
        if isValidMove(nx, ny):
            new_board = [r[:] for r in board]
            swap(new_board, x, y, nx, ny)
            neighbors.append((new_board, nx, ny, move_names[i]))
    return neighbors

#For replay solution path
def reconstruct_and_print(start_board, path):
    board = [r[:] for r in start_board]
    x, y = get_xy(board)
    print("Initial State:\nStep 0:")
    print_board(board)
    for i, mv in enumerate(path, 1):
        d = move_names.index(mv)
        nx, ny = x + row_moves[d], y + col_moves[d]
        swap(board, x, y, nx, ny)
        print(f"\nStep {i}: (Move blank {mv})")
        print_board(board)
        x, y = nx, ny

#Function to prompt and filter user input, then convert string into list of list [[1,2,3],[4,5,6],[7,8,0]]
def user_input():
    while(True):
        requiredDigit = set("123456780")
        problem=input("\nEnter puzzle (Example: 132465708 where 0 is empty space), or 'c' to cancel: ").strip()
        if problem.lower() == "c":
            return None
        elif len(problem) != 9:
            print("8 Puzzle requires 8 numbers + 1 empty space. Please enter again.")
            continue
        elif not problem.isdigit():
            print("The Puzzle only accepts numbers/integers. Please enter again.")
            continue
        elif set(problem) != requiredDigit:
            print("Every number from 0 to 8 must appear exactly once. Please enter again.")
            continue
        elif is_solvable(problem):
            print("This puzzle is unsolvable. Try another puzzle.")
            continue
        elif problem == "123456780":
            print("This puzzle is already in goal state. Try another puzzle.")
            continue
        else:
            return problem

#10 Hardcode puzzles with different difficulty for quick test case
TEST_PUZZLES = [
    {"id": "T1",  "puzzle": "412053786", "difficulty": "Easy",   "optimal_depth": 5},
    {"id": "T2",  "puzzle": "123560478", "difficulty": "Easy",   "optimal_depth": 5},
    {"id": "T3",  "puzzle": "103426758", "difficulty": "Easy",   "optimal_depth": 3},
    {"id": "T4",  "puzzle": "203168475", "difficulty": "Medium", "optimal_depth": 9},
    {"id": "T5",  "puzzle": "123748605", "difficulty": "Medium", "optimal_depth": 9},
    {"id": "T6",  "puzzle": "253107486", "difficulty": "Medium", "optimal_depth": 10},
    {"id": "T7",  "puzzle": "162743508", "difficulty": "Medium", "optimal_depth": 9},
    {"id": "T8",  "puzzle": "541706823", "difficulty": "Hard",   "optimal_depth": 18},
    {"id": "T9",  "puzzle": "173406285", "difficulty": "Hard",   "optimal_depth": 20},
    {"id": "T10", "puzzle": "451638720", "difficulty": "Hard",   "optimal_depth": 18},
]

#Breadth-First Search Solution (BFS)
def bfs_solution(start, verbose=True):
    start_x, start_y = get_xy(start)
    frontier = deque()
    visited = set()
    nodes_expanded = 0
    max_frontier = 1
    start_time = time.perf_counter()
    used_time = 0.0

    frontier.append(Puzzle(start, start_x, start_y, 0, []))
    visited.add(to_tuple(start))

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        current = frontier.popleft()
        nodes_expanded += 1

        if is_goal_state(current.board):
            used_time = (time.perf_counter() - start_time)*1000
            if verbose:
                reconstruct_and_print(start, current.path)
            return {
                "algorithm": "BFS",
                "solved": True,
                "path": current.path,
                "moves": len(current.path),
                "nodes_expanded": nodes_expanded,
                "max_frontier": max_frontier,
                "time_ms": used_time
            }

        for new_board, nx, ny, mv in get_neighbors(current.board, current.x, current.y):
            t = to_tuple(new_board)
            if t not in visited:
                visited.add(t)
                frontier.append(Puzzle(new_board, nx, ny, current.depth + 1, current.path + [mv]))

    used_time = (time.perf_counter() - start_time)*1000
    return {
        "algorithm": "BFS", "solved": False, "path": [], "moves": None,
        "nodes_expanded": nodes_expanded, "max_frontier": max_frontier, "time_ms": used_time,
    }

#Greedy Best-First Search
def greedy_solution(start_board, heuristic=manhattan_distance, verbose=True):
    start_x, start_y = get_xy(start_board)
    visited = set()
    nodes_expanded = 0
    max_frontier = 1
    tie_breaker = count()
    start_time = time.perf_counter()

    h0 = heuristic(start_board)
    heap = [(h0, next(tie_breaker), Puzzle(start_board, start_x, start_y, 0, []))]
    visited.add(to_tuple(start_board))

    while heap:
        max_frontier = max(max_frontier, len(heap))
        _, _, current = heapq.heappop(heap)
        nodes_expanded += 1

        if is_goal_state(current.board):
            used_time = (time.perf_counter() - start_time)*1000
            if verbose:
                reconstruct_and_print(start_board, current.path)
            return {
                "algorithm": "Greedy Best-First",
                "solved": True,
                "path": current.path,
                "moves": len(current.path),
                "nodes_expanded": nodes_expanded,
                "max_frontier": max_frontier,
                "time_ms": used_time,
            }

        for new_board, nx, ny, mv in get_neighbors(current.board, current.x, current.y):
            t = to_tuple(new_board)
            if t not in visited:
                visited.add(t)
                hn = heuristic(new_board)
                heapq.heappush(
                    heap,
                    (hn, next(tie_breaker), Puzzle(new_board, nx, ny, current.depth + 1, current.path + [mv])),
                )

    used_time = (time.perf_counter() - start_time)*1000
    return {
        "algorithm": "Greedy Best-First", "solved": False, "path": [], "moves": None,
        "nodes_expanded": nodes_expanded, "max_frontier": max_frontier, "time_ms": used_time,
    }

#A Star Search
def astar_solution(start_board, heuristic=manhattan_distance, verbose=True):
    start_x, start_y = get_xy(start_board)
    best_g = {}
    nodes_expanded = 0
    max_frontier = 1
    tie_breaker = count()
    start_time = time.perf_counter()

    g0 = 0
    h0 = heuristic(start_board)
    heap = [(g0 + h0, next(tie_breaker), Puzzle(start_board, start_x, start_y, 0, [], g0))]
    best_g[to_tuple(start_board)] = g0

    while heap:
        max_frontier = max(max_frontier, len(heap))
        _, _, current = heapq.heappop(heap)
        nodes_expanded += 1

        if is_goal_state(current.board):
            used_time = (time.perf_counter() - start_time) * 1000  # milliseconds
            if verbose:
                reconstruct_and_print(start_board, current.path)
            return {
                "algorithm": "A*",
                "solved": True,
                "path": current.path,
                "moves": len(current.path),
                "nodes_expanded": nodes_expanded,
                "max_frontier": max_frontier,
                "time_ms": used_time,
            }

        for new_board, nx, ny, mv in get_neighbors(current.board, current.x, current.y):
            t = to_tuple(new_board)
            g_new = current.cost + 1
            if t not in best_g or g_new < best_g[t]:
                best_g[t] = g_new
                h_new = heuristic(new_board)
                heapq.heappush(
                    heap,
                    (g_new + h_new, next(tie_breaker),
                     Puzzle(new_board, nx, ny, current.depth + 1, current.path + [mv], g_new)),
                )

    used_time = (time.perf_counter() - start_time) * 1000  # milliseconds
    return {
        "algorithm": "A*", "solved": False, "path": [], "moves": None,
        "nodes_expanded": nodes_expanded, "max_frontier": max_frontier, "time_ms": used_time,
    }

#To run all algorithms
def solve_all(board_list, verbose=False):
    results = []
    solvers = [
        (lambda b, v: bfs_solution(b, v), ),
        (lambda b, v: greedy_solution(b, manhattan_distance, v), ),
        (lambda b, v: astar_solution(b, manhattan_distance, v), ),
    ]
    for (solver,) in solvers:
        board_copy = [r[:] for r in board_list]
        results.append(solver(board_copy, verbose))

    optimal_moves = next((r["moves"] for r in results if r["algorithm"] == "BFS" and r["solved"]), None)
    for r in results:
        r["optimal"] = bool(r["solved"] and optimal_moves is not None and r["moves"] == optimal_moves)
    return results

#Display result
def print_results_table(results, puzzle=None, difficulty=None):
    if puzzle:
        print(f"\nPuzzle: {puzzle}   Difficulty: {difficulty}")
    header = f"{'Algorithm':<20}{'Solved':<8}{'Moves':<8}{'Nodes Exp.':<12}{'Max Frontier':<14}{'Time (ms)':<14}{'Optimal':<8}"
    print(header)
    print("-" * len(header))
    for r in results:
        moves = r["moves"] if r["moves"] is not None else "N/A"
        print(
            f"{r['algorithm']:<20}"
            f"{('Yes' if r['solved'] else 'No'):<8}"
            f"{str(moves):<8}"
            f"{r['nodes_expanded']:<12}"
            f"{r['max_frontier']:<14}"
            f"{r['time_ms']:<14.3f}"
            f"{('Yes' if r['optimal'] else 'No'):<8}"
        )

#Display history
def show_history(puzzle_history):
    if not puzzle_history:
        print("\nNo puzzles have been solved yet in this session.")
        return
    print("\n" + "=" * 60)
    print(" PUZZLE HISTORY")
    print("=" * 60)
    for entry in puzzle_history:
        print(f"\n[{entry['id']}] Puzzle: {entry['puzzle']}  Difficulty: {entry['difficulty']}")
        print_results_table(entry["results"])

#Display result summary for 10 test cases
def show_test_summary(entries):
    print("\n" + "=" * 90)
    print(" TEST PUZZLE PERFORMANCE SUMMARY (10 hardcoded puzzles)")
    print("=" * 90)
    for entry in entries:
        print_results_table(entry["results"], puzzle=entry["puzzle"], difficulty=entry["difficulty"])

#For csv export
CSV_FIELDS = [
    "Puzzle_ID", "Puzzle_String", "Difficulty", "Algorithm",
    "Solved", "Optimal", "Moves", "Nodes_Expanded",
    "Max_Frontier_Size", "Time_Taken_ms",
]


def build_csv_row(pid, puzzle_str, difficulty, r):
    return {
        "Puzzle_ID": pid,
        "Puzzle_String": puzzle_str,
        "Difficulty": difficulty,
        "Algorithm": r["algorithm"],
        "Solved": "Yes" if r["solved"] else "No",
        "Optimal": "Yes" if r["optimal"] else "No",
        "Moves": r["moves"] if r["moves"] is not None else "N/A",
        "Nodes_Expanded": r["nodes_expanded"],
        "Max_Frontier_Size": r["max_frontier"],
        "Time_Taken_ms": round(r["time_ms"], 3),
    }


def export_csv(all_results):
    if not all_results:
        print("\nNo results available yet. Solve at least one puzzle first (menu option 1 or 3).")
        return

    filename = input("Enter CSV filename to save (default: puzzle_results.csv): ").strip()
    if not filename:
        filename = "puzzle_results.csv"
    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"\nResults successfully exported to: {os.path.abspath(filename)}")
    except OSError as e:
        print(f"\nFailed to write CSV file: {e}")

#Main program loop
def main():
    puzzle_history = []
    all_results = []
    next_id = 1

    print("=" * 60)
    print("   8-PUZZLE AI SEARCH SOLVER")
    print("   BFS  |  Greedy Best-First  |  A*")
    print("=" * 60)

    while True:
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("-" * 60)
        print("1. Enter a custom puzzle and solve (BFS + Greedy + A*)")
        print("2. View puzzle history (this session)")
        print("3. Run the 10 hardcoded test puzzles (Easy/Medium/Hard)")
        print("4. View performance results table (all puzzles solved so far)")
        print("5. Export all results to CSV")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            flat = user_input()
            if flat is None:
                print("Cancelled.")
                continue
            board_list = str_to_board(flat)
            results = solve_all(board_list, verbose=True)
            entry = {"id": next_id, "puzzle": flat, "difficulty": "Custom", "results": results}
            puzzle_history.append(entry)
            for r in results:
                all_results.append(build_csv_row(next_id, flat, "Custom", r))
            next_id += 1
            print("\n=== PERFORMANCE SUMMARY ===")
            print_results_table(results)

        elif choice == "2":
            show_history(puzzle_history)

        elif choice == "3":
            print("\nRunning all 10 hardcoded test puzzles through BFS, Greedy Best-First and A*...")
            new_entries = []
            for p in TEST_PUZZLES:
                board_list = str_to_board(p["puzzle"])
                results = solve_all(board_list, verbose=False)
                entry = {"id": p["id"], "puzzle": p["puzzle"], "difficulty": p["difficulty"], "results": results}
                puzzle_history.append(entry)
                new_entries.append(entry)
                for r in results:
                    all_results.append(build_csv_row(p["id"], p["puzzle"], p["difficulty"], r))
            print("Done.")
            show_test_summary(new_entries)

        elif choice == "4":
            if not puzzle_history:
                print("\nNo results yet. Try option 1 or option 3 first.")
            else:
                print("\n" + "=" * 90)
                print(" ALL PERFORMANCE RESULTS")
                print("=" * 90)
                for entry in puzzle_history:
                    print_results_table(entry["results"], puzzle=entry["puzzle"], difficulty=entry["difficulty"])

        elif choice == "5":
            export_csv(all_results)

        elif choice == "6":
            print("\nExiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()