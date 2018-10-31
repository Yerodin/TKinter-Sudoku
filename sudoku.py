from tkinter import *
from random import *
from tkinter.filedialog import askopenfilename

name_of_game = ""
solution = list()
initial_board = list()
board = list()
difficulty = ""
selected_X = 0
selected_Y = 0
load = False


def main():
    setup_window = Tk()
    setup_window.wm_title("Sudoku Setup")
    game_name = StringVar(None, "Sudoku")
    game_name_label = Label(setup_window, text="Game Name:")
    game_name_label.pack()
    game_name_entry = Entry(setup_window,textvariable=game_name, bd=5)
    game_name_entry.pack()
    game_difficulty_label = Label(setup_window, text="Game Difficulty:")
    game_difficulty_label.pack()
    game_difficulty_list = Spinbox(setup_window,values=('Easy', 'Medium', 'Hard'), bd=5, state='readonly')
    game_difficulty_list.pack()

    def start_call_back():

        def key(event):
            handle_key_event(event, game_canvas)

        def callback(event):
            handle_mouse_event(event, game_canvas)

        def submit_call_back():
            submit_window = Tk()
            valid = True
            for i in range(0, 9):
                for j in range(0, 9):
                    if board[i][j] == 0:
                        redraw_with_selected(game_canvas, board, i, j)
                        valid = False

            for i in range(0, 9):
                candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for j in range(0, 9):
                    if board[i][j] in candidates:
                        candidates.remove(board[i][j])
                if len(candidates) > 0:
                    valid = False
            for j in range(0, 9):
                candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for i in range(0, 9):
                    if board[i][j] in candidates:
                        candidates.remove(board[i][j])
                if len(candidates) > 0:
                    valid = False

            if valid:
                for i in range(0, 9):
                    for j in range(0, 9):
                        redraw_with_selected(game_canvas, board, i, j)
                submit_label = Label(submit_window, text="Your solution is correct!\nWould you like to play again?")
                submit_label.pack()

                def yes_callback():
                    submit_window.destroy()
                    game_canvas.delete("all")
                    setup_game(name_of_game,difficulty, game_canvas, False)
                    game_window.deiconify()

                yes_button = Button(submit_window, text="Yes", command=yes_callback)
                yes_button.pack()

                def no_callback():
                    submit_window.destroy()
                    setup_window.deiconify()

                no_button = Button(submit_window, text="No", command=no_callback)
                no_button.pack()
            else:
                submit_err_label = Label(submit_window, text="Oops! The solution is incorrect!\nDo you want to continue?")
                submit_err_label.pack()

                def yes_err_callback():
                    game_window.deiconify()
                    submit_window.destroy()

                yes_err_button = Button(submit_window, text="Yes", command=yes_err_callback)
                yes_err_button.pack()

                def no_err_callback():
                    setup_window.deiconify()
                    submit_window.destroy()

                no_err_button = Button(submit_window, text="No", command=no_err_callback)
                no_err_button.pack()
            game_window.withdraw()
            submit_window.mainloop()

        def save_call_back():
            save_file_window = Tk()
            save_file_window.wm_title("Save File")
            save_file_label = Label(save_file_window, text="Enter filename:")
            save_file_label.pack()
            save_name = StringVar(None, "File Name")
            save_name_entry = Entry(save_file_window, textvariable=save_name, bd=5)
            save_name_entry.pack()

            def save_file_call_back():
                save_game(save_name_entry.get())
                save_file_window.destroy()

            save_button = Button(save_file_window, text="Save", command=save_file_call_back)
            save_button.pack()

        game_namestr = game_name.get()
        diff = game_difficulty_list.get()
        setup_window.withdraw()
        game_window = Tk()
        game_window.wm_title(game_namestr)
        game_window.bind("<Key>", key)
        game_window.bind("<Button-1>", callback)
        game_window.resizable(width=False, height=False)

        def on_closing():
            exit(0)

        game_window.protocol("WM_DELETE_WINDOW", on_closing)
        game_canvas = Canvas(game_window, bg="white", height=9*50, width=9*50)
        setup_game(game_namestr, diff, game_canvas, load)
        game_submit_button = Button(game_window, text="Submit Sudoku", command=submit_call_back)
        game_submit_button.pack()
        game_save_button = Button(game_window, text="Save Game", command=save_call_back)
        game_save_button.pack()
        game_window.mainloop()

    def load_call_back():
        global name_of_game, board, initial_board, solution, difficulty, load
        load = True
        for i in range(0, 9):
            initial_board.append([0] * 9)
        for i in range(0, 9):
            board.append([0] * 9)
        for i in range(0, 9):
            solution.append([0] * 9)
        filename = ""
        try:
            filename = askopenfilename()
            file = open(filename, "r")
            name_of_game = file.readline()
            difficulty = file.readline()
            for i in range(0, 9):
                for j in range(0, 9):
                    board[i][j] = int(file.readline())
            for i in range(0, 9):
                for j in range(0, 9):
                    initial_board[i][j] = int(file.readline())
            for i in range(0, 9):
                for j in range(0, 9):
                    solution[i][j] = int(file.readline())
            file.close()
            start_call_back()
        except:
            load = False

    game_start_button = Button(setup_window, text="Start Game", command=start_call_back)
    game_start_button.pack()
    game_load_button = Button(setup_window, text="Load Game", command=load_call_back)
    game_load_button.pack()
    setup_window.mainloop()


