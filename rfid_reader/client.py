import paho.mqtt.client as mqtt

# The broker name or IP address.
broker = "DESKTOP-JKNSR9D"
port = 8883

# The MQTT client.
client = mqtt.Client()


def call_worker(worker_name):
    client.publish("worker/name", worker_name + "." + terminal_id)


def connect_to_broker():
    client.tls_set("ca.crt")  # provide path to certification
    # Connect to the broker.
    client.connect(broker, port)  # modify connect call by adding port
    # Send message about conenction.
    call_worker("Client connected")


def disconnect_from_broker():
    # Send message about disconenction.
    call_worker("Client disconnected")
    # Disconnet the client.
    client.disconnect()


def run_client():
    connect_to_broker()

    disconnect_from_broker()


if __name__ == "__main__":
    run_client()
