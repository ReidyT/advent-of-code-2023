import re 

class Number:
    def __init__(self, line: int, number: int, start_pos: int, end_pos: int):
        if start_pos > end_pos:
            raise Exception('Start index must be <= than end index')

        if start_pos is None or end_pos is None:
            raise Exception('Indexes must not be None')

        self.__line = line
        self.__number = number
        self.__start_pos = start_pos
        self.__end_pos = end_pos

    def get_line(self):
        return self.__line
    def get_number(self):
        return self.__number
    def get_start_pos(self):
        return self.__start_pos
    def get_end_pos(self):
        return self.__end_pos    
    # override to check if in array
    def __eq__(self, other):
        if isinstance(other, Number):
            return self.__line == other.__line and \
                self.__number == other.__number and \
                self.__start_pos == other.__start_pos and \
                self.__end_pos == other.__end_pos
        return False

class Symbol:
    def __init__(self, line: int, symbol: str, pos: int):
        if pos is None:
            raise Exception('Index must not be None')

        self.__line = line
        self.__symbol = symbol
        self.__pos = pos

    def get_line(self):
        return self.__line
    def get_symbol(self):
        return self.__symbol
    def get_pos(self):
        return self.__pos

def construct_numbers_pos(id_line, line) -> [Number]:
    matches = re.finditer(r'\d+', line)
    # warning, match.end() give superior index end
    return [Number(id_line, int(match.group()), match.start(), match.end() - 1) for match in matches]

def construct_symbols_pos(id_line, input_string) -> [Symbol]:
    matches = re.finditer(r'\*', input_string)
    return [Symbol(id_line, match.group(), match.start()) for match in matches]

def is_touch_horizontally(number: Number, symbol_pos: int):
    number_start_pos = number.get_start_pos()
    number_end_pos = number.get_end_pos()

    return (
        (number_start_pos <= symbol_pos + 1 <= number_end_pos) or
        (number_start_pos <= symbol_pos - 1 <= number_end_pos) or
        (number_start_pos <= symbol_pos <= number_end_pos)
    )

def compute_gear(symbol: Symbol, numbers: [Number]):
    touched_numbers = []
    symbol_line = symbol.get_line()
    symbol_pos = symbol.get_pos()

    for number in numbers:
        number_line = number.get_line()

        # Check if the number touches the char horizontally
        if number_line == symbol_line and is_touch_horizontally(number, symbol_pos):
            touched_numbers.append(number.get_number())
            continue

        # Check if the number touches the char diagonally
        if (
            (number_line + 1 == symbol_line or number_line - 1 == symbol_line) and
            (is_touch_horizontally(number, symbol_pos))
        ):
            touched_numbers.append(number.get_number())
            continue

    if len(touched_numbers) == 2:
        return touched_numbers[0] * touched_numbers[1]        
    
    return 0


def get_numbers_for_line(id_line: int, all_numbers: dict):
    numbers_for_line = []
    if id_line > 0:
        numbers_for_line.extend(all_numbers[id_line - 1])

    numbers_for_line.extend(all_numbers[id_line])

    if id_line + 1 <= len(all_numbers.keys()) - 1:
        numbers_for_line.extend(all_numbers[id_line + 1])
    
    return numbers_for_line

def process_file(file_path):
    try:
        file_lines = []
        with open(file_path, 'r') as file:
            file_lines = file.read().split('\n')

        sum = 0
        all_numbers = {} # numbers per line
        all_symbols = [] # symbols per line

        for idx, line in enumerate(file_lines):
            all_numbers[idx] = construct_numbers_pos(idx, line)
            all_symbols.extend(construct_symbols_pos(idx, line))

        for symbol in all_symbols:
            numbers_for_line = get_numbers_for_line(symbol.get_line(), all_numbers)
            sum += compute_gear(symbol, numbers_for_line)

        print(sum)

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

process_file("example.txt")
process_file("input.txt")

# example = 467835
# good answer is: 75741499