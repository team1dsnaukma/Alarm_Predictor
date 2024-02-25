import csv
import requests
from datetime import datetime

def translate_text(text, source_lang, target_lang):
    api_url = 'https://api-free.deepl.com/v2/translate'
    api_key = '-'  

    payload = {
        'auth_key': api_key,
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }

    # POST request to DeepL API
    response = requests.post(api_url, data=payload)
    translated_text = response.json()['translations'][0]['text']

    return translated_text


def translate_csv(input_file, output_file, column_index, source_lang, target_lang, start_date, end_date):
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        translated_rows = []
        for row in rows:
            try:
                row_date = datetime.strptime(row[1], '%Y-%m-%d')  
                if start_date <= row_date <= end_date:
                    translated_text = translate_text(row[column_index], source_lang, target_lang)
                    row[column_index] = translated_text
                translated_rows.append(row)
            except (ValueError, IndexError):
                translated_rows.append(row)  # Append untranslated rows

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(translated_rows)

# usage
input_file = 'filtered_data.csv'
output_file = 'filtered_translated.csv'
column_index = 2  
source_lang = 'RU'  # Source language
target_lang = 'UK'  # Target language
# 2022-02-24 - 2023-01-25
start_date = datetime(2022, 2, 24)  
end_date = datetime(2022, 8, 8)   

translate_csv(input_file, output_file, column_index, source_lang, target_lang, start_date, end_date)
