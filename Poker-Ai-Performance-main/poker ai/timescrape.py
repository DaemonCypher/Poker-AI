import re
# search trough a file and finds key word and sums up the seconds 
def search_and_sum_time(file_path, search_text):
    total_time = 0.0
    time_pattern = re.compile(r'Time taken to play: ([\d.]+) seconds For ' + search_text)

    with open(file_path, 'r') as file:
        for line in file:
            match = time_pattern.search(line)
            if match:
                time_value = float(match.group(1))
                total_time += time_value
    return total_time

file_path = 'log.txt'  
search_text = 'Fish player'

total_time = search_and_sum_time(file_path, search_text)

print(f'Total time taken for "{search_text}": {total_time:.10f} seconds')
