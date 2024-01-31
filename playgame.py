from checkers import Game, Board, Player, Piece
from typing import Tuple
import checkers as ch
import colorama 
import copy
from termcolor import colored

colorama.init()

WELCOME = "\n************************************************************\n" \
          "*                                                          *\n" \
          "*                    Welcome to Checkers!                  *\n" \
          "*                                                          *\n" \
          "************************************************************\n"

TEXT_COLORS_LST = ['red', 'green', 'blue', 'magenta', 'cyan', 'white']

def get_int_input(prompt, default=None, min_val=None, max_val=None) -> int:
    """
    Gets an integer input from the user, with optional constraints.

    Input:
        prompt: The input prompt to display.
        default: The default value to return if the user inputs nothing.
        min_val: The minimum allowed value (inclusive).
        max_val: The maximum allowed value (inclusive).
    Output:
        An integer value, or the default value if the user inputs nothing.
    """
    while True:
        try:
            raw_input = input(colored(prompt, "yellow")).strip()
            if not raw_input and default is not None:
                return default
            value = int(raw_input)
            if min_val is not None and value < min_val:
                raise ValueError(colored(f"Value must be at least {min_val}.", 'red'))
            if max_val is not None and value > max_val:
                raise ValueError(colored(f"Value must be at most {max_val}.", 'red'))
            return value
        except ValueError as e:
            print(colored(f"Invalid input: {e}\n", 'red'))

def get_yes_no_input(prompt) -> bool:
    """
    Gets a yes/no input from the user.

    Input:
        prompt: The input prompt to display.
    Output:
        True for "yes", False for "no".
    """
    while True:
        raw_input = input(colored(prompt, "yellow")).strip().lower()
        if raw_input in ('y', 'yes'):
            return True
        elif raw_input in ('n', 'no'):
            return False
        else:
            print(colored("Invalid input. Please enter 'yes' or 'no'.\n", 'red'))

def get_color_input(prompt, color_lst) -> Tuple[bool, str]:
    """
    Gets a color input from the user based off a global variable lst
    
    Input:
        prompt: The input prompt to display
    Output:
        boolean, raw_input: either run the function again or return the color
    """
    while True:
        raw_input = input(colored(prompt, "black")).strip().lower()
        if raw_input in color_lst:
            return True, raw_input
        else:
            print(colored("Invalid input. Please enter a color from the options\n", "red"))

def get_piece_prompt(prompt: str, to_move_there: str) -> Tuple[bool, int, int]:
    """
    Prompt to get the piece position from user input in formal rowcol format.

    Input:
        prompt: A string containing the prompt to display.
        to_move_there: A boolean value that is True if the input is for the position to move to,
        and False if the input is for the piece to move.

    Output:
        A tuple containing three values:
        - A boolean value indicating whether the input was valid or not.
        - An integer representing the row number of the piece.
        - An integer representing the column number of the piece.

    Raises:
        ValueError: If the user input is not in formal rowcol format.
    """

    while True:
        raw_input = input(colored(prompt, "yellow")).lower().strip()
        if (len(raw_input) == 2 and raw_input[0].isdigit()) or (len(raw_input) == 3 and raw_input[0:2].isdigit()):
            
            try:
                row, col = get_row_col(raw_input, to_move_there)
                return True, row, col
            except ValueError: 
                print(colored("Invalid input. Please enter a valid position in formal rowcol (eg 1a) \n", "red"))

        else:
            print(colored("Invalid input. Please enter a valid position in formal rowcol (eg 1a) \n", "red"))

def fill_row_prompt() -> int: 
    """
    Fill row prompt
    
    Input:
        None
    Output:
        rv (int): rows to fill
    """
    default = 3
    rv = get_int_input(f"How many filled rows per player do you want? Press Enter for {default}: ",
                         default=default, min_val=1)
    return rv

