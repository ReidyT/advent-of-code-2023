
def get_sets_from_line(line: str):
    splitted_line = line.replace('\n', '').split('|')
    wins = []
    for n in splitted_line[0].split(':')[1].split(' '):
        if n.isnumeric():
            wins.append(int(n))
    played = []
    for n in splitted_line[1].split(' '):
        if n.isnumeric():
            played.append(int(n))
    wins = set(wins)
    played = set(played)
    return wins, played

def count_scratch_cars(copy_cards: [], all_cards: []):
    new_count = len(copy_cards)
    for card in copy_cards:
        len_matched = card['len_matched']
        if len_matched == 0:
            continue
        first_card_copy = card['line'] # because line start with 1, current card is line - 1
        last_card_copy = first_card_copy + len_matched
        new_count += count_scratch_cars(all_cards[first_card_copy:last_card_copy], all_cards)

    return new_count

def process_file(file_path):
    try:
        cards = {}
        with open(file_path, 'r') as file:
            for idx, line in enumerate(file):
                wins, played = get_sets_from_line(line)
                len_matched_cards = len(wins.intersection(played))                
                cards[idx+1] = { 'line': idx+1, 'wins': wins, 'played': played, 'len_matched': len_matched_cards }

        tot_scratchcards = count_scratch_cars(list(cards.values()), list(cards.values()))

        print(tot_scratchcards)
    
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

process_file("example.txt")
process_file("input.txt")

# example = 30
# good answer is: 27059