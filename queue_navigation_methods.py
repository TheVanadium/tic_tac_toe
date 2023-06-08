# store a list of tic tac toe games in progress
# the games are formatted as a dictionary with the key being the player who started the game
# and the value being the TicTacToe object
playersLookingForGame = {}
ongoingGames = {}

# character to seperate the players in the key of the ongoingGames dictionary
# this is used to ensure that the key is always the same regardless of the order of the players
# spacer has to be a character that is not allowed in a discord username
SPACER_CHARACTER = ':'

def make_key(user1, user2):
    return user1 + SPACER_CHARACTER + user2

# function that gets a key and determines if a user is in that game
def user_is_in_game(key, user):
    if str(user) + SPACER_CHARACTER in key or SPACER_CHARACTER + str(user) in key:
        return True
    return False

def player_is_in_ongoing_game(user):
    for k in ongoingGames:
        if user_is_in_game(k, user):
            return True
    return False

def player_is_in_game_queue(user):
    if str(user) in playersLookingForGame:
        return True
    return False