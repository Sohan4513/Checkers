class Game:
    """
    A class that represents the checkers game.
    """
    def __init__(self, player1, player2, filled_rows = 3):
        """
        Initializes a new game of checkers with the specified players and board 
        size.

        Parameters:
            player1 (Player): First player
            player2 (Player): Second player
            filled_rows (int): The number of rows with pieces for each player
        """
        # Adds players
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        # Game status
        self.winner = None
        self.loser = None
        self.tie = False
        # Creates board
        self.board = Board(filled_rows)
        self.initialize_pieces()
        # Multiple jumps
        self.current_jump = []
        self.count = 0

    def _switch_player(self):
        """
        Switches the current player.

        Parameters: None

        Returns: None
        """
        if self.current_player == self.player2:
            self.current_player = self.player1
        else:
            self.current_player = self.player2

    def _remove_piece_from_player(self, piece):
        """
        Removes the captured piece from the player class.
				
        Parameters:
            piece (Piece): The piece being removed

        Returns: None
        """
        if piece.color == self.player1.color:
            self.player1.pieces.remove(piece)
        elif piece.color == self.player2.color:
            self.player2.pieces.remove(piece)

    def initialize_pieces(self):
        """
        Places the initial pieces for each player on the board.

        Parameters: None

        Returns: None
        """
        for row in range(self.board.length):
            for col in range(self.board.length):
                if col % 2 != row % 2:
                    if row < self.board.filled_rows:
                        # Places pieces for player1
                        pieces_position = []
                        if len(self.player1.pieces) > 0:
                            for p in self.player1.pieces:
                                pieces_position.append(p.position)
                            if (row, col) not in pieces_position:
                                piece = Piece(self.player1.color, (row, col))
                                self.board.squares[row][col] = piece
                                self.player1.pieces.append(piece)
                        else:
                            piece = Piece(self.player1.color, (row, col))
                            self.board.squares[row][col] = piece
                            self.player1.pieces.append(piece)
                    elif row > self.board.filled_rows + 1:
                        # Places pieces for player2
                        pieces_position = []
                        if len(self.player2.pieces) > 0:
                            for p in self.player2.pieces:
                                pieces_position.append(p.position)
                            if (row, col) not in pieces_position:
                                piece = Piece(self.player2.color, (row, col))
                                self.board.squares[row][col] = piece
                                self.player2.pieces.append(piece)
                        else:
                            piece = Piece(self.player2.color, (row, col))
                            self.board.squares[row][col] = piece
                            self.player2.pieces.append(piece)

    def make_move(self, piece, end):
        """
        Attempts to make a move from the piece's current position to the ending
        position.

		Parameters:
	        piece (Piece): The starting piece
	        end ((int, int)): The coordinates of the place the player wants
            to move a piece to
    
		Returns:
	        bool: True if the move was successful, False otherwise
        """
        if piece is None:
            return False
        pos = piece.position
        if piece.color != self.current_player.color:
            return False
        # Checks if move is legal and removes pieces if captures are possible
        if self.move_legality(piece, end):
            self.current_jump = []
            if self.is_capture_possible(piece.position, end, piece.is_king):
                self.current_jump.append(end)
                if abs(end[0] - pos[0]) >= 2:
                    for jump in self.current_jump: 
                        mid_row = (jump[0] + pos[0]) // 2
                        mid_col = (jump[1] + pos[1]) // 2
                        mid_piece = self.board.squares[mid_row][mid_col]
                        self.board.remove_piece(mid_piece)
                        self._remove_piece_from_player(mid_piece)
                        self.board.move_piece(piece, jump)
                        pos = piece.position
                    self.current_jump = []
            else:
                end_piece = self.board.squares[end[0]][end[1]]
                if end_piece is not None:
                    return False
                else:
                    self.board.move_piece(piece, end)
            return True
        else:
            return False

    def move_legality(self, piece, end):
        """
        Returns a boolean indicating if the specified move is legal.

        Parameters:
            piece (Piece): The piece being moved
            end ((int, int)): A tuple containing the end position of a move

        Returns:
            bool: True if the move is legal, False otherwise
        """
        pos = piece.position
        if pos == end:
            return False
        # Checks if move cannot go backwards (not king piece)
        if piece in self.player1.pieces and not piece.is_king:
            if pos[0] > end[0]:
                return False    
        elif piece in self.player2.pieces and not piece.is_king:
            if pos[0] < end[0]:
                return False
        # Checks if move is within board dimensions
        if end[0] > self.board.length - 1 or end[0] < 0:
            return False
        if end[1] > self.board.length - 1 or end[1] < 0:
            return False
        # Checks if move consists of proper distance
        if abs(end[0] - pos[0]) < 3:
            if abs(end[1] - pos[1]) != abs(end[0] - pos[0]):
                return False
        elif abs(end[0] - pos[0]) > 3 and abs(end[0] - pos[0]) % 2 == 0:
            if abs(end[1] - pos[1]) % 2 != abs(end[0] - pos[0]) % 2:
                return False
        return True

    def is_capture_possible(self, start, end, is_king):
        """
        Returns a boolean indicating if a capture is possible with the 
        specified move.

        Parameters:
            start ((int, int)): A tuple containing the start position of a move
            end ((int, int)): A tuple containing the end position of a move
            is_king (bool): A boolean that verifies if a piece is a king

        Returns:
            bool: True if a capture is possible, False otherwise
        """
        # Checks for single capture (base case)
        if abs(end[0] - start[0]) == 2:
            mid_row = (end[0] + start[0]) // 2
            mid_col = (end[1] + start[1]) // 2
            end_piece = self.board.squares[end[0]][end[1]]
            mid_piece = self.board.squares[mid_row][mid_col]
            if end_piece is None:
                if mid_piece is None:
                    return False
                elif self.current_player.color == mid_piece.color:
                    return False
                elif self.current_player.color != mid_piece.color:
                    return True
                
        # Checks multiple captures (recursive)    
        elif abs(end[0] - start[0]) > 2 and abs(end[0] - start[0]) % 2 == 0\
            and abs(end[1] - start[1]) % 2 == 0:
            # Verifies captures for player1 or a king piece
            if self.current_player == self.player1 or is_king:
                # Verifies lower right captures
                if start[0] + 2 < self.board.length - 1 \
                and start[1] + 2 < self.board.length - 1:
                    pos = (start[0] + 2, start[1] + 2)
                    if pos not in self.current_jump:
                        if self.is_capture_possible\
                        (start, pos, is_king):
                            self.current_jump.append(pos)
                            if end not in self.current_jump:
                                return self.is_capture_possible\
                                (pos, end, is_king)
                # Verifies lower left captures
                if start[0] + 2 < self.board.length - 1 and start[1] - 2 > 0:
                    pos = (start[0] + 2, start[1] - 2)
                    if pos not in self.current_jump:                      
                        if self.is_capture_possible\
                        (start, pos, is_king):
                            self.current_jump.append(pos)
                            if end not in self.current_jump:                                                                   
                                return self.is_capture_possible\
                                (pos, end, is_king)
            # Verifies captures for player2 or a king piece
            if self.current_player == self.player2 or is_king:
                # Verifies upper right captures
                if start[0] - 2 > 0 and start[1] + 2 < self.board.length - 1:
                    pos = (start[0] - 2, start[1] + 2)
                    if pos not in self.current_jump:
                        if self.is_capture_possible\
                        (start, pos, is_king):
                            self.current_jump.append(pos)    
                            if end not in self.current_jump:                                                 
                                return self.is_capture_possible\
                                (pos, end, is_king)
                # Verifies upper left captures
                if start[0] - 2 > 0 and start[1] - 2 > 0:
                    pos = (start[0] - 2, start[1] - 2)
                    if pos not in self.current_jump:
                        if self.is_capture_possible\
                        (start, pos, is_king):
                            self.current_jump.append(pos)            
                            if end not in self.current_jump:      
                                return self.is_capture_possible\
                                (pos, end, is_king)
        return False

    def all_moves(self, piece):
        """
        Returns a list of the possible moves for the piece. Each 
        move is a tuple where the first value is the row index on the board
        and the second value is its column.

        Parameters:
            piece (Piece): The piece being assessed

        Returns: 
            [(int, int)]: The possible moves as a list of tuples
        """
        moves = []
        for row, pieces in enumerate(self.board.squares):
            for col, _ in enumerate(pieces):
                end = (row, col)
                pos = piece.position
                if self.board.squares[row][col] != piece:
                    if self.board.squares[row][col] is None:
                        # Checks move legality
                        if abs(end[0] - pos[0]) == 1:
                            if self.move_legality(piece, end):
                                moves.append(end)
                        else:                        
                        # Checks if capture is possible
                            if self.move_legality(piece, end):
                                self.current_jump = []
                                if self.is_capture_possible\
                                (pos, end, piece.is_king):
                                    moves.append(end)
        return moves

    def get_all_moves(self, player):
        """
        For a given player: returns a dictionary of all their pieces that 
        can move as keys and a list of their possible moves as values. Each 
        move is a tuple where the first value is the row index on the board 
        and the second value is its column.

        Parameters: 
            player (Player): The player being assessed

        Returns:
            {Piece:[(int, int)]}: All pieces that can move and their possible
            moves
        """
        all_moves = {}
        for piece in player.pieces:
            all_moves[piece] = self.all_moves(piece)
        return all_moves

    def resign(self, player):
        """
        Takes in a player who resigned and returns the opposing player who wins
        the game.

        Parameters:
            player (Player): The player resigning

        Returns: 
            str: The color of the winning player
        """
        # If player1 resigns
        if player == self.player1:
            self.player1.pieces = []
            return self.get_winner()
        # If player2 resigns
        elif player == self.player2:
            self.player2.pieces = []
            return self.get_winner()
        
    def draw(self):
        """
        Forces a tie in the game. Neither player wins.

        Parameters:
            None

        Returns: 
            None
        """
        self.tie = True
        self.get_winner()

    def get_winner(self):
        """
        Returns the color of the player who has won the game, or None if the 
        game is not over.
				
		Parameters: None

        Returns:
			str: The color of the winning player, or None if a draw is requested
            or the game is not over
        """
        # Draw requested (game is tied)
        if self.tie:
            self.player1.draws += 1
            self.player2.draws += 1
            return None
        # Player1 loses the match (no pieces left)
        if len(self.player1.pieces) == 0:
            self.winner = self.player2.name
            self.player2.wins += 1
            self.loser = self.player1.name
            self.player1.losses += 1
            return self.player2.color
        # Player2 loses the match (no pieces left)
        if len(self.player2.pieces) == 0:
            self.winner = self.player1.name
            self.player1.wins += 1
            self.loser = self.player2.name
            self.player2.losses += 1
            return self.player1.color
        # Player1 loses the match (no moves left)
        loser = True
        for _, moves in self.get_all_moves(self.player1).items():
            if moves != []:
                loser = False
        if loser:
            self.player2.wins += 1
            self.player1.losses += 1
            self.winner = self.player2.name
            self.loser = self.player1.name
            return self.player2.color
        # Player2 loses the match (no moves left)
        loser = True
        for _, moves in self.get_all_moves(self.player2).items():
            if moves != []:
                loser = False
        if loser:
            self.player1.wins += 1
            self.player2.losses += 1
            self.winner = self.player1.name
            self.loser = self.player2.name
            return self.player1.color
        # Winner not determined yet
        return None
        