def print_board(board: list, length, real: bool) -> None:
    """
    Iterates over a Board object and returns a string representation
    of what the board looks like. 
    Pass in the current board or a board that highlights all moves.

    Input:
        array
    Output:
        None
    """
    FLOOR = "+---"
    FLOOR_END = "+"
    WALL = "|   "
    WALL_END = "|"
    POT_MOVE = "| * "
    rv = []
    even_rows = FLOOR * length + FLOOR_END

    # Create an array of strings of the board
    for row_i, row in enumerate(board):
        rv.append(even_rows)
        temp = []
        for sq_i, sq in enumerate(row):
            if sq is not None:
                if isinstance(sq, str):
                    if sq == "potential":
                        temp.append(POT_MOVE)
                        if sq_i == (length -1):
                            temp.append(WALL_END + f" {row_i +1}")
                elif isinstance(sq, ch.Piece):
                    if sq.color == p1_color:
                        if sq.is_king:
                            temp.append(P1_COLOR_BIGGER)
                        else:
                            temp.append(P1_COLOR_SMALLER)
                        if sq_i == (length -1):
                            temp.append(WALL_END + f" {row_i +1}")
                    elif sq.color == p2_color:
                        if sq.is_king:
                            temp.append(P2_COLOR_BIGGER)
                        else:
                            temp.append(P2_COLOR_SMALLER)
                        if sq_i == (length -1):
                            temp.append(WALL_END + f" {row_i +1}")

            else:
                if sq_i == (length -1):
                    temp.append(WALL + WALL_END + f" {row_i +1}")
                else:
                    temp.append(WALL)

        rv.append(''.join(temp))
    rv.append(even_rows)
    rv.append((f"  {chr(i+65)} ") for i in range(length))
    
    # Determine Header of the baord
    if real:
        print(colored("\nCurrent Board", "yellow"))
    else:
        print(colored("\nPotential Moves", "yellow"))

    # Print the board with color
    for i, lst in enumerate(rv):
        acc = ""
        for string in lst:
            acc += string
        if i == len(rv) -1:
            print(acc)
            break
        for char in acc:
            # There cannot be any colors in the list that start with the same color
            if char == p1_color[0] or char == p1_color[0].upper():
                print(colored(char, f'{p1_color}'), end='')
            elif char == p2_color[0] or char == p2_color[0].upper():
                print(colored(char, f'{p2_color}'), end='')
            elif char == "*":
                print(colored(char, "yellow"), end='')
            else:
                print(char, end='')
        print()

def get_row_col(input_string: str, to_move_there: bool) -> Tuple[int, int]: 
    """
    Gets the row and column coordinates from a user input string.

    Input:
        input_string: A string representing a chess board position in the format of "rowcol" (e.g. "1a").
        to_move_there: A boolean value indicating if the piece must exist in the input position.

    Output:
        A tuple containing the row and column integer coordinates of the input position.

    Raises:
        ValueError: If the input position is outside the board or if to_move_there is True and the input position does not contain a piece.
    """
    bound = 1
    if len(input_string) >= 3:
        bound = 2

    row = int(input_string[:bound]) - 1
    col = ord(input_string[bound:]) - ord('a')
    if row >= g.board.length or col >= g.board.length:
        raise ValueError()
    if g.board.squares[row][col] is None and not to_move_there:
        raise ValueError()
    return row, col

def convert_tuple_to_coordinate(tup: tuple) -> str:
    row = tup[0] + 1
    col = chr(tup[1] + 65)
    return f"{row}{col}"

def confirm_draw(player: Player) -> bool:
    """
    Confirms if a player wants to draw the match and returns the result.

    Input:
        player: The player to confirmt the match draw

    Output:
        A boolean value indicating if the match was successfully drawn or not.
        Returns False if the player wants to draw the match and True if the other player did not accept the draw.
    """
    draw_match = get_yes_no_input(f"{player.name}, are you sure you want to draw the match? (y/n)\n")
    if draw_match:
        print(colored("> The match is drawn!\n", "yellow"))
        return False
    elif draw_match is False:
        print(colored("> Other player did not accept draw!\n", "red"))
        g._switch_player()
        return True
    
def print_clone_board(board: list, potential) -> None:
    """
    Prints a clone board with highlighted potential moves.

    Input:
        board: A list representing the game board.
        potential: A list of tuples representing potential moves.

    Output:
        None. The board is printed to the console.
    """
    for clone_row_i, clone_row in enumerate(board):
        for clone_col_i, _ in enumerate(clone_row):
            if (clone_row_i, clone_col_i) in potential:
                board[clone_row_i][clone_col_i] = "potential"
    print_board(board, len(board), False)

