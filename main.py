# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
from time import sleep

#pip install py-bgg
from libbgg.apiv1 import BGG
# You can also use version 2 of the api:
from libbgg.apiv2 import BGG as BGG2


def is_best_player_count(poll_result: list) -> bool:
    best_numvotes = float(poll_result['result'][0]['numvotes'])
    recommended_numvotes = float(poll_result['result'][1]['numvotes'])
    not_recommended_numvotes = float(poll_result['result'][2]['numvotes'])
    total_votes = float(best_numvotes + recommended_numvotes + not_recommended_numvotes)
    best_proportion = best_numvotes / total_votes
    recommended_proportion= recommended_numvotes / total_votes
    not_recommended_proportion= not_recommended_numvotes / total_votes

    return best_proportion >= recommended_proportion and best_proportion >= not_recommended_proportion


def get_recommended_player_count(poll: dict) -> list:
    player_count_results = poll['results']
    results = []
    for player_count_result in player_count_results:
        if is_best_player_count(player_count_result):
            results.append(player_count_result['numplayers'])
    return results


if __name__ == '__main__':
    bgg_client = BGG()
    # Batch gets with a list, tuple, or comma separated str
    bgg_client2 = BGG2()

    owned_boardgames = bgg_client2.get_collection(username="chichaslocas", own=1, excludesubtype="boardgameexpansion")

    for game in owned_boardgames['items']['item']:
        sleep(2)
        game_name = game.name.TEXT
        full_game = bgg_client2.boardgame(game.objectid)['items']['item']
        recommended_player_count_poll = full_game.poll[0]
        recommended_player_counts = get_recommended_player_count(recommended_player_count_poll)
        min_game_time = full_game['minplaytime']['value']
        max_game_time = full_game['maxplaytime']['value']

        print(f"{game_name} is recommended for {recommended_player_counts} players and takes between {min_game_time} and {max_game_time} minutes")
