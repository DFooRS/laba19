#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import pydantic
from pydantic import BaseModel, validator, ValidationError


class Product(BaseModel):
    product: str
    shop: str
    cost: float

    @validator('product')
    def validation_prod(cls, v:str):
        if v:
            return v
        else:
            raise ValidationError("Название товара д.б строкой!")

    @validator('shop')
    def validation_shop(cls, v:str):
        if v:
            return v
        else:
            raise ValidationError("Название магазина д.б строкой!")

    @validator('cost')
    def validation_cost(cls, v:float):
        if v:
            return v
        else:
            raise ValidationError("Стоимость товара д.б числом!")


def add_product():
    """
    Ввод информации о товарах.
    """
    prod = input("Введите название товара: ")
    shop = input("Введите название магазина: ")
    cost = float(input("Введите стоимость товара: "))

    return {
        'product': prod,
        'shop': shop,
        'cost': cost
    }


def save_products(file_name, products):
    """
    Сохранить список всех товаров в формате JSON
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(products, fout, ensure_ascii=False, indent=4)


def load_products(file_name):
    """
    Загрузить список всех товаров из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)

def product_list(products):
    """
    Вывод списка товаров
    """
    line = '+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20
    )
    print(line)
    print(
        '| {:^25} | {:^15} | {:^14} |'.format(
            "Товар",
            "Магазин",
            "Стоимость"
        )
    )
    print(line)

    for product in products:
        print(
            '| {:^25} | {:^15} | {:^14} |'.format(
                product.get('product', ''),
                product.get('shop', ''),
                product.get('cost', 0)
            )
        )
    print(line)


def select(products, shop):
    """
    Выбрать товары из конкретного магазина.
    """
    result = []
    for product in products:
        if product.get('shop', '') == shop:
            result.append(product)
    return result


def get_help():
    print("Список команд:\n")
    print("add - добавить информацию о товаре;")
    print("list - вывести список товаров;")
    print("select - запросить товары из одного магазина;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")


def error(command):
    print(f"Неизвестная команда {command}", file=sys.stderr)


def main():
    """
    Главная функция программы.
    """
    products = []

    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == 'add':
            product = add_product()
            products.append(product)
            if len(products) > 1:
                products.sort(key=lambda item: item.get('shop', ''))

        elif command == 'list':
            product_list(products)

        elif command == 'select':
            sel_shop = input("Введите магазин: ")
            selected = select(products, sel_shop)
            product_list(selected)

        elif command == 'help':
            get_help()

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_products(file_name, products)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            prods = [Product(**prod) for prod in load_products(file_name)]
            for prod in prods:
                if Product.parse_obj(prod):
                    products = load_products(file_name)

        else:
            error(command)

if __name__ == '__main__':
    main()
