import configparser
import csv
import os
import uuid
from datetime import datetime
from random import choice, randint, uniform


dirname = os.path.dirname(__file__)

# Настраиваем конфиги
config = configparser.ConfigParser()
config.read(os.path.join(dirname, "config.ini"), encoding='utf-8')

# В переменные записываем данные из конфига
FOLDER_PATH = config['Files']['FOLDER_PATH']
CATEGORIES = dict(config.items('Products'))

# Создаем папку data, если ее нет
if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)

# Генерируем данные для одного файла
def generate_cash_desk(shop_num, cash_num):
    file_shop = f"{FOLDER_PATH}/{shop_num}_{cash_num}.csv"
    cnt_cheks = randint(30, 50)  # Задаем количество чеков за день

    with open(file_shop, "w", newline="", encoding="utf-8") as f:
        headers = [
            "num_shop",
            "num_cash_desk",
            "dt",
            "doc_id",
            "item",
            "category",
            "amount",
            "price",
            "discount"
        ]
        writer = csv.DictWriter(f, fieldnames=headers)

        writer.writeheader()

        for _ in range(cnt_cheks):
            doc_id = str(uuid.uuid4()).replace("-", "")[:10]  # Создаем численно-буквенный идентификатор чека
            cnt_items = randint(1, 15)  # Задаем количество позиций в чеке

            for _ in range(cnt_items):  # В каждый чек добавляем товары, количество, цены, скидки
                category = choice(list(CATEGORIES.keys()))
                item = choice(eval(CATEGORIES[category]))
                amount = randint(1, 10)
                price = round(uniform(50, 10000), 2)
                discount = round(uniform(0, price * 0.3), 2)

                # Заносим в csv файл
                writer.writerow(
                    {
                        "num_shop": shop_num,
                        "num_cash_desk": cash_num,
                        "dt": datetime.today().strftime("%Y-%m-%d"),
                        "doc_id": doc_id,
                        "item": item,
                        "category": category,
                        "amount": amount,
                        "price": price,
                        "discount": discount,
                    }
                )


# Генерируем данные для всех магазинов
def generate_shops():

    # Удаляем только .csv файлы в папке DATA
    for file in os.listdir(FOLDER_PATH):
        if file.endswith('.csv'):
            os.remove(os.path.join(FOLDER_PATH, file))

    # Проверяем, не воскресенье ли сегодня
    if datetime.today().isoweekday() == 7:
        print("Магазины сегодня не работают")
        return

    shops = 6  # Задаем количество магазинов

    for shop_num in range(1, shops + 1):
        cash_desk = randint(1, 3)  # Задаем количество работающих сегодня касс в магазине
        for cash_num in range(1, cash_desk + 1):
            generate_cash_desk(shop_num, cash_num)


if __name__ == "__main__":
    generate_shops()