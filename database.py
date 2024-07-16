import json

game_data = []

def load_game_data(filename):
    with open(filename, "r") as file:
        for line in file:
            game = json.loads(line)
            game_data.append(game)
    game_data.sort(key=lambda x: x["id"])
