from GlickoPlayer import GlickoPlayer
import json
import datetime

def create_player(player_name: str):
    with open('elo.json', 'r') as f:
        data = json.load(f)
    new_player = GlickoPlayer(player_name)
    data[player_name] = new_player.to_json_dict()
    with open('elo.json', 'w') as f:
        json.dump(data, f)

# if the player is not in the json file, create a new player
def get_player_stat(player_name: str, stat: str):
    if stat not in ['rating', 'rd', 'vol', 'last_game_date']: raise ValueError('Invalid stat')
    with open('elo.json', 'r') as f:
        data = json.load(f)
    if player_name not in data: return None
    return int(data[player_name][stat])

# function to update player statistics after a game
# if the player is not in the database, create a new player
def update_player_stats(winner_player_name: str, loser_player_name: str, is_tie: bool = False):
    with open('elo.json', 'r') as f:
        data = json.load(f)
    if winner_player_name not in data:
        create_player(winner_player_name)
    if loser_player_name not in data:
        create_player(loser_player_name)

    # get the updated data
    with open('elo.json', 'r') as f:
        data = json.load(f) 

    # get datetimes
    # datetimes are stored as strings so we have to convert them back to datetime objects
    # they might also be none so we have to check for that
    winner_last_game_date = datetime.datetime.strptime(data[winner_player_name]['last_game_date'], "%Y-%m-%d %H:%M:%S") if data[winner_player_name]['last_game_date'] is not None else None
    loser_last_game_date = datetime.datetime.strptime(data[loser_player_name]['last_game_date'], "%Y-%m-%d %H:%M:%S") if data[loser_player_name]['last_game_date'] is not None else None

    winner_player = GlickoPlayer(winner_player_name, data[winner_player_name]['rating'], data[winner_player_name]['rd'], data[winner_player_name]['vol'], winner_last_game_date)
    loser_player = GlickoPlayer(loser_player_name, data[loser_player_name]['rating'], data[loser_player_name]['rd'], data[loser_player_name]['vol'], loser_last_game_date)
    
    if is_tie:
        winner_player.update_rating(loser_player, 0.5)
        loser_player.update_rating(winner_player, 0.5)
    else:
        winner_player.update_rating(loser_player, 1)
        loser_player.update_rating(winner_player, 0)

    data[winner_player_name] = winner_player.to_json_dict()
    data[loser_player_name] = loser_player.to_json_dict()
    with open('elo.json', 'w') as f:
        json.dump(data, f)

# get top 10 players, sorted by rating, then append the player to the leaderboard with their rank if they aren't in the top 10
def get_leaderboard(player: str=None, num_players=10):
    with open('elo.json', 'r') as f:
        data = json.load(f)
    leaderboard = []
    for player_name in data:
        if data[player_name]['rd'] >= 100: continue
        leaderboard.append((player_name, data[player_name]['rating']))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    if player not in [x[0] for x in leaderboard]:
        player_rating = get_player_stat(player, 'rating')
        if player_rating is None: player_rating = 1500
        leaderboard.append((player, player_rating))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard[:num_players]



if __name__ == '__main__':
    create_player('test_player_1')
    update_player_stats('test_player_2', 'test_player_3')
    update_player_stats('test_player_4', 'test_player_5', True)