#!/usr/bin/env python3
import csv
import logging
from tkinter import simpledialog

import paho.mqtt.client as mqtt
import tkinter

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


def employee_report():
    employee_id = simpledialog.askstring('Wygeneruj raport odczytów', 'Podaj numer pracownika', parent=window)
    print_report(int(employee_id))
    print_report_window()


def print_report_window():
    print_report = tkinter.Tk()

    file = open(report, newline='')
    reader = csv.reader(file)

    labels = []

    for row in reader:
        labels.append(tkinter.Label(print_report,
                                    text='%s - RFID no. %s - czytnik %s (%s)' % (row[0], row[1], row[2], row[3])))

    for label in labels:
        label.pack(side="top")

    file.close()

    print_report.mainloop()


def create_main_window():
    window.geometry("274x175")
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

    report_button = tkinter.Button(window, text="Wygeneruj raport dla pracownika", width=30,
                                          command=lambda: employee_report())
    report_button.grid(row=6, column=0)

    exit_button = tkinter.Button(window, text="Zamknij", command=window.quit, width=30)
    exit_button.grid(row=7, column=0)


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
