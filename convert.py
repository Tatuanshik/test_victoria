import csv
import json


with open('questions.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    questions_list = []

    for row in reader:
        question = row['question']
        options = row['options'].split(';')
        correct = row['correct']

        question_data = {
            "question": question,
            "options": options,
            "correct": correct
        }

        questions_list.append(question_data)


with open('questions.json', mode='w', encoding='utf-8') as json_file:
    json.dump(questions_list, json_file, indent=4, ensure_ascii=False)

print("Файл questions.json успешно создан!")
