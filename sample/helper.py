import csv
from datetime import datetime

cards_file = "../data/cards.csv"
employees_file = "../data/employees.csv"
readers_file = "../data/readers.csv"

cards = []
employees = []
readers = []


class Employee:
    __employee_id_counter = 0

    def __init__(self, name, surname, date_registered, date_unregistered):
        self.__id = self.__employee_id_counter
        self.__employee_id_counter += 1
        self.__name = name
        self.__surname = surname
        self.__date_registered = date_registered
        self.__date_unregistered = date_unregistered
        self.__edited = False

    def get_full_name(self):
        return str(self.__name, self.__surname)


class Reader:
    reader_id_counter = 1

    def __init__(self, reader_id, date_registered, date_unregistered, description, edited):
        self.__terminal_id = reader_id
        self.__date_registered = date_registered
        self.__date_unregistered = date_unregistered
        self.__description = description
        self.__edited = edited

    def to_string(self):
        if self.__date_unregistered is None:
            string = "Terminal {}: {}, zarejestrowany {}"
            string = string.format(self.__terminal_id, self.__description, self.__date_registered)
        else:
            string = "Terminal {}: {}, zarejestrowany {}, wyrejestrowany {}"
            string = string.format(self.__terminal_id, self.__description, self.__date_registered, self.__date_unregistered)
        return string

    def get_id(self):
        return self.__terminal_id

    def unregister(self, date):
        self.__date_unregistered = date
        pass

    def get_data(self):
        if self.__date_unregistered is None:
            date_unregistered = ''
        else:
            date_unregistered = datetime.strftime(self.__date_unregistered, '%d/%m/%Y')

        return [self.__terminal_id, datetime.strftime(self.__date_registered, '%d/%m/%Y'),
                date_unregistered, self.__description]

    def is_edited(self):
        return self.__edited

    def set_edited(self, edited):
        self.__edited = edited
        pass


class Card:

    def __init__(self, card_rfid_no, employee_id, date):
        self.__card_rfid_no = card_rfid_no
        self.__employee_id = employee_id
        self.__date_registered = date
        self.__edited = False


def __load_employees():
    pass


def __load_readers():
    file = open(readers_file, newline='')
    reader = csv.reader(file)

    last_id = 0

    header = next(reader)
    # header = [reader_id, date_registered, date_unregistered, description]

    for row in reader:
        reader_id = int(row[0])
        date_registered = datetime.strptime(row[1], '%d/%m/%Y').date()
        if row[2] is not '':
            date_unregistered = datetime.strptime(row[2], '%d/%m/%Y').date()
        else:
            date_unregistered = None
        description = row[3]

        index = get_reader_index(reader_id)
        if index is not -1:
            readers.pop(index)

        readers.append(Reader(reader_id, date_registered, date_unregistered, description, False))

        if int(row[0]) > last_id:
            last_id = int(row[0])

    Reader.reader_id_counter = last_id + 1
    pass


def get_reader_index(reader_id):
    for i in range(len(readers)):
        if readers[i].get_id() is reader_id:
            return i
    return -1


def save_changes_reader(index):
    file = open(readers_file, "a", newline='')
    writer = csv.writer(file)

    row = readers[index].get_data()
    writer.writerow(row)
    readers[index].set_edited(False)
    pass


def save_changes_readers():
    file = open(readers_file, "a", newline='')
    writer = csv.writer(file)

    for reader in readers:
        if reader.is_edited():
            row = reader.get_data()
            writer.writerow(row)
            reader.set_edited(False)
    pass


def __load_cards():
    pass


def load_db():
    __load_cards()
    __load_employees()
    __load_readers()
