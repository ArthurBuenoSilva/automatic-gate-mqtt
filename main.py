from app import create_app
from app.extensions import socketio
from app.automatic_gate.mqtt import mqtt_client
from configuration import HOST, PORT

if __name__ == "__main__":
    app = create_app()
    socketio.run(app=app, host=HOST, port=PORT, allow_unsafe_werkzeug=True)

    mqtt_client.stop_loop()