import paho.mqtt.client as mqtt
import sqlite3
import time
from .content import *

# The broker name or IP address.
broker = "DESKTOP-JKNSR9D"
port = 8883

# The MQTT client.
client = mqtt.Client()


workers = []
clients = []


def register_worker():
    pass


def __add_worker(name, surname, rdif_id):
    workers.append(Worker(name, surname, rdif_id))


def add_reader(name):
    clients.append(Client(name))


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


def connect_to_broker():
    client.tls_set("ca.crt")
    client.username_pw_set(username='server', password='server1234')

    client.connect(broker, port)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("worker/name")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def run_server():
    connect_to_broker()

    disconnect_from_broker()


if __name__ == "__main__":
    run_server()
