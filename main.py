from database_manager import DatabaseManager
from tkinter import ttk
from tabulate import tabulate

import tkinter as tk
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


class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book")

        logging.info("Application started")

        # Input fields
        tk.Label(root, text="First Name:").grid(row=0, column=0)
        self.first_name_var = tk.StringVar()
        first_name_entry = tk.Entry(root, textvariable=self.first_name_var)
        first_name_entry.grid(row=0, column=1)
        first_name_entry.bind('<Button-1>',
                              lambda x: self.first_name_var.set(""))

        tk.Label(root, text="Last Name:").grid(row=1, column=0)
        self.last_name_var = tk.StringVar()
        last_name_entry = tk.Entry(root, textvariable=self.last_name_var)
        last_name_entry.grid(row=1, column=1)
        last_name_entry.bind('<Button-1>',
                             lambda x: self.last_name_var.set(""))
        tk.Label(root, text="Phone Number:").grid(row=2, column=0)
        self.phone_number_var = tk.StringVar()
        tk.Entry(root, textvariable=self.phone_number_var).grid(row=2,
                                                                column=1)
        phone_entry = tk.Entry(root, textvariable=self.phone_number_var)
        phone_entry.grid(row=2, column=1)
        phone_entry.bind('<Button-1>',
                         lambda x: self.phone_number_var.set(""))
        # Address fields
        province_objects = Province.select()
        province_names = [province_object.province_name for province_object
                          in province_objects]
        tk.Label(root, text="Province:").grid(row=3, column=0)
        self.province_var = tk.StringVar()
        province_combobox = ttk.Combobox(root,
                                         textvariable=self.province_var,
                                         values=province_names)
        province_combobox.grid(row=3, column=1)

        tk.Label(root, text="City:").grid(row=4, column=0)
        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(root,
                                          textvariable=self.city_var,
                                          values=list())
        self.city_combobox.grid(row=4, column=1)

        # Update cities based on province selection
        province_combobox.bind('<<ComboboxSelected>>',
                               lambda event: self.update_cities())

        # Buttons
        tk.Button(root, text="Save", command=self.save_contact).grid(row=5,
                                                                     column=0)
        tk.Button(root, text="Load Data In Terminal",
                  command=self.load_data).grid(row=5,
                                               column=1)
        self.clear_inputs()

    @staticmethod
    def all_data_table_print():
        """print all person's information in sentences"""
        table_list = list()
        phonebook = PhoneBook.select()
        for index, contact in enumerate(phonebook):
            city_object = contact.address
            province_object = Province.select().where(
                Province.id == city_object.province).first()
            table_data = [
                contact.person.first_name,
                contact.person.last_name,
                contact.phone_number,
                province_object.province_name,
                city_object.city_name
            ]
            table_list.append(table_data)
            table_str = tabulate(table_list,
                                 headers=["First name",
                                          "Last name",
                                          "Phone number",
                                          "Province",
                                          "City"
                                          ]
                                 )
            print(table_str)

    def info_to_dict(self):
        info_dict = dict()
        if self.first_name_var.get() != "Type first name in ENG":
            info_dict["first_name"] = self.first_name_var.get()
        else:
            raise (Exception("Please enter first name"))
        if self.last_name_var.get() != "Type last name in ENG":
            info_dict["last_name"] = self.last_name_var.get()
        else:
            raise (Exception("Please enter last name"))
        if self.phone_number_var.get() != "Type Phone Number":
            if len(self.phone_number_var.get()) > 11:
                raise (Exception("Please enter a valid phone number"))
            else:
                info_dict["phone_number"] = self.phone_number_var.get()
        else:
            raise (Exception("Please enter phone_number"))
        if self.province_var.get() != "Select Province":
            info_dict["province"] = self.province_var.get()
        else:
            raise (Exception("Please select province"))
        if self.city_var.get() != "Select City":
            info_dict["city"] = self.city_var.get()
        else:
            raise (Exception("Please select city"))

        return info_dict

    def clear_inputs(self):
        self.first_name_var.set("Type first name in ENG")
        self.last_name_var.set("Type last name in ENG")
        self.phone_number_var.set("Type Phone Number")
        self.province_var.set("Select Province")
        self.city_var.set("Select City")

    def save_contact(self):
        try:
            contact_info = self.info_to_dict()
            person = Person.create(first_name=contact_info["first_name"],
                                   last_name=contact_info["last_name"],
                                   )
            phone_number = contact_info["phone_number"]
            city_object = City.select().where(City.city_name == contact_info[
                "city"]).first()
            address = city_object
            PhoneBook.create(person=person,
                             phone_number=phone_number,
                             address=address,
                             )
            self.clear_inputs()
            logging.info(f"Contact saved: {contact_info}")
        except Exception as e:
            logging.error(e)

    def load_data(self):
        try:
            self.all_data_table_print()
            logging.info("Data loaded successfully")
        except FileNotFoundError:
            logging.error("File not found.")
        except Exception as e:
            logging.error(e)

    def update_cities(self):
        province = self.province_var.get()
        # Assuming we have a predefined dictionary of provinces to cities
        province_object = Province.select().where(Province.province_name ==
                                                  province).first()
        city_objects = City.select().where(City.province == province_object)
        city_names = [city_object.city_name for city_object in city_objects]
        self.city_combobox['values'] = city_names
        self.city_combobox.current()
        logging.info(f"Cities updated for province: {province}")


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
    root = tk.Tk()
    PhoneBookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
