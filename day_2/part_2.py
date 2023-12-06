import re
from enum import Enum

class Cubes(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

MATCH_GAME = {
    'red': 12,
    'green': 13,
    'blue': 14
}

GAME_INFO_DELIMITER = ':'
GAME_SETS_DELIMITER = ';'
GAME_CUBES_DELIMITER = ','

def keep_numbers_only(line):
    # Use regex to keep only numbers
    return int(re.sub(r'[^0-9]', '', line))

def process_set(sets: [str]):
    sets_cubes = []

    for g_set in sets:
        cubes_str = g_set.split(GAME_CUBES_DELIMITER)

        cubes = {
            'red': 0,
            'blue': 0,
            'green': 0
        }

        for cube_str in cubes_str:
            if Cubes.RED.value in cube_str:
                cubes[Cubes.RED.value] = keep_numbers_only(cube_str)
            elif Cubes.BLUE.value in cube_str:
                cubes[Cubes.BLUE.value] = keep_numbers_only(cube_str)
            elif Cubes.GREEN.value in cube_str:
                cubes[Cubes.GREEN.value] = keep_numbers_only(cube_str)
        sets_cubes.append(cubes)
    return sets_cubes

def get_game_sum(game_id: int, sets_cubes: []):
    max_cubes = {
        'red': 0,
        'blue': 0,
        'green': 0
    }

    for cubes in sets_cubes:
        if cubes[Cubes.RED.value] > max_cubes[Cubes.RED.value]:
            max_cubes[Cubes.RED.value] = cubes[Cubes.RED.value]
        if cubes[Cubes.BLUE.value] > max_cubes[Cubes.BLUE.value]:
            max_cubes[Cubes.BLUE.value] = cubes[Cubes.BLUE.value]
        if cubes[Cubes.GREEN.value] > max_cubes[Cubes.GREEN.value]:
            max_cubes[Cubes.GREEN.value] = cubes[Cubes.GREEN.value]
    return max_cubes[Cubes.RED.value] * max_cubes[Cubes.BLUE.value] * max_cubes[Cubes.GREEN.value]

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            tot_games_id = 0
            for line in file:
                game_str = line
                game_split = game_str.split(GAME_INFO_DELIMITER)
                game_id = keep_numbers_only(game_split[0])

                game_sets = game_split[1].split(GAME_SETS_DELIMITER)
                sets_cubes = process_set(game_sets)
                tot_games_id = tot_games_id + get_game_sum(game_id, sets_cubes)
            print(tot_games_id)
                
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

process_file('input.txt')