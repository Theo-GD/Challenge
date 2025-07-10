#CREDIT: CHATGPT

import csv
import requests
import time

# Configuration
lengths = range(4, 21)  # Word lengths from 2 to 20
words_per_length = 100
api_url = "https://random-word-api.herokuapp.com/word?length={length}&number={number}"

# Collect words by length
words_by_length = {}

for length in lengths:
    try:
        print(f"Fetching {words_per_length} words of length {length}...")
        response = requests.get(api_url.format(length=length, number=words_per_length))
        response.raise_for_status()
        words = response.json()
        words_by_length[length] = words
        time.sleep(1)  # be polite to the API
    except Exception as e:
        print(f"Error fetching words of length {length}: {e}")
        words_by_length[length] = []

# Transpose words into rows
rows = []
for i in range(words_per_length):
    row = []
    for length in lengths:
        word_list = words_by_length.get(length, [])
        word = word_list[i] if i < len(word_list) else ''
        row.append(word)
    rows.append(row)

# Write to CSV
with open('words_by_length.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Header: 2, 3, ..., 20
    writer.writerow(list(lengths))
    # Rows
    writer.writerows(rows)

print("CSV file 'words_by_length.csv' created successfully.")
