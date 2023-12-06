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
    matches = re.finditer(r'[^\d.]+', input_string)
    return [Symbol(id_line, match.group(), match.start()) for match in matches]

def is_touch_horizontally(number: Number, symbol_pos: int):
    number_start_pos = number.get_start_pos()
    number_end_pos = number.get_end_pos()

    return (
        (number_start_pos <= symbol_pos + 1 <= number_end_pos) or
        (number_start_pos <= symbol_pos - 1 <= number_end_pos) or
        (number_start_pos <= symbol_pos <= number_end_pos)
    )

def is_part_number(number: Number, symbols: [Symbol]):
    number_line = number.get_line()
    for symbol in symbols:
        symbol_pos = symbol.get_pos()
        symbol_line = symbol.get_line()

        # Check if the number touches the char horizontally
        if number_line == symbol_line and is_touch_horizontally(number, symbol_pos):
            return True

        # Check if the number touches the char diagonally
        if (
            (number_line + 1 == symbol_line or number_line - 1 == symbol_line) and
            (is_touch_horizontally(number, symbol_pos))
        ):
            return True
    
    return False
    
# get symbols of current line as well as prev and next line
def get_symbols_for_line(id_line: int, all_symbols: dict):
    symbols_for_line = []
    if id_line > 0:
        symbols_for_line.extend(all_symbols[id_line - 1])

    symbols_for_line.extend(all_symbols[id_line])

    if id_line + 1 < len(all_symbols.keys()) - 1:
        symbols_for_line.extend(all_symbols[id_line + 1])
    
    return symbols_for_line

def process_file(file_path):
    try:
        file_lines = []
        with open(file_path, 'r') as file:
            file_lines = file.read().split('\n')

        sum = 0
        all_numbers = []
        all_symbols = {} # symbols per line

        for idx, line in enumerate(file_lines):
            # possible to improve by not storing empty arr
            all_numbers.extend(construct_numbers_pos(idx, line))
            all_symbols[idx] = construct_symbols_pos(idx, line)

        matched = {}
        counted = []
        for number in all_numbers:
            symbols_for_line = get_symbols_for_line(number.get_line(), all_symbols)

            if is_part_number(number, symbols_for_line):
                sum = sum + number.get_number()
                counted.append(number.get_number())
                if number.get_line() not in matched:
                    matched[number.get_line()] = []
                matched[number.get_line()].append(number.get_number())

        print(sum)
    
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

process_file("example.txt")
process_file("input.txt")

# example = 4361
# good answer is: 536576