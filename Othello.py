import numpy as np

EMPTY = '.'
BLACK = 'B'
WHITE = 'W'

# Directions for checking valid moves
DIRECTIONS = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

class Othello:
    def __init__(self):
        self.board = np.full((8, 8), EMPTY)
        self.board[3, 3] = self.board[4, 4] = WHITE
        self.board[3, 4] = self.board[4, 3] = BLACK
        self.current_player = BLACK

    def print_board(self):
        print("  " + " ".join(map(str, range(8))))
        for i, row in enumerate(self.board):
            print(i, " ".join(row))
        print()

    def is_valid_move(self, row, col):
        if self.board[row, col] != EMPTY:
            return False
        
        opponent = WHITE if self.current_player == BLACK else BLACK
        valid = False

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            flipped = False
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                r += dr
                c += dc
                flipped = True
            if flipped and 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.current_player:
                valid = True
        
        return valid

    def get_valid_moves(self):
        return [(r, c) for r in range(8) for c in range(8) if self.is_valid_move(r, c)]

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False

        self.board[row, col] = self.current_player
        opponent = WHITE if self.current_player == BLACK else BLACK

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            flipped = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                flipped.append((r, c))
                r += dr
                c += dc
            if flipped and 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == self.current_player:
                for fr, fc in flipped:
                    self.board[fr, fc] = self.current_player

        self.current_player = WHITE if self.current_player == BLACK else BLACK
        return True

    def is_game_over(self):
        return not self.get_valid_moves() and not Othello().get_valid_moves()

    def count_pieces(self):
        black_count = np.sum(self.board == BLACK)
        white_count = np.sum(self.board == WHITE)
        return black_count, white_count

def play_game():
    game = Othello()
    while not game.is_game_over():
        game.print_board()
        print(f"{game.current_player}'s Turn")
        moves = game.get_valid_moves()
        if not moves:
            print(f"No valid moves for {game.current_player}. Skipping turn.")
            game.current_player = WHITE if game.current_player == BLACK else BLACK

        while True:
            try:
                row, col = map(int, input("Enter row and column").split())
                if (row, col) in moves:
                    game.make_move(row, col)
                    break
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input! Enter row and column numbers.")

    game.print_board()
    black, white = game.count_pieces()
    print(f"Game Over! Final Score - Black: {black}, White: {white}")
    if black > white:
        print("Black Wins!")
    elif white > black:
        print("White Wins!")
    else:
        print("It's a Tie!")

if __name__ == "__main__":
    play_game()
