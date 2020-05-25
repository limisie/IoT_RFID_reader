workers = []
clients = []


def register_worker():
    pass


def __add_worker(name, surname, rfid_id):
    workers.append(Worker(name, surname, rfid_id))


def add_reader(name):
    clients.append(Client(name))


class Worker:
    __worker_counter = 0

    def __init__(self, name, surname, rdif_id):
        self.__id = self.__worker_counter
        self.__worker_counter += 1
        self.__name = name
        self.__surname = surname
        self.__rdif_id = rdif_id
        self.__logged_in = False
        self.__logs = []

    def get_full_name(self):
        return str(self.__name, self.__surname)


class Client:
    __terminal_counter = 0

    def __init__(self, name):
        self.__terminal_id = self.__terminal_counter
        self.__terminal_counter += 1
        self.__name = name

    def log_worker(self, rdif_id):
        pass
