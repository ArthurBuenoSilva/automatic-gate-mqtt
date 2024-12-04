from flask import render_template, jsonify

from app.automatic_gate import bp
from app.automatic_gate.mqtt import mqtt_client


@bp.route('/')
def index():
    return render_template("base.html")


@bp.route('/get_current_state', methods=['GET'])
def get_current_state():
     mqtt_client.get_current_state()

     return jsonify(), 200


@bp.route('/open_gate', methods=['POST'])
def open_gate():
    mqtt_client.open_gate()

    return jsonify(), 200


@bp.route('/close_gate', methods=['POST'])
def close_gate():
    mqtt_client.close_gate()

    return jsonify(), 200


@bp.route('/stop_gate', methods=['POST'])
def stop_gate():
    mqtt_client.stop_gate()

    return jsonify(), 200