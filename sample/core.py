import tkinter
from datetime import date

from sample.helper import *
from sample.error import *


def register_reader(name=''):
    readers.append(Reader(reader_id=Reader.reader_id_counter, date_registered=date.today(), date_unregistered=None,
                          description=name))
    Reader.reader_id_counter += 1
    save_changes(-1, 'readers')
    pass


def unregister_reader(reader_id):
    index = get_index(reader_id, 'readers')

    if index is -1:
        not_found_err(": core.py - unregister_reader - podanego czytnika nie ma aktualnie zarejestrowanego w systemie")
    else:
        readers[index].unregister(date=date.today())
        save_changes(index, 'readers')
        readers.pop(index)
    pass


def register_card(rfid_tag, user_id=''):
    index = get_index(rfid_tag, 'cards')

    if user_id == '':
        if index is -1:
            cards.append(Card(rfid_tag=rfid_tag, date=date.today()))
            save_changes(-1, 'cards')
        else:
            impossible_err((": core.py - register_card: card no {}"
                           " - podana karta jest już w systemie").format(rfid_tag))
    else:
        if index is -1:
            cards.append(Card(rfid_tag=rfid_tag, employee_id=user_id, date=date.today()))
            save_changes(-1, 'cards')
        elif index is not -1 and cards[index].get_user_id() is -1:
            cards[index].set_new_user(user_id)
            save_changes(index, 'cards')
        else:
            impossible_err((": core.py - register_card: card no {}"
                           " - podana karta ma już użytkownika no {},"
                            "jeśli chcesz go zmienić, "
                            "wyrejestruj obecnego użytkownika").format(rfid_tag, cards[index].get_user_id()))
    pass


def unregister_card_user(rfid_tag):
    index = get_index(rfid_tag, 'cards')

    if index is -1:
        not_found_err((": core.py - unregister_card_user: card no {} "
                       "- podana karta nie istnieje w systemie").format(rfid_tag))
    else:
        if cards[index].get_user_id() is not -1:
            cards[index].set_new_user(-1)
            cards[index].set_date(date.today())
            save_changes(index, 'cards')
        else:
            impossible_err((": core.py - unregister_card_user: card no {} "
                           "- podana karta nie jest skojarzona z żadnym użytkownikiem").format(rfid_tag))
    pass


if __name__ == "__main__":
    load_db()
    # for employee in employees:
    #     print(employee.to_string())
    # print()

