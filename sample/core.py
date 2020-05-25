from datetime import date

from sample.helper import *
from sample.error import *


def register_reader(name):
    readers.append(Reader(reader_id=Reader.reader_id_counter, date_registered=date.today(), date_unregistered=None,
                          description=name, edited=True))
    Reader.reader_id_counter += 1
    save_changes_reader(-1)
    pass


def unregister_reader(reader_id):
    index = get_reader_index(reader_id)

    if index is -1:
        not_found_err(": core.py - unregister_reader")
    else:
        if readers[index].get_data()[2] is '':
            readers[index].unregister(date=date.today())
            readers[index].set_edited(True)
            save_changes_reader(index)
            readers.pop(index)
        else:
            impossible_err(": core.py - unregister_reader")
    pass


def register_card(rfid_tag):
    cards.append(Card(rfid_tag=rfid_tag, date=date.today()))
    save_changes_card(-1)
    pass


def register_card_user(rfid_tag, user_id):
    cards.append(Card(rfid_tag=rfid_tag, employee_id=user_id, date=date.today()))
    save_changes_card(-1)
    pass


def unregister_card_user(reader_id):
    index = get_reader_index(reader_id)

    if index is -1:
        not_found_err(": core.py - unregister_reader")
    else:
        if readers[index].get_data()[2] is '':
            readers[index].unregister(date=date.today())
            readers[index].set_edited(True)
            save_changes_reader(index)
            readers.pop(index)
        else:
            impossible_err(": core.py - unregister_reader")
    pass


if __name__ == "__main__":
    load_db()
