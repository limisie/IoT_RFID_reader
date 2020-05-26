import csv
from datetime import datetime

cards_file = "data/cards.csv"
employees_file = "data/employees.csv"
logs_file = "data/logs.csv"
readers_file = "data/readers.csv"

cards = []
employees = []
readers = []


class Employee:
    employee_id_counter = 1

    def __init__(self, employee_id, name, surname, date_registered, date_unregistered):
        self.__id = employee_id
        self.__name = name
        self.__surname = surname
        self.__date_registered = date_registered
        self.__date_unregistered = date_unregistered

    def get_id(self):
        return self.__id

    def to_string(self):
        if self.__date_unregistered is None:
            string = "Pracownik {}: {} {}"
            string = string.format(self.__id, self.__name, self.__surname)
        else:
            string = "Pracownik {}: {} {}, zatrudniony {}, zwolniony {}"
            string = string.format(self.__id, self.__name, self.__surname, self.__date_registered,
                                   self.__date_unregistered)
        return string

    def get_data(self):
        if self.__date_unregistered is None:
            date_unregistered = ''
        else:
            date_unregistered = datetime.strftime(self.__date_unregistered, '%d/%m/%Y')

        return [self.__id, self.__name, self.__surname, datetime.strftime(self.__date_registered, '%d/%m/%Y'),
                date_unregistered]


class Reader:
    reader_id_counter = 1

    def __init__(self, reader_id, date_registered, date_unregistered, description):
        self.__terminal_id = reader_id
        self.__date_registered = date_registered
        self.__date_unregistered = date_unregistered
        self.__description = description

    def to_string(self):
        if self.__date_unregistered is None:
            string = "Czytnik RFID no. {}: {}"
            string = string.format(self.__terminal_id, self.__description)
        else:
            string = "Czytnik RFID no. {}: {}, zarejestrowany {}, wyrejestrowany {}"
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


class Card:

    def __init__(self, rfid_tag, employee_id, date):
        self.__rfid_tag = rfid_tag
        self.__employee_id = employee_id
        self.__date_actualized = date

    def get_user_id(self):
        return self.__employee_id

    def set_new_user(self, user_id):
        self.__employee_id = user_id
        pass

    def set_date(self, date):
        self.__date_actualized = date
        pass

    def get_id(self):
        return self.__rfid_tag

    def get_data(self):
        if self.__employee_id is -1:
            employee_id = ''
        else:
            employee_id = self.__employee_id

        return [self.__rfid_tag, employee_id, datetime.strftime(self.__date_actualized, '%d/%m/%Y')]

    def to_string(self):
        if self.__employee_id is -1:
            string = "{}: zarejestrowano {}"
            string = string.format(self.__rfid_tag, self.__date_actualized)
        else:
            string = "{}: pracownik {}, zarejestrowano {}"
            string = string.format(self.__rfid_tag, self.__employee_id, self.__date_actualized)
        return string


def __list_and_path(mode):
    return {
        'cards': (cards, cards_file),
        'employees': (employees, employees_file),
        'readers': (readers, readers_file)}[mode]


def save_changes(index, mode):
    db, file_path = __list_and_path(mode)

    file = open(file_path, "a", newline='')
    writer = csv.writer(file)

    row = db[index].get_data()
    writer.writerow(row)

    file.close()
    pass


def save_log(date, rfid_tag, reader_id):
    file = open(logs_file, "a", newline='')
    writer = csv.writer(file)

    card_index = get_index(rfid_tag, 'cards')
    if card_index == -1:
        user_id = ''
    else:
        user_id = cards[card_index].get_user_id()
        if user_id == -1:
            user_id = ''

    row = [date, rfid_tag, user_id, reader_id]
    writer.writerow(row)

    file.close()
    pass


def get_index(data_id, mode):
    items, _ = __list_and_path(mode)
    for i in range(len(items)):
        if items[i].get_id() == data_id:
            return i
    return -1


def __load_employees():
    file = open(employees_file, newline='')
    reader = csv.reader(file)

    last_id = 0

    header = next(reader)
    # header = [id, name, surname, date_registered, date_unregistered]

    for row in reader:
        index = get_index(int(row[0]), 'employees')
        if index is not -1:
            employees.pop(index)

        if row[4] is '':
            employee_id = int(row[0])
            name = row[1]
            surname = row[2]
            date_registered = datetime.strptime(row[3], '%d/%m/%Y').date()

            employees.append(Employee(employee_id, name, surname, date_registered, None))

        if int(row[0]) > last_id:
            last_id = int(row[0])

    Employee.employee_id_counter = last_id + 1
    file.close()
    pass


def __load_readers():
    file = open(readers_file, newline='')
    reader = csv.reader(file)

    last_id = 0

    header = next(reader)
    # header = [reader_id, date_registered, date_unregistered, description]

    for row in reader:
        index = get_index(int(row[0]), 'readers')
        if index is not -1:
            readers.pop(index)

        if row[2] is '':
            reader_id = int(row[0])
            date_registered = datetime.strptime(row[1], '%d/%m/%Y').date()
            description = row[3]

            readers.append(Reader(reader_id, date_registered, None, description))

        if int(row[0]) > last_id:
            last_id = int(row[0])

    Reader.reader_id_counter = last_id + 1
    file.close()
    pass


def __load_cards():
    file = open(cards_file, newline='')
    reader = csv.reader(file)

    header = next(reader)
    # header = [rfid_tag, employee_id, date_actualized]

    for row in reader:
        index = get_index(row[0], 'cards')
        if index is not -1:
            cards.pop(index)

        rfid_tag = row[0]
        if row[1] is '':
            user_id = -1
        else:
            user_id = int(row[1])
        date_actualized = datetime.strptime(row[2], '%d/%m/%Y').date()

        cards.append(Card(rfid_tag, user_id, date_actualized))

    file.close()


def load_db():
    __load_cards()
    __load_employees()
    __load_readers()
