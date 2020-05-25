#!/usr/bin/env python3
from tkinter import messagebox

import paho.mqtt.client as mqtt
import tkinter

terminal_id = "T0"
broker = "Kajas-MBP"
port = 8883

client = mqtt.Client()
window = tkinter.Tk()


def call_worker(worker_name):
    client.publish("worker/name", worker_name + "." + terminal_id, )


def create_main_window():
    window.geometry("300x200")
    window.title("SENDER")

    intro_label = tkinter.Label(window, text="Select employee:")
    intro_label.grid(row=0, columnspan=5)

    button_1 = tkinter.Button(window, text="Employee 1",
                              command=lambda: call_worker("Employee 1"))
    button_1.grid(row=1, column=0)
    button_2 = tkinter.Button(window, text="Employee 2",
                              command=lambda: call_worker("Employee 2"))
    button_2.grid(row=2, column=0)
    button_3 = tkinter.Button(window, text="Employee 3",
                              command=lambda: call_worker("Employee 3"))
    button_3.grid(row=3, column=0)
    button_4 = tkinter.Button(window, text="Employee 4",
                              command=lambda: call_worker("Employee 4"))
    button_4.grid(row=1, column=1)
    button_5 = tkinter.Button(window, text="Employee 5",
                              command=lambda: call_worker("Employee 5"))
    button_5.grid(row=2, column=1)
    button_6 = tkinter.Button(window, text="Employee 6",
                              command=lambda: call_worker("Employee 6"))
    button_6.grid(row=3, column=1)
    button_stop = tkinter.Button(window, text="Stop", command=window.quit)
    button_stop.grid(row=4, columnspan=2)


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8")))
    print(message_decoded)
    messagebox.showinfo("Message from the Server", message_decoded)


def connect_to_broker():
    client.tls_set("./certs/ca.crt")
    client.username_pw_set(username="client", password="1234")
    client.connect(broker, port)
    call_worker("Client connected")
    client.on_message = process_message
    client.loop_start()
    client.subscribe("server/name")


def disconnect_from_broker():
    call_worker("Client disconnected")
    client.loop_stop()
    client.disconnect()


def run_sender():
    connect_to_broker()
    create_main_window()

    # Start to display window (It will stay here until window is displayed)
    window.mainloop()

    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()