def player_choice(user_input: str, current: Player):
    user_input = user_input.lower().strip()

    if user_input == 'm': 
        _, curr_pos_row, curr_pos_col = get_piece_prompt(f"> {current.name}, what piece do you want to move? rowcol (eg 1a)\n", False)
        _, new_pos_row, new_pos_col = get_piece_prompt(f"> {current.name}, where do you want to move it to? rowcol (eg 1a)\n", True)
        status = g.make_move(g.board.squares[curr_pos_row][curr_pos_col], (new_pos_row, new_pos_col))
        if not status:
            print(colored("> This move is not valid. Try again.", 'red'))
            return player_choice(user_input, current)

    elif user_input == 'p': # Potential move
        _, curr_pos_row, curr_pos_col = get_piece_prompt(f"> {current.name}, what piece do you want to see the potential moves for (eg 1a)?\n", False)
        if g.board.squares[curr_pos_row][curr_pos_col] is None:
            raise ValueError()

        clone = copy.deepcopy(g.board.squares)        
        piece = clone[curr_pos_row][curr_pos_col]
        pm_lst = g.all_moves(piece)
        in_board_form = []
        for tup in pm_lst:
            in_board_form.append(convert_tuple_to_coordinate(tup))
        print(colored(f'\n> Potential moves include:\n{", ".join(in_board_form)}\n', 'yellow'))

        print_clone_board(clone, pm_lst)
        g._switch_player()

    elif user_input == 'a': # All potential moves
        d =  g.get_all_moves(current)
        clone = copy.deepcopy(g.board.squares)
        pm = []
        moves = ""
        for key in d: # Key is a piece object
            if d[key] != []:
                key_temp = f'{convert_tuple_to_coordinate(key.position)}:'
                for tup in d[key]:
                    pm.append(tup)
                    key_temp += (convert_tuple_to_coordinate(tup) + ".")
                moves += (key_temp + "\n")     

        print(colored(f"> All potential moves include:\n{moves}", 'yellow'))
        print_clone_board(clone, pm)
        
        g._switch_player()

    elif user_input == 'd': # Draw match
        draw_match = get_yes_no_input(f"{current.name}, are you sure you want to draw the match? (y/n)\n")
        if draw_match:
            if current is g.player1:
                return confirm_draw(g.player2)
            elif current is g.player2:
                return confirm_draw(g.player1)

    elif user_input == 'f': # Forfeit match
        forfeit_match = get_yes_no_input(f"{current.name}, are you sure you want to forfeit the match? (y/n)\n")
        if forfeit_match:
            if current is g.player1:
                winner = g.player2
            elif current is g.player2:
                winner = g.player1
            print(colored(f'{current.name} has forfeited the match. {winner.name} wins!', "yellow"))
            return False
        else:
            print(colored("> Invalid input. Try again.\n", "red"))
            return player_choice(user_input, current)

    else:
        g._switch_player()
        print(colored("> Invalid input. Try again.\n", "red"))

def play_checkers(board: Board) -> None:
    """
    Plays checkers game, alternating turns between two players until the game is over or forfeited.

    Input:
        board: a CheckersBoard instance representing the game board

    Output:
        None
    """
    while True:
        current = g.current_player
        print_board(g.board.squares, g.board.length, True)

        user_input = print_options(current)

        rv = player_choice(user_input, current)

        if g.get_winner() is not None:
            print(colored(f'{current.name}, you are the winner!', "yellow"))
            break

        if rv is False: # There is a draw or forfeit, message printed earlier
            break
    
        g._switch_player()

def print_options(current: Player) -> str:
    """
    Displays the options menu for the player to choose from.

    Input:
        current: The current player object.

    Output:
        A string representing the user's input from the menu.
    """
    options = f"\n\n> {current.name} ({current.color}), What would you like to do?\n"\
              "    'm' to move piece\n"\
              "    'p' to see potential move for a specific piece\n"\
              "    'a' to see all potential moves\n"\
              "    'd' to draw match\n"\
              "    'f' to forfeit match\n"
    return input(colored(options, "black"))

def print_text_colors() -> str:
    """
    Displays a list of available text colors for the user to choose from.

    Output:
        A string prompt that lists the available text colors.
    """
    rv = ", ".join(TEXT_COLORS_LST)
    return f'> Pick a color from the following: {rv}\n'

# Introduction message
print(colored(WELCOME, 'yellow'))

# Initialize player name and player color
player1_name = input(colored("> What is the name of Player 1?\n", "black"))
_, p1_color = get_color_input(print_text_colors(), TEXT_COLORS_LST)
TEXT_COLORS_LST.remove(p1_color)
player2_name = input(colored("> What is the name of Player 2\n", "black"))
_, p2_color = get_color_input(print_text_colors(), TEXT_COLORS_LST)
filled_rows = fill_row_prompt()

# Create string of player color (regular piece and king piece)
P1_COLOR_SMALLER = f'| {p1_color[0].lower()} ' 
P1_COLOR_BIGGER = f'| {p1_color[0].upper()} '
P2_COLOR_SMALLER = f'| {p2_color[0].lower()} ' 
P2_COLOR_BIGGER = f'| {p2_color[0].upper()} '

# Initialize game
g = Game(Player(player1_name, p1_color), Player(player2_name, p2_color), filled_rows)
g.initialize_pieces()

# Play game (while loop)
play_checkers(g.board)