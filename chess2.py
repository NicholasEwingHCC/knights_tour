import multiprocessing, time

all_points = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)
]

ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
columns_to_files = {v: k for k, v in files_to_columns.items()}

def getChessNotation(piece) -> str:
    return columns_to_files[piece[1]] + rows_to_ranks[piece[0]]

def getKnightMoves(row, column):
    valid_positions = []
    knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    for m in knight_moves:
        end_row = row + m[0]
        end_column = column + m[1]
        if 0 <= end_row <= 7 and 0 <= end_column <= 7:
            valid_positions.append((end_row, end_column))
            
    return valid_positions

def thread_handler(start_point: tuple):
    start_time = time.time()
    step = 1

    board = [["--" for i in range(8)]for i in range(8)]
    board[start_point[0]][start_point[1]] = f"{step:02d}"

    if solve(board, start_point, step+1): 
        with open(("solutions/" + getChessNotation(start_point) + ".txt"), "w") as file:
            file.write("Knight's Tour output for starting point " + getChessNotation(start_point) + ":\n\n")
            for line in board:
                for item in line:
                    file.write(item + " ")
                file.write("\n")
    else:
        print("Failed to find solution for point " + getChessNotation(start_point) + ".")
        return False
        
    end_time = time.time()
    print("Thread for point " + getChessNotation(start_point) + " took " + str((end_time-start_time) * 10**3) + " ms ")

def solve(board, point, step) -> bool:
    if step == 65:
        return True

    moves = getKnightMoves(point[0], point[1])
    moves.sort(key=lambda l: len(getKnightMoves(l[0], l[1])))

    for move in moves:
        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7 and board[move[0]][move[1]] == "--":
            board[move[0]][move[1]] = f"{step:02d}"
            if solve(board, (move[0], move[1]), step+1):
                return True
            board[move[0]][move[1]] = "--"
    return False

if __name__ == "__main__":
    main_start_time = time.time()
    processes = []
    for point in all_points:
        processes.append(multiprocessing.Process(target=thread_handler, args=(point,)))
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print("Final completion time:", (time.time()-main_start_time), " Seconds ")