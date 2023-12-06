import re

def keep_numbers_only(line):
    # Use regex to keep only numbers
    return re.sub(r'[^0-9]', '', line)

def keep_first_and_last(number: int):
    number_to_str = str(number)
    len_str = len(number_to_str)

    if len_str == 1:
        return int(f"{number_to_str[0]}{number_to_str[0]}")

    if len_str <= 2:
        return int(number)
    
    return int(f"{number_to_str[0]}{number_to_str[len_str - 1]}")


def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            tot_number = 0
            for line in file:
                # Keep only numbers in each line
                tot_number = tot_number + keep_first_and_last(int(keep_numbers_only(line)))
            print(tot_number)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = 'input.txt'
process_file(file_path)
