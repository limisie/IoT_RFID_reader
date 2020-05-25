from datetime import date

from sample.helper import *
from sample.error import *


def register_reader(name):
    readers.append(Reader(reader_id=Reader.reader_id_counter, date_registered=date.today(), date_unregistered=None,
                          description=name, edited=True))
    Reader.reader_id_counter += 1
    save_changes_readers()
    pass


def unregister_reader(reader_id):
    index = get_reader_index(reader_id)

    if index is -1:
        not_found_err()
    else:
        print(str(readers[index].get_data()))
        if readers[index].get_data()[2] is '':
            readers[index].unregister(date=date.today())
            readers[index].set_edited(True)
        else:
            impossible_err()
    print(str(readers[index].get_data()))
    save_changes_reader(index)
    pass


if __name__ == "__main__":
    load_db()

    for reader in readers:
        print(reader.to_string())

    register_reader('hol')
    unregister_reader(1)