def setup_game(name, diff, canvas, loaded):
    global board, initial_board, solution, name_of_game, difficulty
    if not loaded:
        name_of_game = name
        difficulty = diff
        solution = generate_valid_sudoku()
        #print_grid(solution)
        grid = create_puzzle_difficulty(solution, difficulty)
        board = grid
        for i in range(0, 9):
            initial_board.append([0] * 9)
        for i in range(0, 9):
            for j in range(0,9):
                initial_board[i][j] = grid[i][j]
    if loaded:
        grid = board
    canvas = draw_grid(canvas)
    canvas = draw_selected_grid(canvas, 0, 1)
    canvas = draw_labels(grid, canvas)
    canvas.pack()


def save_game(filename):
    global name_of_game, board, initial_board, solution, difficulty
    file = open(filename, "w")
    file.write(name_of_game+"\n")
    file.write(difficulty+"\n")
    for i in range(0, 9):
        for j in range(0, 9):
            file.write(str(board[i][j])+"\n")
    for i in range(0, 9):
        for j in range(0, 9):
            file.write(str(initial_board[i][j])+"\n")
    for i in range(0, 9):
        for j in range(0, 9):
            file.write(str(solution[i][j])+"\n")
    file.close()


def redraw_with_selected(canvas, grid, i, j):
    canvas.delete("all")
    canvas = draw_labels(grid, draw_selected_grid(draw_grid(canvas), i, j))
    return canvas


def draw_selected_grid(canvas, i, j):
    global solution, initial_board
    if initial_board[j][i] == 0:
        canvas.create_rectangle(j*50, i*50, j*50+50, i*50+50, fill="green", stipple="gray50")
    else:
        canvas.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill="red", stipple="gray50")
    return canvas


def draw_grid(canvas):
    width = 9*50
    for i in range(0, 10):
        if i == 3 or i == 6:
            canvas.create_line(i*50, 0, i*50, width, fill="black", width=3)
            canvas.create_line(0, i*50, width, i*50, fill="black", width=3)
        else:
            canvas.create_line(i*50, 0, i*50, width, fill="black")
            canvas.create_line(0, i*50, width, i*50, fill="black")
    return canvas


def draw_labels(grid, canvas):
    c = Canvas()
    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] != 0:
                canvas.create_text(i*50+25, j*50+25, text=str(grid[i][j]))
    return canvas


def create_puzzle_difficulty(grid, diff):
    current_x = 0
    current_y = 0
    for i in range(0, 9):
        blanked = list()
        missing = 0
        if diff == "Easy":
            missing = randint(2, 3)
        if diff == "Medium":
            missing = randint(4, 5)
        if diff == "Hard":
            missing = randint(7, 8)
        for j in range(0, missing):
            pos = (randint(current_x, current_x+2), randint(current_y, current_y+2))
            while pos in blanked:
                pos = (randint(current_x, current_x + 2), randint(current_y, current_y + 2))
            if pos not in blanked:
                grid[pos[0]][pos[1]] = 0
                blanked.append(pos)
        if i == 0 or i == 1 or i == 3 or i == 4 or i == 6 or i == 7:
            current_y = current_y + 3
        if i == 2 or i == 5:
            current_y = 0
            current_x = current_x+3
    return grid


def generate_valid_sudoku():
    i = 0
    grid = list()
    for i in range(0, 9):
        grid.append([0] * 9)
    while not is_filled(grid):
        posx = randint(0, 8)
        posy = randint(0, 8)
        candidates = get_candidates(grid, posx, posy)
        if len(candidates) == 0:
            i = i+1
            if i == 200:
                i = 0
                grid = list()
                for i in range(0, 9):
                    grid.append([0] * 9)
            continue
        if len(candidates) > 0:
            num = randint(0, len(candidates)-1)
            grid[posx][posy] = candidates[num]
    return grid


def is_filled(grid):
    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] == 0:
                return False
    return True


def print_grid(grid):
    for i in range(0, 9):
        line = ""
        for j in range(0, 9):
            line = line + str(grid[j][i])
        print(line)


def get_candidates(grid, x, y):
    candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 9):
        if i != x:
            if grid[i][y] in candidates:
                candidates.remove(grid[i][y])
    for j in range(0, 9):
        if j != y:
            if grid[x][j] in candidates:
                candidates.remove(grid[x][j])
    a = 0
    b = 0
    if x > 2:
        a = 3
    if x > 5:
        a = 6
    if y > 2:
        b = 3
    if y > 5:
        b = 6
    for i in range(a, a+3):
        for j in range(b, b+3):
            if i != x and j != y:
                if grid[i][j] in candidates:
                    candidates.remove(grid[i][j])

    return candidates


def handle_key_event(event, canvas):
    global selected_X, selected_Y, board
    if event.char == '1':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 1
    if event.char == '2':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 2
    if event.char == '3':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 3
    if event.char == '4':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 4
    if event.char == '5':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 5
    if event.char == '6':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 6
    if event.char == '7':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 7
    if event.char == '8':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 8
    if event.char == '9':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 9
    if event.char == '0':
        if initial_board[selected_X][selected_Y] == 0:
            board[selected_X][selected_Y] = 0

    if event.char == 'w':
        selected_Y = selected_Y - 1
    if event.char == 'a':
        selected_X = selected_X - 1
    if event.char == 's':
        selected_Y = selected_Y + 1
    if event.char == 'd':
        selected_X = selected_X + 1
    if selected_Y < 0:
        selected_Y = 0
    if selected_X < 0:
        selected_X = 0
    if selected_X > 8:
        selected_X = 8
    if selected_Y > 8:
        selected_Y = 8
    redraw_with_selected(canvas, board, selected_Y, selected_X)


def handle_mouse_event(event, canvas):
    global selected_X, selected_Y, board
    xymax = 9 * 50
    x_quantum = xymax / 9
    y_quantum = xymax / 9

    selected_X = int(event.x / x_quantum)
    selected_Y = int(event.y / y_quantum)
    redraw_with_selected(canvas, board, selected_Y, selected_X)


if __name__ == '__main__':
    main()
