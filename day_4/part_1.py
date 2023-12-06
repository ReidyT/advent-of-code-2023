
def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            sum = 0
            for line in file:
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

                len_wins_mine = len(wins.intersection(played))                
                sum += 2 ** (len_wins_mine - 1) if len_wins_mine > 0 else 0
            print(sum)
    
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

process_file("example.txt")
process_file("input.txt")

# example = 13
# good answer is: 27059