class Board:
    """
    A class that represents the checkers board.
    """
    def __init__(self,filled_rows):
        """
        Initializes an empty checkers board.

        Parameters:
            filled_rows (int): Amount of rows that are filled by pieces for each
            player
        """
        self.filled_rows = filled_rows
        self.length = 2 * filled_rows + 2
        # Creates grid for checkers game
        self.squares = [[None for _ in range(self.length)]\
            for _ in range(self.length)]

    def move_piece(self, piece, end):
        """
        Places the specified piece on the board at the specified position.

        Parameters:
            piece (Piece): The piece being moved
            end ((int, int)): The coordinates of the place the player wants
            to move a piece to

        Returns: None
        """
        pos = piece.position
        self.squares[pos[0]][pos[1]] = None
        self.squares[end[0]][end[1]] = piece
        piece.change_position(end)
        # If piece becomes king
        if end[0] == 0 or end[0] == self.length - 1:
            piece.become_king()

    def remove_piece(self, piece):
        """
        Removes the captured piece from the board at the specified position.
				
        Parameters:
            piece (Piece): The piece being removed

        Returns: None
        """
        pos = piece.position
        self.squares[pos[0]][pos[1]] = None

class Piece:
    """
    A class that represents a checkers piece.
    """

    def __init__(self, color, position):
        """
        Initializes a checkers piece with the specified color and position.

        Parameters:
            color (str): The color of the piece
            position ((int, int)): The starting position of the piece
        """
        self.color = color
        self.position = position
        self.is_king = False

    def become_king(self):
        """
        Sets the piece to be a king.

        Parameters: None

        Returns: None
        """
        self.is_king = True

    def change_position(self, pos):
        """
        Changes the position of the piece.
        
        Parameters: None

        Returns: None
        """
        self.position = pos

class Player:
    """
    A class that represents a player.
    """
    def __init__(self, name, color):
        """
        Initializes a player with a name and a color.
			
        Parameters:
            name (str): The name of the player
            color (str): The color of the player's pieces
        """
        self.name = name
        # History of player's games
        self.wins = 0
        self.losses = 0
        self.draws = 0
        # Player within a checkers game
        self.color = color
        self.pieces = []