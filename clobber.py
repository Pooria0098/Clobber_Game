import pygame
import sys
import random
from collections import deque

# how to run: clobber.py dim1 dim2 opt
# dim1 = num of rows between [1 to 25]
# dim2 = num of cols between[2 to 25]
# opt = 1: comp will choose to clobber a stone from the largest connected component of white stones
# opt = 2: comp will choose to clobber a stone from the smallest connected component of white stones
# opt = 3: comp will randomly choose a white stone to clobber
# default: 6x5 board, opt = 1

p1, comp, empty = 1, 2, 0
board_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]  # red,yellow,green
player_colors = [(255, 255, 255), (0, 0, 0)]  # white, black

# check for command line args, set size of board and algorithm option
len_args = len(sys.argv)
# print(len_args)
if len_args < 3 or \
        (not sys.argv[1].isnumeric()) or int(sys.argv[1]) > 25 or int(sys.argv[1]) < 1 or \
        (not sys.argv[2].isnumeric()) or int(sys.argv[2]) > 25 or int(sys.argv[2]) < 2:
    dim = [6, 5]  # if not specified, set default row=6 col=5
else:
    dim = [int(sys.argv[1]), int(sys.argv[2])]

size = (700, 500)  # screen width,height

if dim[0] > dim[1]:
    square_size = size[1] // dim[0]
else:
    square_size = size[1] // dim[1]
# print('square_size : ', square_size)

if len_args > 3 and sys.argv[3].isnumeric() and 0 < int(sys.argv[3]) < 4:
    opt = int(sys.argv[3])
elif len_args == 2 and sys.argv[1].isnumeric():
    opt = int(sys.argv[1])
else:
    opt = 1  # default: largest connected component algo


def check_finished(board):
    # check if there are any moves left to make, ie if a black and
    # white cell are on horizontally or vertically adjacent cells
    finished = True
    for row in range(dim[0]):
        for col in range(dim[1]):
            if board[row][col] == 1:
                finished = check_if_no_neighbors(board, row, col, 1, 0)
            elif board[row][col] == 2:
                finished = check_if_no_neighbors(board, row, col, 2, 0)

            if not finished:
                return finished
    return finished


def check_if_no_neighbors(board, row, col, player, opt):
    # If the cell has a neighbor that has an opponent's stone on it,
    # return false (vertical/horizontal neighbors only)
    # if opt = 1: return the cell where that neighbor is
    if player == 1:
        check = 2
    else:
        check = 1

    if row > 0:
        if board[row - 1][col] == check:  # check up
            if opt == 1:
                return [row - 1, col]
            else:
                return False
    if row < dim[0] - 1:
        if board[row + 1][col] == check:  # check bottom
            if opt == 1:
                return [row + 1, col]
            else:
                return False
    if col > 0:
        if board[row][col - 1] == check:  # check left
            if opt == 1:
                return [row, col - 1]
            else:
                return False
    if col < dim[1] - 1:
        if board[row][col + 1] == check:  # check right
            if opt == 1:
                return [row, col + 1]
            else:
                return False

    return True


