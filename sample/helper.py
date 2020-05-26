import csv

cards_file = "data/cards.csv"
employees_file = "data/employees.csv"
logs_file = "data/logs.csv"
readers_file = "data/readers.csv"
report = './data/report.csv'

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

    def unregister(self, date):
        self.__date_unregistered = date
        pass

    def get_full_name(self):
        return self.__name + ' ' + self.__surname

    def to_string(self):
        if self.__date_unregistered == '':
            string = "Pracownik {}: {} {}"
            string = string.format(self.__id, self.__name, self.__surname)
        else:
            string = "Pracownik {}: {} {}, zatrudniony {}, zwolniony {}"
            string = string.format(self.__id, self.__name, self.__surname, self.__date_registered,
                                   self.__date_unregistered)
        return string

    def get_data(self):
        return [self.__id, self.__name, self.__surname, self.__date_registered, self.__date_unregistered]


class Reader:
    reader_id_counter = 1

    def __init__(self, reader_id, date_registered, date_unregistered, description):
        self.__terminal_id = reader_id
        self.__date_registered = date_registered
        self.__date_unregistered = date_unregistered
        self.__description = description

    def to_string(self):
        if self.__date_unregistered == '':
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
        return [self.__terminal_id, self.__date_registered, self.__date_unregistered, self.__description]


class Card:

    def __init__(self, rfid_tag, employee_id, date):
        self.__rfid_tag = rfid_tag
        self.__employee_id = employee_id
        self.__date_actualized = date

    def get_employee_id(self):
        return self.__employee_id

    def set_new_employee(self, employee_id):
        self.__employee_id = employee_id
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

        return [self.__rfid_tag, employee_id, self.__date_actualized]

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


def get_index(data_id, mode):
    items, _ = __list_and_path(mode)
    for i in range(len(items)):
        if items[i].get_id() == data_id:
            return i
    return -1


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
        employee_id = ''
    else:
        employee_id = cards[card_index].get_employee_id()
        if employee_id == -1:
            employee_id = ''

    row = [date, rfid_tag, employee_id, reader_id]
    writer.writerow(row)

    file.close()
    pass


def print_report(employee_id):
    index = get_index(employee_id, 'employees')

    logs = open(logs_file, newline='')
    reader = csv.reader(logs)
    file = open(report, 'w', newline='')
    writer = csv.writer(file)

    # logs_header = date, rfid_id, employee_id, reader_id
    header = ['time', 'rfid_id', 'reader_id', 'reader_name']
    next(reader)

    for row in reader:
        if row[2] is not '':
            if int(row[2]) == employee_id:
                time = row[0]
                rfid_id = row[1]
                reader_id = int(row[3])
                reader_index = get_index(reader_id, 'readers')
                reader_name = readers[reader_index].get_data()[3]
                writer.writerow([time, rfid_id, reader_id, reader_name])

    file.close()
    logs.close()


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
            date_registered = row[3]

            employees.append(Employee(employee_id, name, surname, date_registered, ''))

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
            date_registered = row[1]
            description = row[3]

            readers.append(Reader(reader_id, date_registered, '', description))

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
            employee_id = -1
        else:
            employee_id = int(row[1])
        date_actualized = row[2]

        cards.append(Card(rfid_tag, employee_id, date_actualized))

    file.close()


def load_db():
    __load_cards()
    __load_employees()
    __load_readers()
