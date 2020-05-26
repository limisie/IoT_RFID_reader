#!/usr/bin/env python3
from tkinter import messagebox
import paho.mqtt.client as mqtt
import tkinter

reader_id = 1

broker = "Kajas-MBP"
port = 8883
topic = 'client' + str(reader_id) + '/read'

client = mqtt.Client()
window = tkinter.Tk()


def call_card_reading(rfid_id):
    message = str(reader_id) + ',' + rfid_id
    client.publish(topic, message)


def call_connection(up):
    message = str(reader_id) + ',' + str(up)
    client.publish('client/logs', message)


def create_main_window():
    window.geometry("425x53")
    window.title("Czytnik RFID no. {}".format(reader_id))

    input_label = tkinter.Label(window, text="Skanuj kartę RFID nr:")
    input_label.grid(row=0, column=0)

    input_area = tkinter.Entry(window)
    input_area.grid(row=0, column=1)

    button = tkinter.Button(window, text="Skanuj", width=10,
                            command=lambda: call_card_reading(input_area.get()))
    button.grid(row=0, column=2)

    button_stop = tkinter.Button(window, text="Zamknij", width=10, command=window.quit)
    button_stop.grid(row=3, column=2)


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8")))
    print(message_decoded)
    messagebox.showwarning('Wiadomość z serwera', message_decoded)


def connect_to_broker():
    client.tls_set("./certs/ca.crt")
    client.username_pw_set(username="client", password="1234")
    client.connect(broker, port)
    call_connection(1)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("server/log")


def disconnect_from_broker():
    call_connection(0)
    client.loop_stop()
    client.disconnect()


def run_client():
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()


if __name__ == "__main__":
    run_client()
