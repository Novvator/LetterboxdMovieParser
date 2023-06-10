import csv

# Define the keywords you want to filter
# keywords = ['venice', 'italy', 'hotel', 'copenhagen', 'denmark', 'waitress', 'depression', 'italian', 'hairdresser', 'parent child relationship', 'daughter', 'friendship', 'language course', 'adult education center', 'priest', 'church', 'woman director']

def filter_rows_without_keywords():
    # Open the input and output CSV files
    with open('dataset_creation/dataset_movies_from_json.csv', 'r', encoding='utf-8') as file_in, open('dataset_creation/keywords_filtered_movies.csv', 'w', newline='', encoding='utf-8') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)

        # Write the header row to the output file
        header = next(reader)
        writer.writerow(header)

        # Iterate over each row
        for row in reader:
            # Extract the keywords from the row
            row_keywords = [keyword.strip() for keyword in row[2].split(',')]

            # Check if any of the keywords are present in the row
            if row_keywords[0]:
                # Write the row to the output file
                writer.writerow(row)

def filter_rows_without_description():
    # Open the input and output CSV files
    with open('dataset_creation/keywords_filtered_movies.csv', 'r', encoding='utf-8') as file_in, open('dataset_creation/description_filtered_movies.csv', 'w', newline='', encoding='utf-8') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)

        # Write the header row to the output file
        header = next(reader)
        writer.writerow(header)

        # Iterate over each row
        for row in reader:
            # Extract the keywords from the row
            row_description = row[1].split(',')

            # Check if any of the keywords are present in the row
            if row_description[0]:
                # Write the row to the output file
                writer.writerow(row)

def filter_short_films():
    # Open the input and output CSV files
    with open('dataset_creation/description_filtered_movies.csv', 'r', encoding='utf-8') as file_in, open('dataset_creation/no_short_films_filtered.csv', 'w', newline='', encoding='utf-8') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)

        # Write the header row to the output file
        header = next(reader)
        writer.writerow(header)

        # Iterate over each row
        for row in reader:
            # Extract the keywords from the row
            row_keywords = [keyword.strip() for keyword in row[2].split(',')]

            # Check if any of the keywords are present in the row
            if 'short film' in row_keywords and len(row_keywords)==1:
                pass
            else:
                # Write the row to the output file
                writer.writerow(row)

def find_rows_no_score():
    # Open the CSV file
    with open('dataset_creation/no_short_films_filtered.csv', 'r', encoding='utf-8') as file_in, open('dataset_creation/no_average_score_lines.csv', 'w', newline='', encoding='utf-8') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)

        # Write the header row to the output file
        header = next(reader)
        writer.writerow(header)

        # Iterate over each row
        for row_number, row in enumerate(reader, start=1):
            if not row[4].replace('.', '', 1).isdigit():
                writer.writerow(str(row_number))


if __name__=="__main__":
    find_rows_no_score()