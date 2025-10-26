from flask import Flask, request, jsonify, render_template, Response
# from flask_socketio import SocketIO, emit
from command_runner import Runner
import subprocess
from time import sleep
import queue
import json
from flask_sse import sse

app = Flask(__name__)
#app.register_blueprint(command_runner)
# socketio = SocketIO(app, cors_allowed_origins="*")  # pozwala na połączenia z frontendu
#status_queue = queue.Queue()
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")
runner = Runner()


@app.route("/")
def home():
    subprocess.Popen(["cmd", "/c", "start", "python", "tcp_proxy.py"])
    print("Uruchomienie proxy.")
    sleep(2)
    return render_template("index.html")


@app.route("/api/check", methods=["POST"])
def check():
    subprocess.Popen(["cmd", "/c", "start", "python", "tcp_simulator.py"])
    #proc = subprocess.Popen(["python", "tcp_simulator.py"])
    print("Uruchomienie symulatora")
    data = request.get_json()
    slots = data.get("slots", [])
    sleep(2)
    try:
        runner.run_commands(slots)
    except ValueError as e:
        return jsonify({"status" : "error", "message" : str(e)})
    #proc.terminate()
    print("Odebrano: ", slots)
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
    return jsonify(runner.cmd.oxidizer_level_data)

# @app.route("/api/statement")
# def get_status():
#     def event_stream():
#         while True:
#             # Czeka na nowy sygnał (blokuje się do momentu, aż coś przyjdzie)
#             data = status_queue.get()
#             print(data)
#             # Wysyłamy dane do klienta (SSE format)
#             yield f"data: {json.dumps(data)}\n\n"
#     print("krawuriwaujkwajudawu")
#     return Response(event_stream(), mimetype="text/event-stream")


# Funkcja, którą możesz wywoływać z innych części aplikacji
# def send_signal(data):
#     print(data)
#     status_queue.put(data)  # wrzuca dane do kolejki

if __name__ == "__main__":
    #socketio.run(app, debug=True)
    app.run(debug=True, threaded=True)

    