import json

def write_dict_to_json_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Словарь успешно записан в файл {filename}.")
    except Exception as e:
        print(f"Ошибка при записи словаря в файл: {e}")

def read_dict_from_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Данные успешно считаны из файла {filename}.")
        return data
    except Exception as e:
        print(f"Ошибка при чтении данных из файла: {e}")
        return None
