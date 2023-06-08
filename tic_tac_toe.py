
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
        self.turnPlayer = 'X'
        self.current_winner = None

    def board_to_string(self):
        return ('`| ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2] + ' |\n' +
                '| ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5] + ' |\n' +
                '| ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8] + ' |\n`')
    
    def board_to_string_with_numbers(self):
        return ('`| 0 | 1 | 2 |\n' +
                '| 3 | 4 | 5 |\n' +
                '| 6 | 7 | 8 |\n`')

    def check_win(self):
        # check rows
        for row in WINNING_COMBINATIONS:
            if self.board[row[0]] == self.board[row[1]] == self.board[row[2]] != ' ':
                self.current_winner = self.board[row[0]]
                return True
        return False
    
    def check_draw(self):
        return ' ' not in self.board and not self.check_win()
    
    def make_move(self, square):
        if self.board[square] == ' ':
            self.board[square] = self.turnPlayer
            return True
        return False
    
    def switch_turn_player(self):
        if self.turnPlayer == 'X':
            self.turnPlayer = 'O'
        else:
            self.turnPlayer = 'X'

    def game_loop(self):
        while True:
            print(self.board_to_string())
            choice = input("It's " + self.turnPlayer + "'s turn. Input move (0-8): ")
            try:
                choice = int(choice)
                if self.make_move(choice, self.turnPlayer):
                    if self.check_win():
                        print(self.board_to_string())
                        print(self.turnPlayer + " wins!")
                        break
                    elif self.check_draw():
                        print(self.board_to_string())
                        print("It's a draw!")
                        break
                    else:
                        if self.turnPlayer == 'X':
                            self.turnPlayer = 'O'
                        else:
                            self.turnPlayer = 'X'
                else: 
                    print("That square is taken.")
            except ValueError:
                print("Please type a number.")

    def victoryMessage(self):
        return self.current_winner + " wins!"

if __name__ == '__main__':
    game = TicTacToe()
    game.game_loop()