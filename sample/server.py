#!/usr/bin/env python3
import distutils
from datetime import datetime
import logging

import paho.mqtt.client as mqtt
import tkinter
import time
from helper import *

# The broker name or IP address.
broker = "Kajas-MBP"
port = 8883

client = mqtt.Client()
window = tkinter.Tk()
logging.basicConfig(filename='./data/server.log', level=logging.INFO)


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode('utf-8'))).split(',')

    if message_decoded[1] == '1':
        log = str(datetime.today()) + ' połączono ' + readers[get_index(int(message_decoded[0]), 'readers')].to_string()
        logging.info(log)
        print(log)
    elif message_decoded[1] == '0':
        log = str(datetime.today()) + ' rozłączono ' + readers[
            get_index(int(message_decoded[0]), 'readers')].to_string()
        logging.info(log)
        print(log)
    else:
        reader = readers[get_index(int(message_decoded[0]), 'readers')]
        card_id = message_decoded[1]
        date = str(datetime.today())
        card_index = get_index(card_id, 'cards')

        if card_index == -1:
            employee_data = 'podana karta nie została zarejestrowana '
            log = date + ' karta RFID no. ' + card_id + ', ' + employee_data + ', ' \
                  + readers[get_index(int(message_decoded[0]), 'readers')].to_string()
            logging.warning(log)
        else:
            employee_id = cards[card_index].get_user_id()
            if employee_id == -1:
                employee_data = 'podana karta nie jest skojarzona z żadnym pracownikiem '
                log = date + ' karta RFID no. ' + card_id + ', ' + employee_data + ', ' \
                      + readers[get_index(int(message_decoded[0]), 'readers')].to_string()
                logging.warning(log)
            else:
                employee_index = get_index(employee_id, 'employees')
                employee_data = employees[employee_index].to_string()
                log = date + ' karta RFID no. ' + card_id + ', ' + employee_data + ', ' \
              + readers[get_index(int(message_decoded[0]), 'readers')].to_string()
                logging.info(log)
        print(log)
        save_log(date, card_id, reader.get_id())


# def print_log_to_window():
#     connection = sqlite3.connect("workers.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM workers_log")
#     log_entries = cursor.fetchall()
#     labels_log_entry = []
#     print_log_window = tkinter.Tk()
#
#     for log_entry in log_entries:
#         labels_log_entry.append(tkinter.Label(print_log_window, text=(
#                 "On %s, %s used the terminal %s" % (log_entry[0], log_entry[1], log_entry[2]))))
#
#     for label in labels_log_entry:
#         label.pack(side="top")
#
#     connection.commit()
#     connection.close()
#
#     # Display this window.
#     print_log_window.mainloop()


def create_main_window():
    window.geometry("250x100")
    window.title("RECEIVER")
    label = tkinter.Label(window, text="Listening to the MQTT")
    hello_button = tkinter.Button(window, text="Hello from the server",
                                  command=lambda: client.publish("server/name", "Hello from the server"))
    exit_button = tkinter.Button(window, text="Stop", command=window.quit)
    # print_log_button = tkinter.Button(
    #     window, text="Print log", command=print_log_to_window)

    label.pack()
    hello_button.pack(side="right")
    exit_button.pack(side="right")
    # print_log_button.pack(side="right")


def connect_to_broker():
    client.tls_set("./certs/ca.crt")
    client.username_pw_set(username="server", password="1234")
    client.connect(broker, port)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("client/log")
    client.subscribe("card/log")


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
