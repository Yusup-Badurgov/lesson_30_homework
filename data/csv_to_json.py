import csv
import json


def convert_csv_to_json(csv_file, json_file, model):
    with open(csv_file, 'r', encoding='utf-8') as csv_f:
        data_dict = []
        for row in csv.DictReader(csv_f):
            del row['id']
            if 'price' in row:
                row['price'] = int(row['price'])
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            data_dict.append({'model': model, 'fields': row})

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(data_dict, ensure_ascii=False))


convert_csv_to_json('ads.csv', 'ads.json', 'ads.Ad')
convert_csv_to_json('categories.csv', 'categories.json', 'ads.Category')


