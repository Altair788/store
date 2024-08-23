import json
from pathlib import Path
from typing import Any

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Product, Category
from configs import CATALOG_DATA_PATH


class Command(BaseCommand):
    """
    Представляет класс Команда
    """

    @staticmethod
    def json_read_categories() -> list[dict[str, Any]]:
        categories_data = []
        try:
            with open(CATALOG_DATA_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

                for row in data:
                    if row["model"] == "catalog.category":
                        category_data_json = {
                            "pk": row["pk"],
                            "name": row["fields"].get("name"),
                            "description": row["fields"].get("description"),
                        }
                        categories_data.append(category_data_json)

                print("Категории успешно загружены из JSON")
                return categories_data

        except FileNotFoundError:
            print(f"Файл {CATALOG_DATA_PATH} не найден.")
        except json.JSONDecodeError:
            print("Ошибка при декодировании JSON.")
        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        return []

    @staticmethod
    def json_read_products() -> list[dict[str, Any]]:
        products_data = []
        try:
            with open(CATALOG_DATA_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

                for row in data:
                    if row["model"] == "catalog.product":
                        product_data_json = {
                            "name": row["fields"].get("name"),
                            "description": row["fields"].get("description"),
                            "preview": row["fields"].get("preview"),
                            "category": row["fields"].get("category"),
                            "price": row["fields"].get("price"),
                            "created_at": row["fields"].get("created_at"),
                            "updated_at": row["fields"].get("updated_at"),
                        }
                        products_data.append(product_data_json)

                print(
                    f"Продукты успешно загружены из JSON в количестве {len(products_data)}"
                )
                return products_data

        except FileNotFoundError:
            print(f"Файл {CATALOG_DATA_PATH} не найден.")
        except json.JSONDecodeError:
            print("Ошибка при декодировании JSON.")
        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        return []

    def handle(self, *args, **options) -> None:
        """
        Заполняет данные в БД, при этом, предварительно ее зачищает от старых данных
        """

        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_for_create = []
        products_for_create = []

        for category in Command.json_read_categories():
            categories_for_create.append(Category(**category))

        print(categories_for_create)

        Category.objects.bulk_create(categories_for_create)

        for product in Command.json_read_products():
            products_for_create.append(
                Product(
                    name=product["name"],
                    description=product["description"],
                    preview=product["preview"],
                    category=Category.objects.get(pk=product["category"]),
                    price=product["price"],
                    created_at=product["created_at"],
                    updated_at=product["updated_at"],
                )
            )

        print(products_for_create)

        Product.objects.bulk_create(products_for_create)
