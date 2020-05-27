import logging
from datetime import datetime

from helper import *
from error import *

log_file = './data/server.log'

logging.basicConfig(filename=log_file, level=logging.INFO)


def register_reader(name=''):
    readers.append(
        Reader(reader_id=Reader.reader_id_counter, date_registered=datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
               date_unregistered='',
               description=name))
    Reader.reader_id_counter += 1

    __log_reader_register(readers[-1].get_id())
    save_changes(-1, 'readers')


def unregister_reader(reader_id):
    index = get_index(reader_id, 'readers')

    if index is -1:
        __log_warning(not_found_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), ": core.py - unregister_reader "
                                    "- podanego czytnika nie ma aktualnie zarejestrowanego w systemie"))
    else:
        readers[index].unregister(date=datetime.today().strftime('%d/%m/%Y %H:%M:%S'))

        __log_reader_unregister(reader_id)
        save_changes(index, 'readers')
        readers.pop(index)


def register_card(rfid_tag, employee_id=-1):
    index = get_index(rfid_tag, 'cards')

    if employee_id == -1:
        if index is -1:
            cards.append(Card(rfid_tag=rfid_tag, employee_id=-1, date=datetime.today().strftime('%d/%m/%Y %H:%M:%S')))
            __log_card_register(rfid_tag)
            save_changes(-1, 'cards')
        else:
            __log_warning(impossible_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                                         (": core.py - register_card: karta no. {} "
                                          "- podana karta jest już w systemie").format(rfid_tag)))
    else:
        employee_index = get_index(employee_id, 'employees')
        if employee_index is -1:
            __log_warning(not_found_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                                        ": core.py - register_card: pracownik no {} nie istnieje".format(employee_id)))
            if index is -1:
                cards.append(Card(rfid_tag=rfid_tag, employee_id=-1,
                                  date=datetime.today().strftime('%d/%m/%Y %H:%M:%S')))
                __log_card_register(rfid_tag)
                save_changes(-1, 'cards')
            else:
                __log_warning(impossible_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                                             (": core.py - register_card: karta no. {} "
                                              "- podana karta jest już w systemie").format(rfid_tag)))
        else:
            if index is -1:
                cards.append(Card(rfid_tag=rfid_tag, employee_id=employee_id,
                                  date=datetime.today().strftime('%d/%m/%Y %H:%M:%S')))
                __log_card_register(rfid_tag)
                __log_sign_card(rfid_tag, employee_id)
                save_changes(-1, 'cards')
            elif index is not -1 and cards[index].get_employee_id() is -1:
                cards[index].set_new_employee(employee_id)
                __log_sign_card(rfid_tag, employee_id)
                save_changes(index, 'cards')
            else:
                __log_warning(impossible_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                                             (": core.py - register_card: karta no. {} "
                                              "- podana karta ma już przypisanego pracownika").format(rfid_tag)))


def unregister_card_employee(rfid_tag):
    index = get_index(rfid_tag, 'cards')

    if index is -1:
        __log_warning(not_found_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                                    (": core.py - unregister_card_employee: karta no. {} "
                                     "- podana karta nie istnieje w systemie").format(rfid_tag)))
    else:
        if cards[index].get_employeyee_id() is not -1:
            __log_unsign_card(rfid_tag)
            cards[index].set_new_employee(-1)
            cards[index].set_date(datetime.today().strftime('%d/%m/%Y %H:%M:%S'))
            save_changes(index, 'cards')
        else:
            __log_warning(impossible_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                                         (": core.py - unregister_card_employee: karta no. {} - "
                                          "podana karta nie jest skojarzona z żadnym użytkownikiem").format(rfid_tag)))


def register_employee(name, surname):
    employees.append(Employee(employee_id=Employee.employee_id_counter, name=name, surname=surname,
                              date_registered=datetime.today().strftime('%d/%m/%Y %H:%M:%S'), date_unregistered=''))
    __log_employee_register(employees[-1].get_id(), -1)
    Employee.employee_id_counter += 1
    save_changes(-1, 'employees')
    pass


def unregister_employee(employee_id):
    index = get_index(employee_id, 'employees')

    if index is -1:
        __log_warning(not_found_err(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), ": core.py - unregister_employee"
                      " - podanego pracownika nie ma aktualnie zarejestrowanego w systemie"))
    else:
        employees[index].unregister(date=datetime.today().strftime('%d/%m/%Y %H:%M:%S'))
        __log_employee_unregister(employee_id, index)
        save_changes(index, 'employees')
        employees.pop(index)
    pass


def connection_message(index):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' połączono ' + readers[index].to_string()
    logging.info(log)
    print(log)
    pass


def disconnection_message(index):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' rozłączono ' + readers[index].to_string()
    logging.info(log)
    print(log)
    pass


def read_message(reader_index, card_id):
    reader = readers[reader_index]
    date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
    card_index = get_index(card_id, 'cards')

    if card_index == -1:
        employee_data = 'podanej karty nie ma w systemie '
        log = date + ' karta RFID no. ' + card_id + ', ' + employee_data + ', ' + reader.to_string()
        logging.warning(log)
    else:
        employee_id = cards[card_index].get_employee_id()
        if employee_id == -1:
            employee_data = 'podana karta nie jest skojarzona z żadnym pracownikiem '
            log = date + ' karta RFID no. ' + card_id + ', ' + employee_data + ', ' + reader.to_string()
            logging.warning(log)
        else:
            employee_index = get_index(employee_id, 'employees')
            employee_data = employees[employee_index].to_string()
            log = date + ' karta RFID no. ' + card_id + ', ' + employee_data + ', ' + reader.to_string()
            logging.info(log)
    print(log)
    save_log(date, card_id, reader.get_id())
    pass


def logs_to_list():
    file = open(log_file)

    logs = []
    max_i = 10
    i = 0
    for row in enumerate(reversed(list(file))):
        logs.append(row[1])
        i += 1
        if i == max_i:
            break

    logs.reverse()

    file.close()
    return logs


def __log_sign_card(rfid_tag, employee_id):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' kartę no. ' + rfid_tag \
          + ' przypisano pracownikowi no. ' + str(employee_id)
    logging.info(log)
    print(log)
    pass


def __log_unsign_card(rfid_tag):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' karta no. ' + rfid_tag \
          + ' nie ma już przypisanego pracownika '
    logging.info(log)
    print(log)
    pass


def __log_card_register(rfid_tag):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' zarejestrowano kartę no. ' + rfid_tag
    logging.info(log)
    print(log)
    pass


def __log_card_unregister(rfid_tag):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' wyrejestrowano kartę no. ' + rfid_tag
    logging.info(log)
    print(log)
    pass


def __log_employee_register(employee_id, index):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' zarejestrowano pracownika no. ' + str(employee_id) + ' ' \
          + employees[index].get_full_name()
    logging.info(log)
    print(log)
    pass


def __log_employee_unregister(employee_id, index):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' wyrejestrowano pracownika no. ' + str(employee_id) + ' ' \
          + employees[index].get_full_name()
    logging.info(log)
    print(log)
    pass


def __log_reader_register(reader_id):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' zarejestrowano czytnik RFID no. ' + str(reader_id)
    logging.info(log)
    print(log)
    pass


def __log_reader_unregister(reader_id):
    log = datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' wyrejestrowano czytnik RFID no. ' + str(reader_id)
    logging.info(log)
    print(log)


def __log_warning(message):
    logging.warning(message)
    print(message)
