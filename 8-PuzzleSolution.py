#For counting the time used by algorithm
import time
#For popleft()
from collections import deque

#Class for puzzle state
class Puzzle:
    def __init__(self, board, x, y, depth, path):
        self.board = board
        self.x = x
        self.y = y
        self.depth = depth
        self.path = path

#Declaration of puzzle dimension
N = 3

#Print board
def print_board(board):
    for row in board:
        print(*row)
    print("--------")

#Available moves (Left, right, up, down)
row = (0,0,-1,1)
col = (-1,1,0,0)
move_names = ["Left","Right","Up","Down"]

#Check if move is valid
def isValidMove(new_x, new_y):
    return 0 <= new_x < N and 0 <= new_y < N

#Check if goal state is reached
def is_goal_state(board):
    goal = [[1,2,3],[4,5,6],[7,8,0]]
    return board == goal

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

#Function to prompt and filter user input, then convert string into list of list [[1,2,3],[4,5,6],[7,8,0]]
def user_input():
    while(True):
        requiredDigit = set("123456780")
        problem=input("\nEnter puzzle (Example: 132465708 where 0 is empty space): ")
        if len(problem) != 9:
            print("8 Puzzle requires 8 numbers + 1 empty space. Please enter again.")
            continue
        elif not problem.isdigit():
            print("The Puzzle only accepts numbers/integers. Please enter again.")
            continue
        elif set(problem) != requiredDigit:
            print("Every number from 0 to 8 must appear exactly once. Please enter again.")
        elif is_solvable(problem):
            print("This puzzle is unsolvable. Try another puzzle.")
        elif problem == "123456780":
            print("This puzzle is already in goal state. Try another puzzle.")
            continue
        else:
            problem_list=[]
            for i in range(0, len(problem), 3):
                temp_problem_list=[]
                for j in range(i,i+3):
                    temp_problem_list.append(int(problem[j]))
                problem_list.append(temp_problem_list)
            return problem_list

#Breadth-First Search Solution (BFS)
def bfs_solution(start):
    start_x, start_y = get_xy(start)
    stack = deque()
    visited = set()
    nodes_expanded = 0
    start_time = time.perf_counter()
    used_time = 0.0

    stack.append(Puzzle(start, start_x, start_y, 0, []))
    visited.add(to_tuple(start))

    while stack:
        current = stack.popleft()
        nodes_expanded += 1

        if is_goal_state(current.board):
            end_time = time.perf_counter()
            used_time = end_time - start_time
            print("Initial State:\nStep 0:")
            print_board(start)
            for i, moves in enumerate(current.path, 1):
                direction = move_names.index(moves)
                new_x = start_x + row[direction]
                new_y = start_y + col[direction]
                swap(start, start_x, start_y, new_x, new_y)
                print(f"\nStep {i}: ")
                print_board(start)
                start_x = new_x
                start_y = new_y
                
            print("\n=== SUCCESS ===")
            print(f"Goal State reached at Depth: {current.depth}")
            print(f"Total Moves Sequence: {current.path}")
            print(f"Total Moves Count: {len(current.path)}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Time Taken: {used_time:.6f} seconds")
            return

        for i in range(4):
            new_x = current.x + row[i]
            new_y = current.y + col[i]

            if isValidMove(new_x,new_y):
                new_board = [row[:] for row in current.board]

                swap(new_board,current.x,current.y,new_x,new_y)

                board_tuple = to_tuple(new_board)

                if board_tuple not in visited:
                    stack.append(Puzzle(new_board, new_x, new_y, current.depth+1, current.path + [move_names[i]]))
                    visited.add(board_tuple)

bfs_solution(user_input())