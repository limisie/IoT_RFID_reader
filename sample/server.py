#!/usr/bin/env python3
import logging
from tkinter import simpledialog

import paho.mqtt.client as mqtt
import tkinter
from datetime import datetime

from helper import *
from core import *

# The broker name or IP address.

broker = "Kajas-MBP"
port = 8883

client = mqtt.Client()
window = tkinter.Tk()
logging.basicConfig(filename='./data/server.log', level=logging.INFO)


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode('utf-8'))).split(',')

    if message_decoded[1] == '1':
        connection_message(get_index(int(message_decoded[0]), 'readers'))
    elif message_decoded[1] == '0':
        disconnection_message(get_index(int(message_decoded[0]), 'readers'))
    else:
        read_message(get_index(int(message_decoded[0]), 'readers'), message_decoded[1])


def new_employee():
    name = simpledialog.askstring('Rejestracja nowego użytkownika', 'Podaj imię', parent=window)
    surname = simpledialog.askstring('Rejestracja nowego użytkownika', 'Podaj nazwisko', parent=window)
    register_employee(name, surname)


def sign_card():
    rfid_id = simpledialog.askstring('Przypisanie karty RFID pracownikowi', 'Podaj numer karty RFID', parent=window)
    employee_id = simpledialog.askstring('Przypisanie karty RFID pracownikowi', 'Podaj numer pracownika', parent=window)
    register_card(rfid_id, int(employee_id))


def new_card():
    rfid_id = simpledialog.askstring('Rejestracja nowej karty RFID', 'Podaj numer karty RFID', parent=window)
    register_card(rfid_id)


def delete_employee():
    employee_id = simpledialog.askstring('Wyrejestruj pracownika', 'Podaj numer pracownika', parent=window)
    unregister_employee(int(employee_id))


def new_reader():
    name = simpledialog.askstring('Rejestracja nowego czytnika RFID', 'Podaj krótki opis czytnika', parent=window)
    register_reader(name)
    new_topic = 'client' + str(readers[-1].get_id()) + '/read'
    client.subscribe(new_topic)


def delete_reader():
    reader_id = simpledialog.askstring('Wyrejestruj czytnik kart RFID', 'Podaj numer czytnika', parent=window)
    unregister_reader(int(reader_id))
    topic = 'client' + reader_id + '/read'
    client.unsubscribe(topic)


# def new_employee_window():
#     new_employee = tkinter.Tk()
#     new_employee.title("Zarejestruj nowego pracownika")
#
#     name_input_label = tkinter.Label(new_employee, text="Imię")
#     name_input_label.grid(row=0, column=0)
#
#     name_input_area = tkinter.Entry(new_employee)
#     name_input_area.grid(row=0, column=1)
#
#     surname_input_label = tkinter.Label(new_employee, text="Nazwisko")
#     surname_input_label.grid(row=1, column=0)
#
#     surname_input_area = tkinter.Entry(new_employee)
#     surname_input_area.grid(row=1, column=1)
#
#     button = tkinter.Button(new_employee, text="Dodaj pracownika", width=10,
#                             command=lambda: [register_employee(name_input_area.get(), surname_input_area.get()),
#                                              new_employee.destroy()])
#     button.grid(row=2, column=1)
#
#     button_stop = tkinter.Button(new_employee, text="Anuluj", width=10, command=new_employee.destroy())
#     button_stop.grid(row=2, column=0)


def create_main_window():
    window.geometry("274x155")
    window.title("Serwer")
    hello_button = tkinter.Button(window, text="Hello from the server",
                                  command=lambda: client.publish("server/log", "Hello from the server"), width=30)
    new_employee_button = tkinter.Button(window, text="Zarejestruj nowego pracownika", width=30,
                                         command=lambda: new_employee())
    new_employee_button.grid(row=0, column=0)

    employee_card_button = tkinter.Button(window, text="Przypisz pracownikowi kartę RFID", width=30,
                                          command=lambda: sign_card())
    employee_card_button.grid(row=1, column=0)

    new_card_button = tkinter.Button(window, text="Zarejestruj nową kartę RFID", width=30, command=lambda: new_card())
    new_card_button.grid(row=2, column=0)

    delete_employee_button = tkinter.Button(window, text="Wyrejestruj pracownika", width=30,
                                          command=lambda: delete_employee())
    delete_employee_button.grid(row=3, column=0)

    new_reader_button = tkinter.Button(window, text="Zarejestruj nowy czytnik kart RFID", width=30,
                                          command=lambda: new_reader())
    new_reader_button.grid(row=4, column=0)

    delete_reader_button = tkinter.Button(window, text="Wyrejestruj czytnik kart RFID", width=30,
                                          command=lambda: delete_reader())
    delete_reader_button.grid(row=5, column=0)

    exit_button = tkinter.Button(window, text="Zamknij", command=window.quit, width=30)
    exit_button.grid(row=6, column=0)


def connect_to_broker():
    client.tls_set("./certs/ca.crt")
    client.username_pw_set(username="server", password="1234")
    client.connect(broker, port)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("client/logs")
    for reader in readers:
        topic = 'client' + str(reader.get_id()) + '/read'
        client.subscribe(topic)


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()


if __name__ == "__main__":
    load_db()
    run_receiver()