def displayText(screen, txt1, txt2, position):
    if position == "top":
        div1 = 5
        div2 = 3.5
    else:
        div1 = 2.25
        div2 = 1.75

    offset = 170

    font = pygame.font.SysFont('Times New Roman', 25)
    text = font.render(txt1, False, player_colors[0])
    text_location = ((dim[1] * square_size + (size[0] - dim[1] * square_size) - offset), size[1] // div1)
    screen.blit(text, text_location)
    text = font.render(txt2, False, player_colors[0])
    text_location = ((dim[1] * square_size + (size[0] - dim[1] * square_size) - offset), size[1] // div2)
    screen.blit(text, text_location)

    font = pygame.font.SysFont('Times New Roman', 17)
    text = font.render("Hit **SPACE** to start over", False, player_colors[0])
    text_location = ((dim[1] * square_size + (size[0] - dim[1] * square_size - 70) - offset), size[1] // 1.25)
    screen.blit(text, text_location)


def eraseSquare(selected_square, screen, board):
    # print('eraseSquare : ', selected_square)
    if (selected_square[0] % 2 == 0 and selected_square[1] % 2 == 0) or (
            selected_square[0] % 2 == 1 and selected_square[1] % 2 == 1):  # if board color 1 field
        color = board_colors[0]
    else:  # if board color 2 field
        color = board_colors[1]
    screen.fill(color, (selected_square[1] * square_size, selected_square[0] * square_size, square_size,
                        square_size))  # erase stone that was just moved
    board[selected_square[0]][selected_square[1]] = empty


def placeStone(square, player, screen, board):
    pygame.draw.circle(screen, player_colors[player - 1],
                       (square[1] * square_size + square_size // 2, square[0] * square_size + square_size // 2),
                       square_size // 2 - square_size // 10)
    board[square[0]][square[1]] = player


def setInitialBoard(board, players, screen):
    # create initial board to store occupied/empty info, fill entire board with stones for p1,comp
    for row in range(dim[0]):
        board.append([])
        for col in range(dim[1]):
            board[row].append(players[(row + col) % 2])  # 1 = p1 / 2 = comp
            # B = [[1, 2, 1, 2, 1],
            #      [2, 1, 2, 1, 2],
            #      ...
            #      ]

    # draw initial grid on screen, fill with stones
    for row in range(dim[0]):
        for col in range(dim[1]):
            if board[row][col] == 1 or board[row][col] == 2:
                idx = (board[row][col] - 1)  # for colors : "B[row][col] - 1" because list index starts from zero
                screen.fill(board_colors[idx], (col * square_size, row * square_size, square_size, square_size))
                pygame.draw.circle(screen, player_colors[idx],
                                   (col * square_size + square_size // 2, row * square_size + square_size // 2),
                                   square_size // 2 - square_size // 10)

    displayText(screen, "Moves: ", "0", "top")
    return board


def get_path_length(B, row, col):
    # starting from cell (row,col), get the length of the component of connected stones of own color
    offsets = [[0, -1], [0, 1], [1, 0], [-1, 0]]
    seen = []
    length = 1
    fringe = deque()
    fringe.append([row, col])
    add = 0
    # print('row and col : ', row, col)
    while len(fringe) > 0:
        cell_coords = fringe.popleft()
        seen.append(cell_coords)
        for offset in offsets:
            if cell_coords[0] + offset[0] >= 0 and \
                    cell_coords[0] + offset[0] < dim[0] and \
                    cell_coords[1] + offset[1] >= 0 and \
                    cell_coords[1] + offset[1] < dim[1]:
                new_cell = [cell_coords[0] + offset[0], cell_coords[1] + offset[1]]
                if new_cell not in seen:
                    if B[new_cell[0]][new_cell[1]] == 1 and new_cell not in fringe:
                        fringe.append(new_cell)
                        add += 1
        if add > 0:
            for _ in range(add):
                length += 1
            add = 0
    return length


def find_best_move(board):
    best_cell_so_far = []

    if opt == 3:  # random
        go = True
        while go:
            rowIdx = random.randint(0, dim[0] - 1)
            colIdx = random.randint(0, dim[1] - 1)
            if board[rowIdx][colIdx] == 1 and check_if_no_neighbors(board, rowIdx, colIdx, p1, 0) == False:
                best_cell_so_far = [rowIdx, colIdx]
                # print('best_cell_so_far_opt_2 : ', best_cell_so_far)
                go = False

    else:
        if opt == 1:  # largest connected component
            best_len_so_far = 0
        else:  # shortest connected component
            best_len_so_far = float("inf")

        for row in range(dim[0]):
            for col in range(dim[1]):
                # if white (human's) stone and has black nbr:
                # (note: check_if_no_neighbors returns false if there is a black nbr)
                if board[row][col] == 1 and check_if_no_neighbors(board, row, col, p1, 0) == False:
                    # find max nr of white stones in a row
                    length = get_path_length(board, row, col)
                    # print('length : ', length)

                    if opt == 1 and length > best_len_so_far:  # largest connected component
                        best_len_so_far = length
                        # print('best_len_so_far_opt_1 : ', best_len_so_far)
                        best_cell_so_far = [row, col]
                        # print('best_cell_so_far_opt_1  : ', best_cell_so_far)

                    elif opt == 2 and length < best_len_so_far:  # shortest connected component
                        best_len_so_far = length
                        # print('best_len_so_far_opt_2 : ', best_len_so_far)
                        best_cell_so_far = [row, col]
                        # print('best_cell_so_far_opt_2  : ', best_cell_so_far)

    best_move_from = check_if_no_neighbors(board, best_cell_so_far[0], best_cell_so_far[1], p1, 1)
    return [best_move_from, best_cell_so_far]


def displayWinner(player, screen):
    if player == 1:
        winner = "Black"
    else:
        winner = "White"
    displayText(screen, "Game Over", winner + " wins", "bottom")


def main():
    # initialize all pygame modules, create pygame display window
    pygame.init()
    screen = pygame.display.set_mode(size)  # surface
    clock = pygame.time.Clock()  # how fast the screen updates
    pygame.display.set_caption("Clobber")
    background_color = (84, 84, 216)
    screen.fill(background_color)  # background

    # create and display initial board, fill entire board with stones for p1, comp
    players = [p1, comp]
    B = setInitialBoard([], players, screen)

    player = p1
    square_selected = False
    running = True
    moves = 0
    while running:
        if check_finished(B):  # check if win
            displayWinner(player, screen)

        pygame.display.flip()  # display screen
        clock.tick(60)  # limit to 60 frames per second
        play = False
        while not play:  # pause game while wait for p1 event to happen
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # start over
                screen.fill(background_color)
                B = setInitialBoard([], players, screen)
                player = p1
                square_selected = False
                moves = 0
                pygame.display.flip()
            elif player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                play = True

        # human to move
        if player == 1 and play:
            click_position = pygame.mouse.get_pos()
            if click_position[0] < square_size * dim[1] and click_position[1] < square_size * dim[
                0]:  # if click within bounds of board
                idx_col = click_position[0] // square_size
                idx_row = click_position[1] // square_size
                # print('idx_row : ', idx_row)
                # print('idx_col : ', idx_col)

                if player == B[idx_row][idx_col]:  # check if player clicked own stone
                    # print('square_selected_outer : ', square_selected)
                    if square_selected != False:  # picks different (own) stone
                        # print('square_selected_inner : ', square_selected)
                        eraseSquare(square_selected, screen, B)  # erase green background from previously selected stone
                        placeStone(square_selected, player, screen, B)  # fill again with correct stone
                    square_selected = (idx_row, idx_col)  # newly selected stone
                    screen.fill(board_colors[2],
                                (idx_col * square_size, idx_row * square_size, square_size, square_size))  # paint green
                    placeStone((idx_row, idx_col), player, screen, B)

                elif B[idx_row][idx_col] != empty and player != B[idx_row][
                    idx_col] and square_selected != False:  # if chose opponent's stone to capture
                    if (idx_row == square_selected[0] and (square_selected[1] - 1 <= idx_col <= square_selected[1] + 1)) \
                            or (idx_col == square_selected[1] and (square_selected[0] - 1 <= idx_row <= square_selected[
                        0] + 1)):  # check if legal move, ie verical or horizontal neighbor
                        eraseSquare(square_selected, screen, B)  # erase square from which player moved their stone
                        placeStone((idx_row, idx_col), player, screen, B)  # replace opponent's stone with own
                        B[idx_row][idx_col] = player  # update board state
                        moves += 1
                        screen.fill(background_color, (size[0] - 170, 0, size[0], 170))
                        displayText(screen, "Moves: ", str(moves), "top")  # update nr of moves
                        if player == p1:
                            player = comp
                        else:
                            player = p1
                        square_selected = False

        # computer to move
        if check_finished(B) == False and player == comp and play == True:
            move = find_best_move(B)
            # print('AI move : ', move)
            # print('-' * 20)
            move_from = move[0]
            move_to = move[1]
            screen.fill(board_colors[2],
                        (move_from[1] * square_size, move_from[0] * square_size, square_size,
                         square_size))  # paint green
            placeStone((move_to[0], move_to[1]), player, screen, B)
            eraseSquare(move_from, screen, B)  # erase square from which player moved their stone
            play = False
            player = 1


main()
