import configparser
import os
from dotenv import load_dotenv
import re
import pandas as pd
from pgdb import PGDatabase

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, "config.ini"), encoding='utf-8')

FOLDER_PATH = config['Files']['FOLDER_PATH']
DATABASE = config["Database"]
load_dotenv()

database = PGDatabase(
    host=DATABASE["HOST"],
    database=DATABASE["DATABASE"],
    user=DATABASE["USER"],
    password=DATABASE["PASSWORD"] or os.getenv("PASSWORD"),
)

# SQL-запрос с плейсхолдерами
INSERT_QUERY = """
    INSERT INTO sales_shops 
    (shop_num, cash_num, dt, doc_id, item, category, amount, price, discount)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

all_files = os.listdir(FOLDER_PATH)

for file in all_files:
    # 1. Проверяем расширение csv
    if not file.endswith('.csv'):
        continue

    # 2. Проверяем формат имени: {{shop_num}}_{{cash_num}}.csv
    if not re.match(r'^\d+_\d+\.csv$', file):
        continue

    full_file_path = os.path.join(FOLDER_PATH, file)

    # 3. Извлекаем номера из имени файла
    shop_num, cash_num = file.replace('.csv', '').split('_')

    try:
        shops_data = pd.read_csv(full_file_path)

        for _, row in shops_data.iterrows():
            database.post(INSERT_QUERY, (
                int(shop_num),
                int(cash_num),
                row['dt'],
                row['doc_id'],
                row['item'],
                row['category'],
                row['amount'],
                row['price'],
                row['discount']
            ))

        # Удаляем только после успешной обработки
        os.remove(full_file_path)

    except Exception as e:
        print(f"Ошибка при обработке {file}: {repr(e)}")
