from enum import Enum
from app.extensions import socketio

import paho.mqtt.client as mqtt


class State(Enum):
    OPEN = 0
    CLOSE = 1
    STOP = 2
    UNKNOWN = 3


class MQTTClient:
    BROKER = "test.mosquitto.org"
    PORT = 1883
    TOPIC = "Inatel/C115/2024/Semester/02/"

    def __init__(self):
        self._last_state: State = State.CLOSE
        self._current_state: State = State.STOP
        self._client = mqtt.Client()
        self._init_client()

    def _init_client(self):
        self._client.connect(self.BROKER, self.PORT, 60)
        self._client.on_message = self._callback
        self._client.subscribe(self.TOPIC + "#") 
        self._client.subscribe(self.TOPIC + "gate/state")
        self._client.loop_start()

        self._client.publish(self.TOPIC + "first_message", "MQTTClient connected")

    def _callback(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")
        if message.topic == self.TOPIC + "gate/state/answer":
            try:
                state_value = int(message.payload.decode())
                self._last_state = self._current_state
                self._current_state = State(state_value)
            except ValueError:
                self._current_state = State.UNKNOWN
            socketio.emit("update_current_state", self._current_state.name.capitalize())

    def stop_loop(self):
        self._client.loop_stop()
        self._client.disconnect()

    def can_it_send_action(self, state: State) -> bool:
        if state == self._last_state and self._current_state == State.STOP:
            return False
        elif self._last_state == State.STOP and self._current_state == state:
            return False
        return True

    def open_gate(self):
        if self.can_it_send_action(State.OPEN):
            self._client.publish(self.TOPIC + "gate/action", State.OPEN.value)

    def close_gate(self):
        if self.can_it_send_action(State.CLOSE):
            self._client.publish(self.TOPIC + "gate/action", State.CLOSE.value)

    def stop_gate(self):
        if self.can_it_send_action(State.STOP):
            self._client.publish(self.TOPIC + "gate/action", State.STOP.value)

    def get_current_state(self):
        self._client.publish(self.TOPIC + "gate/state", 0)
        print("Command sent: get_state")


mqtt_client = MQTTClient()
