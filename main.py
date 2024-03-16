from database_manager import DatabaseManager

import peewee
import logging
import local_settings
import os
import json

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


class Person(peewee.Model):
    first_name = peewee.CharField(max_length=255,
                                  null=False,
                                  verbose_name='First name',
                                  )
    last_name = peewee.CharField(max_length=255,
                                 null=False,
                                 verbose_name='Last name',
                                 )

    class Meta:
        database = database_manager.db


class Province(peewee.Model):
    id = None
    province_name = peewee.CharField(max_length=255,
                                     null=False,
                                     verbose_name='Province name',
                                     )

    class Meta:
        database = database_manager.db


class City(peewee.Model):
    province = peewee.ForeignKeyField(model=Province,
                                      null=False,
                                      verbose_name='Province',
                                      )
    city_name = peewee.CharField(max_length=255,
                                 null=False,
                                 verbose_name='City name',
                                 )

    class Meta:
        database = database_manager.db


class PhoneBook(peewee.Model):
    person = peewee.ForeignKeyField(model=Person,
                                    null=False,
                                    verbose_name='Person'
                                    )
    address = peewee.ForeignKeyField(model=City,
                                     null=False,
                                     verbose_name='Address',
                                     )
    phone_number = peewee.CharField(max_length=11,
                                    null=False,
                                    verbose_name='Phone number',
                                    )

    class Meta:
        database = database_manager.db


class CityProvinceQuery:
    def __init__(self, base_path):
        self.provinces = list()
        cities_file_path = os.path.join(base_path, 'ir.json')

        with open(cities_file_path, 'r', encoding='utf-8') as cities_file:
            self.cities = json.load(cities_file)

    def get_all_cities(self):
        return self.cities

    def get_all_provinces(self):
        self.provinces = list()
        for city in self.cities:
            if city["admin_name"] not in self.provinces:
                self.provinces.append(city["admin_name"])
        return self.provinces


def read_all_provinces_and_add_to_db(path: str = "./city and province json/"):
    city_province = CityProvinceQuery(path)
    provinces = city_province.get_all_provinces()
    for province in provinces:
        Province.create(province_name=province)


def read_all_cities_and_add_to_db(path: str = "./city_and province json/"):
    city_province = CityProvinceQuery(path)
    cities = city_province.get_all_cities()
    for city in cities:
        province = Province.select().where(
            Province.province_name == city["admin_name"]).first()
        City.create(city_name=city["city"], province=province)


def main():
    try:
        database_manager.drop_tables(models=[PhoneBook])
        database_manager.drop_tables(models=[Person, City])
        database_manager.drop_tables(models=[Province])
        database_manager.create_tables(models=[PhoneBook,
                                               Person,
                                               City,
                                               Province])

        read_all_provinces_and_add_to_db("./city and province json/")
        read_all_cities_and_add_to_db("./city and province json/")

    except Exception as error:
        print("Error", error)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")


if __name__ == "__main__":
    main()
