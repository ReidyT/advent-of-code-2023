import re

numbers_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def extract_numbers(line):
    # solution: use positive lookahead assertion
    return re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|[0-9]))", line, flags=re.IGNORECASE)

def convert_to_number(numbers: [str]):
    new_numbers = []
    for n in numbers:
        try:
            new_numbers.append(int(n))
        except:
            new_numbers.append(numbers_map[n.lower()])
    return new_numbers 

def keep_first_and_last(numbers: [int]):
    len_arr = len(numbers)

    if len_arr == 1:
        return int(f"{numbers[0]}{numbers[0]}")
    
    return int(f"{numbers[0]}{numbers[len_arr - 1]}")


def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            tot_number = 0
            for line in file:
                # Keep only numbers in each line
                number = keep_first_and_last(convert_to_number(extract_numbers(line)))
                tot_number = tot_number + number
                print(line, number)
            print(tot_number)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = 'input.txt'
process_file(file_path)
