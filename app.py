from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
from command_runner import Runner
import subprocess
from time import sleep
#from command_runner import command_runner

app = Flask(__name__)
#app.register_blueprint(command_runner)
# socketio = SocketIO(app, cors_allowed_origins="*")  # pozwala na połączenia z frontendu
runner = Runner()


@app.route("/")
def home():
    subprocess.Popen(["cmd", "/c", "start", "python", "tcp_proxy.py"])
    print("Uruchomienie proxy.")
    return render_template("index.html")


@app.route("/api/check", methods=["POST"])
def check():
    subprocess.Popen(["cmd", "/c", "start", "python", "tcp_simulator.py"])
    #proc = subprocess.Popen(["python", "tcp_simulator.py"])
    print("Uruchomienie symulatora")
    data = request.get_json()
    slots = data.get("slots", [])
    runner.run_commands(slots)
    print("Odebrano: ", slots)
    #proc.terminate()
    return jsonify({"status" : "ok", "received": slots})


""" @app.route("/api/status")
def sending_status():
    data = {
        "state": "LAUNCH_READY",
        "rocketstatus": "All systems nominal.",
        "sensors": {
            "fuel_level": 100,
            "oxidizer_level": 100,
            "oxidizer_pressure": 60,
            "altitude": 0
        },
        "servos": {
            "fuel_intake": 0,
            "oxidizer_intake": 0,
            "fuel_main": "closed",
            "oxidizer_main": "closed"
        },
        "relays": {
            "oxidizer_heater": 0,
            "igniter": 0,
            "parachute": "armed"
        },
        "velocity": 0.0,
        "angle": 90
    }
    return jsonify(data) """

# @socketio.on("connect")
# def handle_connect():
#     print("Frontend połączony przez WebSocket")

@app.route("/api/oxidizer_data")
def get_oxidizer_data():
    if not runner.oxidizer_level:
        return jsonify({"status": "pending"}), 202
    print("jeeest")
    return jsonify(runner.cmd.oxidizer_level_data)


if __name__ == "__main__":
    #socketio.run(app, debug=True)
    app.run(debug=True)

    