
# winning combinations
WINNING_COMBINATIONS = ((0, 1, 2),
                        (3, 4, 5),
                        (6, 7, 8),
                        (0, 3, 6),
                        (1, 4, 7),
                        (2, 5, 8),
                        (0, 4, 8),
                        (2, 4, 6))

# tic tac toe logic
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def check_win(self):
        # check rows
        for row in WINNING_COMBINATIONS:
            if self.board[row[0]] == self.board[row[1]] == self.board[row[2]] != ' ':
                self.current_winner = self.board[row[0]]
                return True
        return False
    
    def check_draw(self):
        return ' ' not in self.board
    
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        return False
    
    def game_loop(self):
        turnPlayer = 'X'
        while True:
            self.print_board()
            choice = input("It's " + turnPlayer + "'s turn. Input move (0-8): ")
            try:
                choice = int(choice)
                if self.make_move(choice, turnPlayer):
                    if self.check_win():
                        self.print_board()
                        print(turnPlayer + " wins!")
                        break
                    elif self.check_draw():
                        self.print_board()
                        print("It's a draw!")
                        break
                    else:
                        if turnPlayer == 'X':
                            turnPlayer = 'O'
                        else:
                            turnPlayer = 'X'
                else: 
                    print("That square is taken.")
            except ValueError:
                print("Please type a number.")

if __name__ == '__main__':
    game = TicTacToe()
    game.game_loop()