#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time

# The broker name or IP address.
broker = "Kajas-MBP"
port = 8883

client = mqtt.Client()
window = tkinter.Tk()


def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    # Print message to console.
    if message_decoded[0] != "Client connected" and message_decoded[0] != "Client disconnected":
        print(time.ctime() + ", " +
              message_decoded[0] + " used the RFID card.")

        # Save to sqlite database.
        connention = sqlite3.connect("workers.db")
        cursor = connention.cursor()
        cursor.execute("INSERT INTO workers_log VALUES (?,?,?)",
                       (time.ctime(), message_decoded[0], message_decoded[1]))
        connention.commit()
        connention.close()
    else:
        print(message_decoded[0] + " : " + message_decoded[1])


def print_log_to_window():
    connection = sqlite3.connect("workers.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM workers_log")
    log_entries = cursor.fetchall()
    labels_log_entry = []
    print_log_window = tkinter.Tk()

    for log_entry in log_entries:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
                "On %s, %s used the terminal %s" % (log_entry[0], log_entry[1], log_entry[2]))))

    for label in labels_log_entry:
        label.pack(side="top")

    connection.commit()
    connection.close()

    # Display this window.
    print_log_window.mainloop()


def create_main_window():
    window.geometry("250x100")
    window.title("RECEIVER")
    label = tkinter.Label(window, text="Listening to the MQTT")
    hello_button = tkinter.Button(window, text="Hello from the server",
                                  command=lambda: client.publish("server/name", "Hello from the server"))
    exit_button = tkinter.Button(window, text="Stop", command=window.quit)
    print_log_button = tkinter.Button(
        window, text="Print log", command=print_log_to_window)

    label.pack()
    hello_button.pack(side="right")
    exit_button.pack(side="right")
    print_log_button.pack(side="right")


def connect_to_broker():
    client.tls_set("./certs/ca.crt")
    client.username_pw_set(username="server", password="1234")
    # Connect to the broker.
    client.connect(broker, port)
    # Send message about conenction.
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("worker/name")


def disconnect_from_broker():
    # Disconnect the client.
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    create_main_window()
    # Start to display window (It will stay here until window is displayed)
    window.mainloop()
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
