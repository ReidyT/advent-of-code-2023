import re 

from enum import Enum

class SectionKeys(Enum): 
    SEED = 'seeds'
    SEED_TO_SOIL = 'seed-to-soil map'
    SEED_TO_FERTILIZER = 'soil-to-fertilizer map'
    FERTILIZER_TO_WATER = 'fertilizer-to-water map'
    WATER_TO_LIGHT = 'water-to-light map'
    LIGHT_TO_TEMPERATURE = 'light-to-temperature map'
    TEMPERATURE_TO_HUMIDITY = 'temperature-to-humidity map'
    HUMIDITY_TO_LOCATION = 'humidity-to-location map'

SECTION_SEPARATOR = ':'
SETS_SEPARATOR = '\n'
VALUES_SEPARATOR = ' '

def remove_starting_whitespace(input_string):
    # Use a regular expression to replace leading '\n' or ' ' with an empty string
    return re.sub(r'^[\n\s]+', '', input_string)

def get_sections_from_file(file):
    sections = file.read().split('\n\n')
    sections_map = {}
    for section in sections:
       section_and_values = section.split(SECTION_SEPARATOR)
       sections_map[section_and_values[0]] = []
       section_sets = remove_starting_whitespace(section_and_values[1]).split(SETS_SEPARATOR)
       section_sets_values = [s.split(VALUES_SEPARATOR) for s in section_sets]
       sections_map[section_and_values[0]] = section_sets_values
    return sections_map

def get_destination(source: int, arrays: [[str]]):
    idx_destination = 0
    idx_source = 1
    idx_range = 2

    for a in arrays:
        map_source_start = int(a[idx_source])
        map_range = int(a[idx_range])
        map_destination_start = int(a[idx_destination])
        if map_source_start <= source <= map_source_start + map_range - 1:
            shift = source - map_source_start
            
            # source = 55
            # map_source_start = 50
            # source - map_source_start = 5
            # destination = 52 + 5 => 57

            return map_destination_start + shift
            
    return source
            

def process_file(file_path):
    try:
        sections = {}
        with open(file_path, 'r') as file:
            sections = get_sections_from_file(file)
        
        min_location = None

        for seeds in sections[SectionKeys.SEED.value]:
            for seed in seeds:
                soil = get_destination(int(seed), sections[SectionKeys.SEED_TO_SOIL.value])
                fertilizer = get_destination(soil, sections[SectionKeys.SEED_TO_FERTILIZER.value])
                water = get_destination(fertilizer, sections[SectionKeys.FERTILIZER_TO_WATER.value])
                light = get_destination(water, sections[SectionKeys.WATER_TO_LIGHT.value])
                temperature = get_destination(light, sections[SectionKeys.LIGHT_TO_TEMPERATURE.value])
                humidity = get_destination(temperature, sections[SectionKeys.TEMPERATURE_TO_HUMIDITY.value])
                location = get_destination(humidity, sections[SectionKeys.HUMIDITY_TO_LOCATION.value])
                
                if min_location is None or location < min_location:
                    min_location = location
        print(min_location)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

process_file("example.txt")
process_file("input.txt")

# example = 35
# good answer is: 525792406